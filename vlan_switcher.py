import json
import logging
import os
import sys
import time
import schedule
import argparse
from pathlib import Path

# Windows service imports
import win32serviceutil
import win32service
import win32event
import servicemanager
import win32api

# Network imports
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException


class VLANSwitcherService(win32serviceutil.ServiceFramework):
    """Simple VLAN Switcher Windows Service"""
    
    _svc_name_ = "VLANSwitcherService"
    _svc_display_name_ = "VLAN Switcher Service"
    _svc_description_ = "Automatically switches VLANs on network interface"
    
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.is_alive = True
        
        # Setup logging
        self.setup_logging()
        
        # Load configuration
        self.config = self.load_config()
        
    def setup_logging(self):
        """Setup logging to file"""
        # Get executable directory
        if hasattr(sys, '_MEIPASS'):
            base_dir = Path(sys.executable).parent
        else:
            base_dir = Path(__file__).parent
            
        # Create logs directory
        log_dir = base_dir / "logs"
        log_dir.mkdir(exist_ok=True)
        
        # Setup logger
        log_file = log_dir / "service.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()  # Also log to console in debug mode
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def load_config(self):
        """Load configuration from config.json"""
        try:
            if hasattr(sys, '_MEIPASS'):
                base_dir = Path(sys.executable).parent
            else:
                base_dir = Path(__file__).parent
                
            config_file = base_dir / "config.json"
            
            if not config_file.exists():
                self.logger.error(f"Configuration file not found: {config_file}")
                return None
                
            with open(config_file, 'r') as f:
                config = json.load(f)                
            self.logger.info("Configuration loaded successfully")
            return config
            
        except Exception as e:
            self.logger.error(f"Error loading configuration: {e}")
            return None
    
    def switch_vlan(self):
        """Switch to the next VLAN in the list"""
        if not self.config:
            self.logger.error("No configuration available")
            return
            
        if not self.config.get("vlans") or len(self.config["vlans"]) == 0:
            self.logger.error("No VLANs configured")
            return
            
        try:
            # Get current VLAN (first in list) and move it to end
            current_vlan = self.config["vlans"][0]
            self.config["vlans"] = self.config["vlans"][1:] + [current_vlan]
            
            self.logger.info(f"Switching to VLAN {current_vlan} on interface {self.config['interface']}")
            self.logger.info(f"Remaining VLANs: {self.config['vlans']}")
            
            # Connect to switch
            device = {
                'device_type': 'cisco_ios',
                'host': self.config["switch_ip"],
                'username': self.config["username"],
                'password': self.config["password"],
                'secret': self.config["enable_password"],
                'timeout': 10,
            }
            
            self.logger.info("Connecting to switch...")
            
            with ConnectHandler(**device) as connection:
                connection.enable()
                
                # Configure interface
                commands = [
                    f"interface {self.config['interface']}",
                    f"switchport access vlan {current_vlan}",
                    "exit"
                ]
                
                output = connection.send_config_set(commands)
                self.logger.info(f"VLAN switch completed successfully")
                self.logger.debug(f"Switch output: {output}")
                
        except (NetmikoTimeoutException, NetmikoAuthenticationException) as e:
            self.logger.error(f"Network error: {e}")
        except Exception as e:
            self.logger.error(f"Error switching VLAN: {e}")
    
    def SvcStop(self):
        """Stop the service"""
        self.logger.info("Service stop requested")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_alive = False
        
    def SvcDoRun(self):
        """Main service loop"""
        self.logger.info("VLAN Switcher Service starting")
        
        if not self.config:
            self.logger.error("Service cannot start without valid configuration")
            return
            
        # Log service to Windows Event Log
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        
        self.logger.info(f"Service configured for switch {self.config['switch_ip']}")
        self.logger.info(f"Schedule: Every {self.config['schedule_minutes']} minute(s)")
        self.logger.info(f"Interface: {self.config['interface']}")
        self.logger.info(f"VLANs: {self.config['vlans']}")
        
        try:
            # Schedule the VLAN switching
            schedule.every(self.config["schedule_minutes"]).minutes.do(self.switch_vlan)
            
            # Main service loop
            while self.is_alive:
                # Check for stop signal
                if win32event.WaitForSingleObject(self.hWaitStop, 1000) == win32event.WAIT_OBJECT_0:
                    break
                    
                # Run scheduled tasks
                schedule.run_pending()
                
        except Exception as e:
            self.logger.error(f"Service error: {e}")
            servicemanager.LogErrorMsg(f"Service error: {e}")
            
        self.logger.info("VLAN Switcher Service stopped")


