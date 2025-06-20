# 🔄 AutoVlanSwitch - Automated VLAN Switching Tool

[![GitHub release](https://img.shields.io/github/release/abedhossainn/AutoVlanSwitch.svg)](https://github.com/abedhossainn/AutoVlanSwitch/releases)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> **Automated VLAN switching for Cisco switches with secure credential management and Windows service integration**

A professional-grade Windows application that automatically cycles through VLAN configurations on Cisco switches at scheduled intervals. Perfect for testing network segmentation, security scenarios, or automated network topology changes.

## ✨ Key Features

### 🚀 **Easy Deployment**
- **One-Click Installation** - Run `build_secure.bat` to create standalone executables
- **No Python Required on Target** - Fully portable application with bundled dependencies
- **Windows Service Integration** - Runs automatically in the background
- **GUI Configuration** - User-friendly interface for all settings

### 🔒 **Enterprise Security**
- **Windows Credential Manager Integration** - Secure password storage using OS encryption
- **Service Account Support** - Run with dedicated user accounts following least privilege principle
- **Domain Authentication** - Full support for Active Directory environments
- **Audit Trail** - Comprehensive logging for security compliance

### 🖥️ **Modern Interface**
- **Real-Time Monitoring** - Live status updates and activity logs
- **Connection Testing** - Validate settings before deployment
- **Error Handling** - Clear error messages and troubleshooting guidance
- **Status Dashboard** - Current VLAN, next switch time, and service status

### 🔧 **Flexible Configuration**
- **Multiple VLAN Support** - Cycle through unlimited VLAN configurations
- **Custom Intervals** - Configure switching frequency from seconds to hours
- **Switch Compatibility** - Works with Cisco switches via SSH/Telnet
- **Backup & Restore** - Export/import configurations for easy deployment

## 🚀 Quick Start

### Option 1: Standalone Executable (Recommended)
```bash
# 1. Download or clone the repository
git clone https://github.com/abedhossainn/AutoVlanSwitch.git
cd AutoVlanSwitch

# 2. Build the application
build_secure.bat

# 3. Run the GUI
dist\SecureVLANSwitcher\SecureVLANSwitcherGUI.exe
```

### Option 2: Python Environment
```bash
# 1. Clone the repository
git clone https://github.com/abedhossainn/AutoVlanSwitch.git
cd AutoVlanSwitch

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the GUI
python secure_vlan_gui.py
```

## 📋 System Requirements

| Component | Requirement |
|-----------|-------------|
| **Operating System** | Windows 10/11, Windows Server 2019/2022 |
| **Python** | 3.8+ (only for development/source) |
| **Privileges** | Administrator rights for service installation |
| **Network** | SSH/Telnet access to Cisco switches |
| **Memory** | 50MB RAM per service instance |
| **Storage** | 10MB disk space |

## 🔧 Configuration

### Basic Setup
1. **Switch Connection**
   - IP Address: `192.168.1.1`
   - Username: `admin`
   - Password: `your_password`
   - Enable Password: `enable_password`

2. **Interface Configuration**
   - Interface: `GigabitEthernet0/1`
   - VLANs: `10,20,30,40` (comma-separated)
   - Switch Interval: `5` minutes

3. **Security Options**
   - ✅ Store passwords securely (recommended)
   - ✅ Run as dedicated service account
   - ✅ Enable audit logging

### Advanced Configuration
```json
{
  "switch_ip": "192.168.1.1",
  "username": "network_admin",
  "interface": "GigabitEthernet0/1",
  "vlans": "10,20,30,40,50",
  "switch_interval_minutes": 5,
  "use_secure_storage": true,
  "service_user": "DOMAIN\\vlan_service",
  "enable_logging": true
}
```

## 📸 Screenshots

### Main Interface
![Main GUI](screenshots/main_gui.png)
*Configuration panel with real-time activity monitoring*

### Service Status
![Service Status](screenshots/service_status.png)
*Live service status, timer, and switching logs*

## 🛠️ Usage Scenarios

### 🧪 **Network Testing**
- **Security Testing** - Simulate network segmentation changes
- **Performance Testing** - Test application behavior across VLANs
- **Failover Testing** - Automated network topology changes

### 🏢 **Enterprise Environments**
- **Compliance Testing** - Automated security posture validation
- **Training Environments** - Dynamic lab configurations
- **Incident Response** - Rapid network isolation capabilities

### 🔬 **Development & Research**
- **IoT Testing** - Device behavior across network segments
- **Protocol Analysis** - Network protocol testing scenarios
- **Automation Research** - Network orchestration studies

## 📁 Project Structure

```
AutoVlanSwitch/
├── 🎮 Core Application
│   ├── secure_vlan_gui.py           # Main GUI application
│   ├── secure_vlan_switcher.py     # VLAN switching logic
│   ├── windows_service.py          # Windows service wrapper
│   └── vlan_switcher_service.py    # Service compatibility layer
├── ⚙️ Configuration
│   ├── config.json                 # Runtime configuration
│   ├── config_template.json        # Configuration template
│   └── requirements.txt            # Python dependencies
├── 🏗️ Build & Deploy
│   ├── build_secure.bat            # Build standalone executable
│   └── SecureVLANSwitcher.spec     # PyInstaller build config
├── 📚 Documentation
│   ├── README.md                   # This file
│   ├── README_SECURE.md            # Detailed usage guide
│   ├── SECURITY_FEATURES.md        # Security implementation details
│   └── CLEANUP_SUMMARY.md          # Project cleanup documentation
└── 🎯 Output
    └── dist/SecureVLANSwitcher/    # Built executable (after build)
```

## 🔐 Security Features

### Credential Protection
- **Windows Keyring** - OS-level encrypted credential storage
- **Service Accounts** - Dedicated user accounts with minimal privileges
- **Domain Integration** - Active Directory authentication support
- **Audit Logging** - Complete activity tracking for compliance

### Network Security
- **Encrypted Connections** - SSH-based switch communication
- **Connection Validation** - Pre-deployment connectivity testing
- **Error Isolation** - Prevents credential leakage in error messages
- **Session Management** - Secure connection lifecycle management

### Operational Security
- **Principle of Least Privilege** - Minimal required permissions
- **Secure Configuration** - Sensitive data excluded from config files
- **Monitoring Integration** - Windows Event Log integration
- **Backup Security** - Secure configuration export/import

## 🚨 Troubleshooting

### Common Issues

#### Installation Problems
```bash
# "Access Denied" during service installation
# Solution: Run as Administrator
Right-click → "Run as Administrator"

# "Python not found" error  
# Solution: Install Python 3.8+ or use standalone executable
```

#### Connection Issues
```bash
# "Connection Failed" when testing
1. Verify switch IP and network connectivity
2. Check SSH/Telnet credentials
3. Validate interface name format
4. Review firewall settings
```

#### Service Issues
```bash
# Service won't start
1. Check Windows Event Viewer
2. Verify service user credentials  
3. Validate config.json format
4. Review logs/vlan_switcher.log
```

### Log Files
- **Application Logs**: `logs/vlan_switcher.log`
- **Windows Events**: Event Viewer → Application
- **Service Status**: Real-time in GUI activity panel

## 🔄 Deployment Options

### Single Computer Deployment
1. Build executable using `build_secure.bat`
2. Copy `dist/SecureVLANSwitcher/` folder to target
3. Run `SecureVLANSwitcherGUI.exe` as Administrator
4. Configure and install service

### Enterprise Deployment
1. Build executable on development machine
2. Create deployment package with configurations
3. Use Group Policy or SCCM for distribution
4. Automate service installation via scripts

### Development Deployment
1. Clone repository on target machine
2. Install Python dependencies
3. Run from source for development/testing
4. Use IDE integration for debugging

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Setup
```bash
git clone https://github.com/abedhossainn/AutoVlanSwitch.git
cd AutoVlanSwitch
pip install -r requirements.txt
python secure_vlan_gui.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Cisco** - For comprehensive switch documentation
- **Python Community** - For excellent networking libraries
- **Microsoft** - For Windows Service API documentation
- **PyInstaller** - For executable packaging capabilities

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/abedhossainn/AutoVlanSwitch/issues)
- **Discussions**: [GitHub Discussions](https://github.com/abedhossainn/AutoVlanSwitch/discussions)
- **Documentation**: [Wiki](https://github.com/abedhossainn/AutoVlanSwitch/wiki)

## 🔗 Related Projects

- [Cisco Network Automation](https://github.com/topics/cisco-automation)
- [Network Testing Tools](https://github.com/topics/network-testing)
- [Windows Service Management](https://github.com/topics/windows-service)

---

<div align="center">

**⭐ Star this repository if you find it useful!**

[Report Bug](https://github.com/abedhossainn/AutoVlanSwitch/issues) • [Request Feature](https://github.com/abedhossainn/AutoVlanSwitch/issues) • [Documentation](https://github.com/abedhossainn/AutoVlanSwitch/wiki)

</div>
