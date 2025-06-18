import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import threading
import subprocess
import os
import sys
from pathlib import Path

class VLANSwitcherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("VLAN Switcher Configuration")
        self.root.geometry("600x700")
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
        
    def create_widgets(self):
        # Main frame with scrollbar
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_frame, text="VLAN Switcher Configuration", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Switch Configuration Section
        switch_frame = ttk.LabelFrame(main_frame, text="Switch Configuration", padding=10)
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
        vlan_frame = ttk.LabelFrame(main_frame, text="VLAN Configuration", padding=10)
        vlan_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        ttk.Label(vlan_frame, text="VLANs (one per line):").pack(anchor=tk.W)
        self.vlan_text = scrolledtext.ScrolledText(vlan_frame, height=8, width=60)
        self.vlan_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        # Service Configuration Section
        service_frame = ttk.LabelFrame(main_frame, text="Run Service As (Optional)", padding=10)
        service_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Service Username
        ttk.Label(service_frame, text="Service Username:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.service_username_var = tk.StringVar()
        self.service_username_entry = ttk.Entry(service_frame, textvariable=self.service_username_var, width=30)
        self.service_username_entry.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # Service Password
        ttk.Label(service_frame, text="Service Password:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.service_password_var = tk.StringVar()
        self.service_password_entry = ttk.Entry(service_frame, textvariable=self.service_password_var, show="*", width=30)
        self.service_password_entry.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        ttk.Label(service_frame, text="(Leave empty to run as Local System)", 
                 font=('Arial', 8, 'italic')).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
        
        # Buttons Frame
        button_frame = ttk.Frame(main_frame)
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
        service_button_frame = ttk.Frame(main_frame)
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
        
        # Build Executable Button
        build_frame = ttk.Frame(main_frame)
        build_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.build_btn = ttk.Button(build_frame, text="Build Executable", 
                                   command=self.build_executable)
        self.build_btn.pack(side=tk.LEFT)
        
        # Status Text
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding=5)
        status_frame.pack(fill=tk.BOTH, expand=True)
        
        self.status_text = scrolledtext.ScrolledText(status_frame, height=6, width=60)
        self.status_text.pack(fill=tk.BOTH, expand=True)
        
    def get_python_command(self):
        """Get the appropriate Python command for this installation"""
        python_exe = self.base_dir / ".venv" / "Scripts" / "python.exe"
        if python_exe.exists():
            return str(python_exe)
        else:
            return "python"
    
    def run_service_command(self, action, with_credentials=False):
        """Run a service command (install, start, stop, remove)"""
        # Check if we're running as an executable (portable version)
        service_exe = self.base_dir / "VLANSwitcherService.exe"
        if service_exe.exists():
            # Use executable version
            cmd = [str(service_exe), action]
        else:
            # Use Python script version
            service_script = self.base_dir / "windows_service.py"
            cmd = [self.get_python_command(), str(service_script), action]
        
        # Add user credentials for install command if provided
        if action == "install" and with_credentials:
            service_username = self.service_username_var.get().strip()
            service_password = self.service_password_var.get().strip()
            
            if service_username and service_password:
                cmd.extend(["--username", service_username, "--password", service_password])
        
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
                self.vlan_text.delete(1.0, tk.END)
                self.vlan_text.insert(1.0, "\n".join(vlans))
                
                # Load service credentials if available
                self.service_username_var.set(config.get("service_username", ""))
                self.service_password_var.set(config.get("service_password", ""))
                
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
            vlan_text = self.vlan_text.get(1.0, tk.END).strip()
            vlans = [vlan.strip() for vlan in vlan_text.split('\n') if vlan.strip()]
            
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
            
            # Add service credentials if provided
            if self.service_username_var.get().strip():
                config["service_username"] = self.service_username_var.get().strip()
                config["service_password"] = self.service_password_var.get()
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
    
    def install_service(self):
        """Install Windows service"""
        def install_worker():
            try:
                self.save_config()
                self.log_status("Installing Windows service...")
                
                # Check if user credentials are provided
                service_username = self.service_username_var.get().strip()
                service_password = self.service_password_var.get().strip()
                
                if service_username and service_password:
                    self.log_status(f"Installing service to run as user: {service_username}")
                    result = self.run_service_command("install", with_credentials=True)
                else:
                    self.log_status("Installing service to run as Local System")
                    result = self.run_service_command("install", with_credentials=False)
                
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
                messagebox.showerror("Error", error_msg)
        
        threading.Thread(target=install_worker, daemon=True).start()
    
    def start_service(self):
        """Start Windows service"""
        def start_worker():
            try:
                self.log_status("Starting Windows service...")
                
                result = self.run_service_command("start")
                
                if result.returncode == 0:
                    self.log_status("✓ Service started successfully")
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
    
    def build_executable(self):
        """Build executable using PyInstaller"""
        def build_worker():
            try:
                self.save_config()
                self.log_status("Building executable... This may take a few minutes...")
                
                build_script = self.base_dir / "build_exe.bat"
                result = subprocess.run([
                    str(build_script)
                ], capture_output=True, text=True, shell=True, cwd=str(self.base_dir))
                
                if result.returncode == 0:
                    self.log_status("✓ Executable built successfully! Check dist/ folder")
                    messagebox.showinfo("Success", "Executable built successfully!\nCheck the 'dist' folder for the .exe files")
                else:
                    error_msg = f"Build failed: {result.stderr}"
                    self.log_status(error_msg)
                    messagebox.showerror("Error", error_msg)
                    
            except Exception as e:
                error_msg = f"Error building executable: {e}"
                self.log_status(error_msg)
                messagebox.showerror("Error", error_msg)
        
        threading.Thread(target=build_worker, daemon=True).start()
    
    def log_status(self, message):
        """Log message to status text area"""
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)
        self.root.update_idletasks()

def main():
    root = tk.Tk()
    app = VLANSwitcherGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