def run_debug_mode():
    """Run in debug mode (non-service mode for testing)"""
    print("=" * 50)
    print("VLAN Switcher - Debug Mode")
    print("=" * 50)
    print("Press Ctrl+C to stop\n")
    
    # Setup logging for debug
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    try:
        # Create a simple test instance without Windows service framework
        print("Loading configuration...")
        
        # Get executable directory
        if hasattr(sys, '_MEIPASS'):
            base_dir = Path(sys.executable).parent
        else:
            base_dir = Path(__file__).parent
            
        # Create logs directory
        log_dir = base_dir / "logs"
        log_dir.mkdir(exist_ok=True)
        
        # Load configuration
        config_file = base_dir / "config.json"
        
        if not config_file.exists():
            print(f"ERROR: Configuration file not found: {config_file}")
            return
            
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        print(f"Configuration loaded:")
        print(f"  Switch IP: {config['switch_ip']}")
        print(f"  Interface: {config['interface']}")
        print(f"  Schedule: Every {config['schedule_minutes']} minute(s)")
        print(f"  VLANs: {config['vlans']}")
        print(f"  VLAN count: {len(config['vlans'])}")
        print()
        
        # Validate VLANs
        if not config.get("vlans") or len(config["vlans"]) == 0:
            print("ERROR: No VLANs configured in config.json!")
            return
        
        def test_switch_vlan():
            """Test VLAN switching function"""
            if not config.get("vlans") or len(config["vlans"]) == 0:
                logger.error("No VLANs configured")
                return
                
            try:
                # Get current VLAN (first in list) and move it to end
                current_vlan = config["vlans"][0]
                config["vlans"] = config["vlans"][1:] + [current_vlan]
                
                logger.info(f"Switching to VLAN {current_vlan} on interface {config['interface']}")
                logger.info(f"Remaining VLANs: {config['vlans']}")
                
                # Connect to switch
                device = {
                    'device_type': 'cisco_ios',
                    'host': config["switch_ip"],
                    'username': config["username"],
                    'password': config["password"],
                    'secret': config["enable_password"],
                    'timeout': 10,
                }
                
                logger.info("Connecting to switch...")
                
                with ConnectHandler(**device) as connection:
                    connection.enable()
                    
                    # Configure interface
                    commands = [
                        f"interface {config['interface']}",
                        f"switchport access vlan {current_vlan}",
                        "exit"
                    ]
                    
                    output = connection.send_config_set(commands)
                    logger.info(f"VLAN switch completed successfully")
                    logger.debug(f"Switch output: {output}")
                    
            except (NetmikoTimeoutException, NetmikoAuthenticationException) as e:
                logger.error(f"Network error: {e}")
            except Exception as e:
                logger.error(f"Error switching VLAN: {e}")
        
        # Schedule the function
        schedule.every(config["schedule_minutes"]).minutes.do(test_switch_vlan)
        
        print("Debug mode running...")
        print("Service will execute according to schedule.")
        print()
        
        # Run one cycle immediately for testing
        print("Running one test cycle...")
        test_switch_vlan()
        print()
        
        # Continue with scheduled execution
        while True:
            schedule.run_pending()
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nStopping debug mode...")
    except Exception as e:
        print(f"Debug mode error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='VLAN Switcher Service')
    parser.add_argument('action', nargs='?', 
                       choices=['install', 'start', 'stop', 'remove', 'debug'],
                       help='Service action to perform')
    parser.add_argument('--username', help='Username to run service as')
    parser.add_argument('--password', help='Password for the service user')
    
    args, unknown = parser.parse_known_args()
    
    try:
        if args.action == 'debug':
            # Debug mode - run without service controller
            run_debug_mode()
        elif args.action in ['install', 'start', 'stop', 'remove']:
            # Service management
            if args.action == 'install' and args.username and args.password:
                # Install with user credentials
                sys.argv = [sys.argv[0], 'install', '--username', args.username, '--password', args.password] + unknown
            
            # Handle service commands
            win32serviceutil.HandleCommandLine(VLANSwitcherService)
        elif len(sys.argv) == 1:
            # No arguments - running as service
            servicemanager.Initialize()
            servicemanager.PrepareToHostSingle(VLANSwitcherService)
            servicemanager.StartServiceCtrlDispatcher()
        else:
            # Show help
            parser.print_help()
            print("\nExamples:")
            print("  python vlan_switcher.py install          - Install service as Local System")
            print("  python vlan_switcher.py install --username USER --password PASS")
            print("  python vlan_switcher.py start            - Start the service")
            print("  python vlan_switcher.py stop             - Stop the service") 
            print("  python vlan_switcher.py remove           - Remove the service")
            print("  python vlan_switcher.py debug            - Run in debug mode")
            
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure you're running as Administrator for service operations.")
        sys.exit(1)
