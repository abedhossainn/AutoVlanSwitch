# Secure VLAN Switcher - Enhanced GUI Application

## 🔒 Security-Enhanced VLAN Management

This is an upgraded version of the VLAN Switcher application featuring advanced security capabilities, improved user interface, and robust Windows service integration.

## ✨ New Features

### 🛡️ Security Enhancements
- **Secure Credential Storage**: Uses Windows Credential Manager via keyring library
- **Service User Configuration**: Run as specific Windows user accounts
- **Credential Validation**: Built-in user authentication testing
- **Password Protection**: Option to store sensitive data outside configuration files

### 🖥️ Enhanced GUI
- **Modern Interface**: Improved user experience with better organization
- **Real-time Status**: Live feedback for all operations
- **Secure Storage Options**: Checkboxes to enable secure password storage
- **User Validation**: Test service account credentials before installation

### 🔧 Service Management
- **Multiple Run Modes**: Local System or specific user account
- **Domain Support**: Works with domain and local user accounts
- **Enhanced Logging**: Comprehensive logging with security event tracking
- **Automatic Credential Retrieval**: Seamlessly loads stored credentials

## 📋 Prerequisites

- **Operating System**: Windows 10/11 or Windows Server 2019/2022
- **Python**: Version 3.8 or higher
- **Privileges**: Administrator rights for service installation
- **Network**: Access to target Cisco switch via SSH/Telnet

## 🚀 Quick Start

### Method 1: Using the Startup Script (Recommended)
1. **Download**: Get all files to a folder on your computer
2. **Run**: Double-click `run_secure_gui.bat`
3. **Configure**: Fill in your switch and credential details
4. **Secure**: Check "Store securely" for passwords
5. **Test**: Click "Test Connection" to verify settings
6. **Install**: Click "Install Service" (requires Admin rights)
7. **Start**: Click "Start Service"

### Method 2: Manual Python Execution
```bash
# Install dependencies
pip install -r requirements.txt

# Launch GUI
python secure_vlan_gui.py
```

### Method 3: Build Executable
```bash
# Build standalone executable
build_secure.bat

# Run from dist folder
dist\SecureVLANSwitcher\SecureVLANSwitcherGUI.exe
```

## 🔧 Configuration

### Switch Settings
| Field | Description | Example |
|-------|-------------|---------|
| Switch IP | IP address of your switch | `192.168.1.1` |
| Username | Switch login username | `admin` |
| Password | Switch password | `secretpass` |
| Enable Password | Privileged mode password | `enablepass` |
| Interface | Interface to configure | `GigabitEthernet0/1` |
| Schedule | Minutes between switches | `5` |

### VLAN Configuration
- Enter one VLAN ID per line in the text area
- VLANs will be switched in the order listed
- System cycles back to first VLAN after the last one

### Service User Options

#### Local System (Default)
- ✅ Maximum compatibility
- ✅ No credential management needed
- ❌ Runs with elevated privileges

#### Specific User Account
- ✅ Principle of least privilege
- ✅ Centralized credential management
- ✅ Domain integration support
- ❌ Requires credential configuration

**Username Formats:**
- Domain user: `DOMAIN\username`
- Local user: `.\username` or `COMPUTERNAME\username`
- UPN format: `username@domain.com`

## 🔐 Security Features

### Credential Protection
The application provides multiple layers of credential protection:

1. **Windows Keyring Integration**
   - Passwords stored using Windows Credential Manager
   - Encrypted storage with user account binding
   - Automatic retrieval on application start

2. **Secure Configuration**
   - Sensitive data excluded from configuration files when stored securely
   - Clear separation between public and private configuration data

3. **Service Account Security**
   - Support for dedicated service accounts
   - Credential validation before service installation
   - Domain and local account support

### Best Practices Implemented
- ✅ Secure credential storage using OS-provided mechanisms
- ✅ Principle of least privilege for service accounts
- ✅ Input validation and sanitization
- ✅ Comprehensive logging for security monitoring
- ✅ Error handling to prevent information disclosure

## 📊 Usage Modes

### 1. GUI Configuration Mode
Perfect for setup, testing, and management:
- Interactive configuration
- Real-time connection testing
- Service management controls
- Status monitoring

### 2. Debug Mode
Ideal for troubleshooting:
- Console output with detailed logging
- Manual execution for testing
- Real-time VLAN switching observation
- Error diagnosis

### 3. Windows Service Mode
Production deployment:
- Automatic startup with Windows
- Background operation
- Scheduled VLAN switching
- Windows Event Log integration

## 🔍 Troubleshooting

### Common Issues and Solutions

