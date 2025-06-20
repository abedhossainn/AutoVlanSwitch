import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import threading
import subprocess
import os
import sys
import datetime
import time
from pathlib import Path

class VLANSwitcherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("VLAN Switcher")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Get the directory where the script/executable is located
        if hasattr(sys, '_MEIPASS'):
            # Running as PyInstaller executable
            self.base_dir = Path(sys.executable).parent
        else:
            # Running as Python script
            self.base_dir = Path(__file__).parent
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        self.create_widgets()
        self.load_config()
        
        # Initialize status tracking variables
        self.current_vlan = "Not Connected"
        self.next_vlan = "N/A" # New
        self.service_running = False
        self.next_switch_time = None
        
        # Start status update timer
        self.update_status_display()
        self.start_status_timer()
        
    def create_widgets(self):
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left frame for configuration
        left_frame = ttk.Frame(main_container, width=400)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        left_frame.pack_propagate(False)

        # Right frame for activity panel
        right_frame = ttk.Frame(main_container, width=380)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        right_frame.pack_propagate(False)

        # --- LEFT FRAME WIDGETS ---

        # Title
        title_label = ttk.Label(left_frame, text="VLAN Switcher Configuration",
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20), anchor='w')
        
        # Switch Configuration Section
        switch_frame = ttk.LabelFrame(left_frame, text="Switch Configuration", padding=10)
        switch_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Switch IP
        ttk.Label(switch_frame, text="Switch IP:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.switch_ip_var = tk.StringVar()
        self.switch_ip_entry = ttk.Entry(switch_frame, textvariable=self.switch_ip_var, width=30)
        self.switch_ip_entry.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # Username
        ttk.Label(switch_frame, text="Username:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(switch_frame, textvariable=self.username_var, width=30)
        self.username_entry.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # Password
        ttk.Label(switch_frame, text="Password:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(switch_frame, textvariable=self.password_var, show="*", width=30)
        self.password_entry.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # Enable Password
        ttk.Label(switch_frame, text="Enable Password:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.enable_password_var = tk.StringVar()
        self.enable_password_entry = ttk.Entry(switch_frame, textvariable=self.enable_password_var, show="*", width=30)
        self.enable_password_entry.grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # Interface
        ttk.Label(switch_frame, text="Interface:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.interface_var = tk.StringVar()
        self.interface_entry = ttk.Entry(switch_frame, textvariable=self.interface_var, width=30)
        self.interface_entry.grid(row=4, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        ttk.Label(switch_frame, text="(e.g., 1/0/10)", font=('Arial', 8)).grid(row=4, column=2, sticky=tk.W, padx=(5, 0))
        
        # Schedule
        ttk.Label(switch_frame, text="Schedule (minutes):").grid(row=5, column=0, sticky=tk.W, pady=2)
        self.schedule_var = tk.StringVar()
        self.schedule_entry = ttk.Entry(switch_frame, textvariable=self.schedule_var, width=30)
        self.schedule_entry.grid(row=5, column=1, sticky=tk.W, padx=(10, 0), pady=2)
          # VLANs Section
        vlan_frame = ttk.LabelFrame(left_frame, text="VLAN Configuration", padding=10)
        vlan_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(vlan_frame, text="VLANs (comma separated):").pack(anchor=tk.W)
        self.vlan_var = tk.StringVar()
        self.vlan_entry = ttk.Entry(vlan_frame, textvariable=self.vlan_var, width=50)
        self.vlan_entry.pack(fill=tk.X, pady=(5, 0))
        ttk.Label(vlan_frame, text="(e.g., 10,20,30,40)", font=('Arial', 8)).pack(anchor=tk.W, pady=(2, 0))
        
        # Buttons Frame
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Save Config Button
        self.save_btn = ttk.Button(button_frame, text="Save Configuration", 
                                  command=self.save_config, style='Accent.TButton')
        self.save_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Test Connection Button
        self.test_btn = ttk.Button(button_frame, text="Test Connection", 
                                  command=self.test_connection)
        self.test_btn.pack(side=tk.LEFT, padx=5)
        
        # Run Console Button
        self.console_btn = ttk.Button(button_frame, text="Run Console Mode", 
                                     command=self.run_console)
        self.console_btn.pack(side=tk.LEFT, padx=5)
        
        # Service Buttons Frame
        service_button_frame = ttk.Frame(left_frame)
        service_button_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Install Service Button
        self.install_btn = ttk.Button(service_button_frame, text="Install Service", 
                                     command=self.install_service)
        self.install_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Start Service Button
        self.start_btn = ttk.Button(service_button_frame, text="Start Service", 
                                   command=self.start_service)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        # Stop Service Button
        self.stop_btn = ttk.Button(service_button_frame, text="Stop Service", 
                                  command=self.stop_service)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
          # Uninstall Service Button
        self.uninstall_btn = ttk.Button(service_button_frame, text="Uninstall Service", 
                                       command=self.uninstall_service)
        self.uninstall_btn.pack(side=tk.LEFT, padx=5)

        # --- RIGHT FRAME WIDGETS (ACTIVITY PANEL) ---

        activity_panel = ttk.LabelFrame(right_frame, text="Activity Panel", padding=10)
        activity_panel.pack(fill=tk.BOTH, expand=True)
        
        # Status grid
        status_grid = ttk.Frame(activity_panel)
        status_grid.pack(fill=tk.X)
        
        # Service Status
        ttk.Label(status_grid, text="Service Status:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=2)
        self.service_status_label = ttk.Label(status_grid, text="Unknown", font=('Arial', 10), foreground="gray")
        self.service_status_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # Current VLAN
        ttk.Label(status_grid, text="Current VLAN:", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=2)
        self.current_vlan_label = ttk.Label(status_grid, text="Not Connected", font=('Arial', 10), foreground="gray")
        self.current_vlan_label.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=2)

        # Next VLAN
        ttk.Label(status_grid, text="Next VLAN:", font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky=tk.W, pady=2)
        self.next_vlan_label = ttk.Label(status_grid, text="N/A", font=('Arial', 10), foreground="gray")
        self.next_vlan_label.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=2)

        # Timer
        ttk.Label(status_grid, text="Next Switch In:", font=('Arial', 10, 'bold')).grid(row=3, column=0, sticky=tk.W, pady=2)
        self.timer_label = ttk.Label(status_grid, text="--:--", font=('Arial', 12, 'bold'), foreground="gray")
        self.timer_label.grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=2)
          # Activity Log
        log_frame = ttk.LabelFrame(activity_panel, text="Logs", padding=5)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(10,0))
        
        self.status_text = scrolledtext.ScrolledText(log_frame, height=6, width=40)
        self.status_text.pack(fill=tk.BOTH, expand=True)

    def get_python_command(self):
        """Get the appropriate Python command for this installation"""
        python_exe = self.base_dir / ".venv" / "Scripts" / "python.exe"
        if python_exe.exists():
            return str(python_exe)
        else:
            return "python"
    
    def run_service_command(self, action):
        """Run a service command (install, start, stop, remove)"""
        # Check if we're running as an executable (portable version)
        service_exe = self.base_dir / "SecureVLANSwitcherService.exe"
        if service_exe.exists():
            # Use executable version
            cmd = [str(service_exe), action]
        else:
            # Fallback to VLANSwitcherService.exe for compatibility
            alt_service_exe = self.base_dir / "VLANSwitcherService.exe"
            if alt_service_exe.exists():
                cmd = [str(alt_service_exe), action]
            else:
                # Use Python script version
                service_script = self.base_dir / "windows_service.py"
                cmd = [self.get_python_command(), str(service_script), action]
        
        return subprocess.run(cmd, capture_output=True, text=True)
    
    def load_config(self):
        """Load existing configuration if available"""
        try:
            config_path = self.base_dir / "config.json"
            if config_path.exists():
                with open(config_path, 'r') as f:
                    config = json.load(f)
                
                self.switch_ip_var.set(config.get("switch_ip", ""))
                self.username_var.set(config.get("username", ""))
                self.password_var.set(config.get("password", ""))
                self.enable_password_var.set(config.get("enable_password", ""))
                self.interface_var.set(config.get("interface", "1/0/10"))
                self.schedule_var.set(str(config.get("schedule_minutes", 1)))
                  # Load VLANs
                vlans = config.get("vlans", [])
                self.vlan_var.set(",".join(vlans))
                
                self.log_status("Configuration loaded successfully")
        except Exception as e:
            self.log_status(f"Error loading configuration: {e}")
    
    def save_config(self):
        """Save configuration to JSON file"""
        try:
            # Validate inputs
            if not self.switch_ip_var.get().strip():
                messagebox.showerror("Error", "Switch IP is required")
                return
            
            if not self.username_var.get().strip():
                messagebox.showerror("Error", "Username is required")
                return
            
            if not self.password_var.get().strip():
                messagebox.showerror("Error", "Password is required")
                return
              # Parse VLANs
            vlan_text = self.vlan_var.get().strip()
            vlans = [vlan.strip() for vlan in vlan_text.split(',') if vlan.strip()]
            
            if not vlans:
                messagebox.showerror("Error", "At least one VLAN is required")
                return
            
            try:
                schedule_minutes = int(self.schedule_var.get())
                if schedule_minutes <= 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("Error", "Schedule minutes must be a positive integer")
                return
            
            # Create configuration
            config = {
                "switch_ip": self.switch_ip_var.get().strip(),
                "username": self.username_var.get().strip(),
                "password": self.password_var.get(),
                "enable_password": self.enable_password_var.get(),
                "interface": self.interface_var.get().strip() or "1/0/10",
                "schedule_minutes": schedule_minutes,
                "vlans": vlans
            }
            
            # Save to file
            config_path = self.base_dir / "config.json"
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=4)
            
            self.log_status("Configuration saved successfully")
            messagebox.showinfo("Success", "Configuration saved successfully!")
            
        except Exception as e:
            error_msg = f"Error saving configuration: {e}"
            self.log_status(error_msg)
            messagebox.showerror("Error", error_msg)
    
    def install_service(self):
        """Install Windows service"""
        def install_worker():
            try:
                self.save_config()
                self.log_status("Installing Windows service...")
                
                self.log_status("Installing service to run as Local System")
                result = self.run_service_command("install")
                
                if result.returncode == 0:
                    self.log_status("✓ Service installed successfully")
                    messagebox.showinfo("Success", "Service installed successfully!")
                else:
                    error_msg = result.stderr.strip()
                    if "Access is denied" in error_msg or result.returncode == 5:
                        admin_msg = ("Service installation failed: Access Denied\n\n"
                                   "Administrator privileges are required to install Windows services.\n\n"
                                   "Please:\n"
                                   "1. Close this application\n"
                                   "2. Right-click 'run_gui.bat'\n"
                                   "3. Select 'Run as Administrator'\n"
                                   "4. Try installing the service again")
                        self.log_status("✗ Installation failed: Administrator privileges required")
                        messagebox.showerror("Administrator Required", admin_msg)
                    else:
                        self.log_status(f"✗ Installation failed: {error_msg}")
                        messagebox.showerror("Installation Failed", error_msg)
                    
            except Exception as e:
                error_msg = f"Error installing service: {e}"
                self.log_status(error_msg)
                messagebox.showerror("Error", error_msg)
        
        threading.Thread(target=install_worker, daemon=True).start()

    def test_connection(self):
        """Test connection to the switch"""
        def test_worker():
            try:
                self.log_status("Testing connection to switch...")
                
                # Save config first
                self.save_config()
                
                # Import here to avoid blocking GUI startup
                from netmiko import ConnectHandler
                
                device = {
                    "device_type": "cisco_ios",
                    "ip": self.switch_ip_var.get().strip(),
                    "username": self.username_var.get().strip(),
                    "password": self.password_var.get(),
                    "secret": self.enable_password_var.get(),
                }
                
                connection = ConnectHandler(**device)
                connection.enable()
                
                # Test a simple command
                output = connection.send_command("show version")
                connection.disconnect()
                
                self.log_status("✓ Connection test successful!")
                messagebox.showinfo("Success", "Connection to switch successful!")
                
            except Exception as e:
                error_msg = f"✗ Connection test failed: {e}"
                self.log_status(error_msg)
                messagebox.showerror("Connection Failed", str(e))
        
        # Run test in background thread
        threading.Thread(target=test_worker, daemon=True).start()
    
    def run_console(self):
        """Run the application in console mode"""
        try:
            self.save_config()
            self.log_status("Starting console mode...")
              # Run in background
            python_exe = self.base_dir / ".venv" / "Scripts" / "python.exe"
            service_script = self.base_dir / "vlan_switcher_service.py"
            
            if python_exe.exists():
                # Use virtual environment if available
                subprocess.Popen([
                    str(python_exe),
                    str(service_script)
                ], creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                # Fallback to system Python or executable
                subprocess.Popen([
                    "python",
                    str(service_script)
                ], creationflags=subprocess.CREATE_NEW_CONSOLE)            
            self.log_status("Console mode started in new window")
            
        except Exception as e:
            error_msg = f"Error starting console mode: {e}"
            self.log_status(error_msg)
            messagebox.showerror("Error", error_msg)
    
    def start_service(self):
        """Start Windows service"""
        def start_worker():
            try:
                self.log_status("Starting Windows service...")
                
                result = self.run_service_command("start")
                
                if result.returncode == 0:
                    self.log_status("✓ Service started successfully")
                    self.set_service_status(True)
                    # Reset status to allow real-time updates
                    self.current_vlan = "Starting..."
                    self.next_switch_time = None
                    messagebox.showinfo("Success", "Service started successfully!")
                else:
                    error_msg = f"Service start failed: {result.stderr}"
                    self.log_status(error_msg)
                    messagebox.showerror("Error", error_msg)
                    
            except Exception as e:
                error_msg = f"Error starting service: {e}"
                self.log_status(error_msg)
                messagebox.showerror("Error", error_msg)
        
        threading.Thread(target=start_worker, daemon=True).start()
    
    def stop_service(self):
        """Stop Windows service"""
        def stop_worker():
            try:
                self.log_status("Stopping Windows service...")
                
                result = self.run_service_command("stop")
                
                if result.returncode == 0:
                    self.log_status("✓ Service stopped successfully")
                    messagebox.showinfo("Success", "Service stopped successfully!")
                else:
                    error_msg = f"Service stop failed: {result.stderr}"
                    self.log_status(error_msg)
                    messagebox.showerror("Error", error_msg)
                    
            except Exception as e:
                error_msg = f"Error stopping service: {e}"
                self.log_status(error_msg)
                messagebox.showerror("Error", error_msg)
        
        threading.Thread(target=stop_worker, daemon=True).start()
    
    def uninstall_service(self):
        """Uninstall Windows service"""
        def uninstall_worker():
            try:
                self.log_status("Uninstalling Windows service...")
                
                result = self.run_service_command("remove")
                
                if result.returncode == 0:
                    self.log_status("✓ Service uninstalled successfully")
                    messagebox.showinfo("Success", "Service uninstalled successfully!")
                else:
                    error_msg = f"Service uninstall failed: {result.stderr}"
                    self.log_status(error_msg)
                    messagebox.showerror("Error", error_msg)
                    
            except Exception as e:
                error_msg = f"Error uninstalling service: {e}"
                self.log_status(error_msg)
                messagebox.showerror("Error", error_msg)
        
        threading.Thread(target=uninstall_worker, daemon=True).start()
    
    def log_status(self, message):
        """Log message to status text area"""
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)
        self.root.update_idletasks()
        
    def update_activity_logs(self):
        """Update the activity log display with recent log entries"""
        try:
            log_file = self.base_dir / "logs" / "vlan_switcher.log"
            if log_file.exists():
                with open(log_file, 'r') as f:
                    lines = f.readlines()
                    # Get the last 20 lines and format them for display
                    recent_lines = lines[-20:] if len(lines) > 20 else lines
                    
                    # Clear the current text and add recent log entries
                    self.status_text.delete(1.0, tk.END)
                    
                    for line in recent_lines:
                        # Clean up the log line for display
                        if ' - INFO - ' in line:
                            # Extract just the message part after the log level
                            message = line.split(' - INFO - ', 1)[1].strip()
                            timestamp = line.split(' - ')[0].split(',')[0]  # Remove milliseconds
                            display_line = f"{timestamp[-8:]} - {message}\n"  # Show only time part
                            self.status_text.insert(tk.END, display_line)
                        elif ' - ERROR - ' in line:
                            message = line.split(' - ERROR - ', 1)[1].strip()
                            timestamp = line.split(' - ')[0].split(',')[0]
                            display_line = f"{timestamp[-8:]} - ERROR: {message}\n"
                            self.status_text.insert(tk.END, display_line)
                        elif line.strip():  # Non-empty line without standard format
                            self.status_text.insert(tk.END, f"{line.strip()}\n")
                    
                    # Scroll to the bottom
                    self.status_text.see(tk.END)
        except Exception as e:
            # If we can't read logs, just keep the existing status messages
            pass

    def check_service_status(self):
        """Check if the service is actually running"""
        try:
            result = subprocess.run(['sc', 'query', 'SecureVLANSwitcherService'], 
                                  capture_output=True, text=True)
            if result.returncode == 0 and 'RUNNING' in result.stdout:
                return True
            return False
        except:            return False
    
    def read_current_vlan_from_logs(self):
        """Read the current VLAN from log files"""
        try:
            log_file = self.base_dir / "logs" / "vlan_switcher.log"
            if log_file.exists():
                with open(log_file, 'r') as f:
                    lines = f.readlines()
                    # Look for the most recent VLAN switch in the logs
                    for line in reversed(lines[-100:]):  # Check last 100 lines
                        if "Switching to VLAN" in line:
                            # Extract VLAN number from log line like "Switching to VLAN 10 on interface"
                            try:
                                parts = line.split("Switching to VLAN ")[1].split(" ")[0]
                                if parts.isdigit():
                                    return parts
                            except (IndexError, AttributeError):
                                continue
                        elif "ERROR" in line.upper() or "Failed" in line:
                            continue  # Skip error lines, look for successful switches
                    
                    # If no VLAN switch found, check if service just started
                    for line in reversed(lines[-50:]):
                        if "Starting VLAN switcher service" in line or "Service started" in line:
                            return "Starting..."
                            
            return "Not Connected"
        except Exception as e:            return "Not Connected"
    
    def calculate_next_switch_time(self):
        """Calculate when the next VLAN switch should occur based on schedule"""
        try:
            schedule_minutes = int(self.schedule_var.get())
            log_file = self.base_dir / "logs" / "vlan_switcher.log"
            if log_file.exists():
                with open(log_file, 'r') as f:
                    lines = f.readlines()
                    # Look for the most recent switch time
                    for line in reversed(lines[-100:]):
                        if "Switching to VLAN" in line:
                            # Try to extract timestamp from log line
                            try:
                                # Log format: "2025-06-19 14:30:25,123 - INFO - Switching to VLAN..."
                                timestamp_str = line.split(' - ')[0]
                                # Remove milliseconds if present
                                if ',' in timestamp_str:
                                    timestamp_str = timestamp_str.split(',')[0]
                                last_switch = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                                return last_switch + datetime.timedelta(minutes=schedule_minutes)
                            except (ValueError, IndexError):
                                continue
            
            # If no log found or can't parse, estimate next switch time
            return datetime.datetime.now() + datetime.timedelta(minutes=schedule_minutes)
        except:
            return None
    
    def update_status_display(self):
        """Update the current status display"""
        try:
            # Check actual service status
            actual_service_running = self.check_service_status()
            self.service_running = actual_service_running
            
            # Update service status
            if actual_service_running:
                self.service_status_label.config(text="Running", foreground="green")
            else:
                self.service_status_label.config(text="Stopped", foreground="red")

            # Get current VLAN from logs if service is running
            if actual_service_running:
                current_vlan_from_logs = self.read_current_vlan_from_logs()
                if current_vlan_from_logs != "Not Connected":
                    self.current_vlan = current_vlan_from_logs
                    
            # Update current VLAN display
            self.current_vlan_label.config(text=self.current_vlan)
            if self.current_vlan == "Not Connected":
                self.current_vlan_label.config(foreground="gray")
            elif self.current_vlan == "Error":
                self.current_vlan_label.config(foreground="red")
            else:
                self.current_vlan_label.config(foreground="green")
              
            # Update next VLAN
            vlans_text = self.vlan_var.get().strip()
            vlans = [vlan.strip() for vlan in vlans_text.split(',') if vlan.strip()]
            if self.current_vlan in vlans and len(vlans) > 1:
                try:
                    current_index = vlans.index(self.current_vlan)
                    next_index = (current_index + 1) % len(vlans)
                    self.next_vlan = vlans[next_index]
                except (ValueError, IndexError):
                    self.next_vlan = vlans[0] if vlans else "N/A"
            elif vlans and actual_service_running:
                # If service is running but current VLAN not in list, show first VLAN as next
                self.next_vlan = vlans[0]
            else:
                self.next_vlan = "N/A"
            self.next_vlan_label.config(text=self.next_vlan)

            # Update timer display
            if actual_service_running:
                # Calculate next switch time from logs
                calculated_next_time = self.calculate_next_switch_time()
                if calculated_next_time:
                    self.next_switch_time = calculated_next_time
                    
                if self.next_switch_time:
                    now = datetime.datetime.now()
                    if self.next_switch_time > now:
                        time_diff = self.next_switch_time - now
                        minutes = int(time_diff.total_seconds() // 60)
                        seconds = int(time_diff.total_seconds() % 60)
                        timer_text = f"{minutes:02d}:{seconds:02d}"
                        self.timer_label.config(text=timer_text, foreground="blue")
                    else:
                        self.timer_label.config(text="Switching...", foreground="orange")
                else:
                    self.timer_label.config(text="Starting...", foreground="orange")
            else:
                self.timer_label.config(text="--:--", foreground="gray")
                
        except Exception as e:
            # Silently handle any display update errors
            pass
    
    def update_current_vlan(self, vlan):
        """Update the current VLAN display"""
        self.current_vlan = vlan
        if vlan == "Not Connected":
            self.current_vlan_label.config(foreground="gray")
        else:
            self.current_vlan_label.config(foreground="green")

    def set_next_switch_time(self, minutes_from_now):
        """Set the next switch time"""
        if minutes_from_now:
            self.next_switch_time = datetime.datetime.now() + datetime.timedelta(minutes=minutes_from_now)
        else:
            self.next_switch_time = None
    
    def set_service_status(self, running):
        """Update service running status"""
        self.service_running = running

    def start_status_timer(self):
        """Start periodic status updates"""
        self.update_status_display()
        # Update activity logs if service is running
        if self.service_running:
            self.update_activity_logs()
        # Schedule next update in 2 seconds
        self.root.after(2000, self.start_status_timer)

def main():
    root = tk.Tk()
    app = VLANSwitcherGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
