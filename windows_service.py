import win32serviceutil
import win32service
import win32event
import servicemanager
import logging
import sys
import os
from pathlib import Path

# Get the directory where the executable/script is located
if hasattr(sys, '_MEIPASS'):
    # Running as PyInstaller executable
    BASE_DIR = Path(sys.executable).parent
else:
    # Running as Python script
    BASE_DIR = Path(__file__).parent

# Add the base directory to the Python path
sys.path.insert(0, str(BASE_DIR))

from vlan_switcher_service import VLANSwitcher

class VLANSwitcherWindowsService(win32serviceutil.ServiceFramework):
    _svc_name_ = "VLANSwitcherService"
    _svc_display_name_ = "VLAN Switcher Service"
    _svc_description_ = "Automatically switches VLANs on Cisco switches"
    
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.is_alive = True
          # Setup logging for service
        log_dir = BASE_DIR / "logs"
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "service.log"),
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def SvcStop(self):
        self.logger.info("Service stop requested")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_alive = False
        
    def SvcDoRun(self):
        self.logger.info("Service starting")
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        
        try:
            # Start the VLAN switcher
            switcher = VLANSwitcher()
            
            # Import schedule here to avoid issues with service
            import schedule
            import time
            
            # Schedule the function
            schedule.every(switcher.config["schedule_minutes"]).minutes.do(switcher.issue_command_to_switch)
            
            self.logger.info("Service running")
            
            while self.is_alive:
                # Check if service should stop
                if win32event.WaitForSingleObject(self.hWaitStop, 1000) == win32event.WAIT_OBJECT_0:
                    break
                    
                # Run pending scheduled tasks
                schedule.run_pending()
                time.sleep(1)
                
        except Exception as e:
            self.logger.error(f"Service error: {e}")
            servicemanager.LogErrorMsg(f"Service error: {e}")
            
    def debug_run(self):
        """Run the service in debug mode (non-service mode for testing)"""
        print("Running VLAN Switcher in debug mode...")
        print("Press Ctrl+C to stop")
        
        try:
            # Start the VLAN switcher
            switcher = VLANSwitcher()
            
            # Import schedule here to avoid issues with service
            import schedule
            import time
            
            # Schedule the function
            schedule.every(switcher.config["schedule_minutes"]).minutes.do(switcher.issue_command_to_switch)
            
            print(f"Service configured: {switcher.config['switch_ip']} - Every {switcher.config['schedule_minutes']} minute(s)")
            print("Running...")
            
            while True:
                # Run pending scheduled tasks
                schedule.run_pending()
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\nStopping debug mode...")
        except Exception as e:
            print(f"Debug mode error: {e}")
            
        self.logger.info("Service stopped")

if __name__ == '__main__':
    try:
        if len(sys.argv) == 1:
            # No arguments - running as service
            servicemanager.Initialize()
            servicemanager.PrepareToHostSingle(VLANSwitcherWindowsService)
            servicemanager.StartServiceCtrlDispatcher()
        elif len(sys.argv) == 2 and sys.argv[1].lower() == 'debug':
            # Debug mode - run without service controller
            service = VLANSwitcherWindowsService([])
            service.debug_run()
        else:
            # Has arguments - check for username/password
            import argparse
            
            # Create a custom argument parser
            parser = argparse.ArgumentParser(description='VLAN Switcher Service')
            parser.add_argument('action', choices=['install', 'start', 'stop', 'remove', 'restart'], 
                              help='Service action to perform')
            parser.add_argument('--username', help='Username to run service as')
            parser.add_argument('--password', help='Password for the service user')
            
            # Parse known args to handle pywin32 service arguments
            args, unknown = parser.parse_known_args()
            
            # If installing with credentials, modify sys.argv for win32serviceutil
            if args.action == 'install' and args.username and args.password:
                # Reconstruct sys.argv for win32serviceutil with user credentials
                sys.argv = [sys.argv[0], 'install', '--username', args.username, '--password', args.password] + unknown
            
            # Handle command line (install, start, stop, remove, etc.)
            win32serviceutil.HandleCommandLine(VLANSwitcherWindowsService)
    except Exception as e:
        # If there's an error, try to log it and show help
        print(f"Service error: {e}")
        print("Available commands:")
        print("  install   - Install the service")
        print("  install --username USER --password PASS - Install service to run as specific user")
        print("  start     - Start the service")
        print("  stop      - Stop the service")
        print("  remove    - Remove the service")
        print("  debug     - Run in debug mode (for testing)")
        sys.exit(1)