#### Installation Problems
**"Access Denied" during service installation:**
```
Solution: Right-click run_secure_gui.bat → "Run as Administrator"
```

**"Python not found" error:**
```
Solution: Install Python 3.8+ and ensure it's in your PATH
```

#### Connection Issues
**"Connection Failed" when testing:**
```
1. Verify switch IP address and network connectivity
2. Check username/password credentials
3. Ensure switch allows SSH connections
4. Verify interface name format (e.g., GigabitEthernet0/1)
5. Check firewall settings
```

#### Service Issues
**Service won't start:**
```
1. Check Windows Event Viewer → Application logs
2. Verify service user credentials
3. Ensure config.json exists and is valid
4. Check logs\vlan_switcher.log for details
5. Test in debug mode first
```

**Stored credentials not working:**
```
1. Click "Clear Stored Credentials" in GUI
2. Re-enter passwords with "Store securely" checked
3. Verify Windows Credential Manager has entries
4. Check user account permissions
```

### Log Files
- **Service Logs**: `logs\vlan_switcher.log`
- **Windows Events**: Event Viewer → Windows Logs → Application
- **GUI Status**: Real-time display in status area

## 📁 File Structure

```
SecureVLANSwitcher/
├── 🖥️ GUI Application
│   ├── secure_vlan_gui.py              # Enhanced GUI
│   └── run_secure_gui.bat              # Startup script
├── 🔧 Service Components  
│   ├── secure_vlan_switcher.py         # Enhanced service
│   └── SecureVLANSwitcher.spec         # Build specification
├── ⚙️ Configuration
│   ├── config.json                     # Active configuration
│   ├── config_template.json            # Template file
│   └── requirements.txt                # Python dependencies
├── 🏗️ Build Tools
│   └── build_secure.bat                # Build script
├── 📚 Documentation
│   ├── README_SECURE.md                # This file
│   └── SECURITY_FEATURES.md            # Detailed security guide
└── 📊 Runtime
    └── logs\                           # Log files directory
```

## 🔄 Upgrade Path

### From Original Version
1. **Backup**: Save your existing `config.json`
2. **Install**: Download the new secure version
3. **Migrate**: Copy configuration values to new GUI
4. **Secure**: Enable secure storage for passwords
5. **Reinstall**: Remove old service and install new one

### Configuration Migration
The new version automatically loads settings from existing `config.json` files. Simply:
1. Open the new GUI
2. Review loaded settings
3. Enable secure storage options
4. Save configuration

## 🛠️ Advanced Usage

### Custom Scheduling
For complex scheduling beyond simple intervals:
1. Install service with specific user account
2. Create Windows Task Scheduler entry
3. Configure task to run debug mode at specific times
4. Use multiple schedules for different scenarios

### Multiple Switch Management
To manage multiple switches:
1. Create separate folders for each switch
2. Configure each with different settings
3. Install services with unique names
4. Monitor each service independently

### Integration Options
- **Monitoring**: Parse log files for automation
- **APIs**: Trigger via external scripts
- **SIEM**: Monitor Windows Event Logs
- **Network Management**: Integrate with existing tools

## 📈 Performance and Scalability

### Resource Usage
- **Memory**: ~50MB per service instance
- **CPU**: Minimal (only during VLAN switches)
- **Network**: Brief SSH connections only
- **Storage**: <10MB installation

### Scalability
- **Multiple Switches**: Install separate instances
- **High Frequency**: Tested down to 30-second intervals
- **Concurrent Operations**: Each service runs independently

## 🤝 Support and Maintenance

### Regular Maintenance
- **Updates**: Keep Python packages current
- **Monitoring**: Review logs weekly
- **Testing**: Validate configuration changes in debug mode
- **Backup**: Export configurations before changes

### Security Maintenance
- **Credentials**: Rotate passwords regularly
- **Monitoring**: Watch for authentication failures
- **Updates**: Apply security updates promptly
- **Auditing**: Review service account permissions

## 📄 License and Disclaimer

This software is provided for educational and operational use. Users are responsible for:
- Compliance with organizational security policies
- Thorough testing before production deployment
- Secure credential management practices
- Monitoring for unauthorized access

**Always test in a non-production environment first!**

---

## 🔗 Reference Documentation

- [Microsoft CreateProcessWithLogonW API](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-createprocesswithlogonw)
- [Windows Task Scheduler](https://learn.microsoft.com/en-us/windows/win32/taskschd/about-the-task-scheduler)
- [Python Keyring Library](https://pypi.org/project/keyring/)

---

*For detailed security implementation information, see [SECURITY_FEATURES.md](SECURITY_FEATURES.md)*
