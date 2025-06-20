# Secure VLAN Switcher - Enhanced GUI Application

## Overview

The Secure VLAN Switcher is an enhanced version of the original VLAN switching application with advanced security features and improved user interface. This application automatically switches VLANs on a Cisco network switch interface at scheduled intervals.

## New Security Features

### 1. Secure Credential Storage
- **Windows Keyring Integration**: Passwords can be stored securely using the Windows Credential Manager
- **Checkbox Options**: Choose which passwords to store securely (Switch Password, Enable Password, Service Password)
- **Automatic Retrieval**: Stored credentials are automatically loaded when the application starts
- **Clear Credentials**: Button to remove all stored credentials from the system

### 2. Service User Configuration
- **Run as Local System**: Default option for maximum compatibility
- **Run as Specific User**: Configure the service to run under a specific Windows user account
- **User Validation**: Built-in credential validation before service installation
- **Domain Support**: Supports both domain users (DOMAIN\username) and local users (.\username)

### 3. Enhanced Security Documentation
- Uses Microsoft's recommended approaches for Windows services
- Implements secure credential handling following best practices
- Supports Task Scheduler integration for advanced scheduling scenarios

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- Windows 10/11 or Windows Server 2019/2022
- Administrator privileges (for service installation)

### Quick Start
1. **Run the GUI**: Double-click `run_secure_gui.bat`
2. **Configure Settings**: Fill in your switch details and credentials
3. **Enable Secure Storage**: Check "Store securely" for passwords you want to protect
4. **Test Connection**: Click "Test Connection" to verify settings
5. **Install Service**: Click "Install Service" (requires Administrator privileges)
6. **Start Service**: Click "Start Service"

### Required Packages
The application will automatically install these packages:
- `netmiko` - Network device automation
- `schedule` - Task scheduling
- `pywin32` - Windows API integration
- `pyinstaller` - Executable building
- `keyring` - Secure credential storage
- `cryptography` - Encryption support

## Configuration Options

### Switch Configuration
- **Switch IP**: IP address of your Cisco switch
- **Username**: Switch login username
- **Password**: Switch login password (can be stored securely)
- **Enable Password**: Privileged mode password (can be stored securely)
- **Interface**: Network interface to configure (e.g., GigabitEthernet0/1)
- **Schedule**: Interval in minutes between VLAN switches

### VLAN Configuration
- **VLAN List**: One VLAN ID per line
- **Rotation**: VLANs are switched in the order listed, cycling back to the first

### Service User Configuration
- **Local System**: Run as the built-in Local System account (default)
- **Specific User**: Run as a designated Windows user account
  - **Username**: Format as `DOMAIN\username` or `.\username` for local
  - **Password**: User account password (can be stored securely)
  - **Validation**: Test credentials before service installation

## Usage Modes

### 1. GUI Configuration Mode
- Use `run_secure_gui.bat` to start the graphical interface
- Configure all settings through the user-friendly interface
- Test connections and manage the Windows service

### 2. Debug Mode
- Click "Run Debug Mode" in the GUI
- Runs in a console window for testing and troubleshooting
- Shows real-time logging and VLAN switching activity

### 3. Windows Service Mode
- Install as a Windows service for automatic startup
- Runs in the background without user interaction
- Logs activity to `logs/vlan_switcher.log`

## Security Best Practices

### Credential Protection
1. **Always use "Store securely"** for production passwords
2. **Use dedicated service accounts** with minimal required privileges
3. **Regularly rotate passwords** and update stored credentials
4. **Limit network switch access** to required IP ranges

### Service Security
1. **Run as specific user** rather than Local System when possible
2. **Use domain accounts** for centralized credential management
3. **Apply least privilege principle** to service accounts
4. **Monitor service logs** for security events

### Network Security
1. **Use SSH where possible** instead of Telnet
2. **Implement network segmentation** for management traffic
3. **Use strong authentication** on network devices
4. **Enable audit logging** on switches

## Troubleshooting

### Common Issues

**"Access Denied" during service installation:**
- Right-click `run_secure_gui.bat` and select "Run as Administrator"
- Ensure your user account has Administrator privileges

**"Connection Failed" when testing:**
- Verify switch IP address and network connectivity
- Check username and password
- Ensure switch allows SSH/Telnet connections
- Verify interface name format (e.g., GigabitEthernet0/1)

**Service won't start:**
- Check Windows Event Viewer for detailed error messages
- Verify service user credentials are valid
- Ensure configuration file exists and is valid
- Check log files in the `logs` directory

**Stored credentials not working:**
- Clear all stored credentials and re-enter them
- Ensure keyring service is available on your system
- Check Windows Credential Manager for stored entries

### Log Files
- **Service Log**: `logs/vlan_switcher.log`
- **Windows Event Log**: Check "Windows Logs > Application" for service events
- **GUI Status**: Real-time status shown in the GUI status area

## Advanced Configuration

### Custom Scheduling
For more advanced scheduling beyond simple minutes intervals, you can:
1. Install the service to run as a specific user
2. Use Windows Task Scheduler to create custom schedules
3. Configure the task to run the debug mode at specific times

### Multiple Switch Support
To manage multiple switches:
1. Create separate configuration files for each switch
2. Install multiple service instances with different names
3. Use different directories for each instance

### Integration with Existing Systems
The application can be integrated with:
- **Monitoring Systems**: Parse log files for VLAN change events
- **Network Management**: Use APIs to trigger VLAN changes
- **Security Systems**: Monitor for unauthorized changes

## API Documentation References

This application implements security features based on:
- [CreateProcessWithLogonW](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-createprocesswithlogonw)
- [Windows Task Scheduler](https://learn.microsoft.com/en-us/windows/win32/taskschd/about-the-task-scheduler)
- [Python Keyring Library](https://pypi.org/project/keyring/)

## Support and Maintenance

### Updates
- Keep Python packages updated: `pip install -r requirements.txt --upgrade`
- Monitor for security updates to dependencies
- Test configuration changes in debug mode first

### Backup
- Backup `config.json` file before making changes
- Document custom configurations and service account details
- Keep a record of stored credential locations

### Monitoring
- Regularly check log files for errors or warnings
- Monitor Windows Event Viewer for service-related events
- Verify VLAN switching is occurring as expected

## File Structure

```
AutoVlanSwitch/
├── secure_vlan_gui.py          # Enhanced GUI application
├── secure_vlan_switcher.py     # Enhanced service module
├── run_secure_gui.bat          # Startup script
├── config_template.json        # Configuration template
├── config.json                 # Active configuration (created by GUI)
├── requirements.txt            # Python dependencies
├── logs/                       # Log files directory
│   └── vlan_switcher.log      # Service log file
└── SECURITY_FEATURES.md        # This documentation file
```

## License and Disclaimer

This software is provided as-is for educational and operational use. Users are responsible for:
- Ensuring compliance with network security policies
- Testing thoroughly before production deployment
- Maintaining secure credential practices
- Monitoring for unauthorized access or changes

Always test in a non-production environment first!
