# VLAN Switcher Service

Automatically switches VLANs on Cisco switches at scheduled intervals.

## Features

- Automatically rotates through a predefined list of VLANs
- Configurable switch credentials and settings via JSON file
- Can run as a Windows service or console application
- Comprehensive logging
- Executable generation for easy deployment

## Files

- `vlan_switcher_service.py` - Main service application
- `vlan_switcher_gui.py` - GUI configuration interface
- `windows_service.py` - Windows service wrapper
- `config.json` - Configuration file
- `switch_vlan_HC.py` - Original script (backup)
- `requirements.txt` - Python dependencies

## Setup

### 1. Configuration

Edit `config.json` with your switch details:

```json
{
    "switch_ip": "192.168.1.1",
    "username": "admin",
    "password": "password",
    "enable_password": "enable_password",
    "interface": "1/0/10",
    "schedule_minutes": 1,
    "vlans": [
        "811", "813", "814", "815", "816", "817", "820", "821", "822", "823",
        "824", "825", "826", "827", "828", "829", "830", "831", "832", "833",
        "834", "835"
    ]
}
```

### 2. Running Options

#### Option A: GUI Configuration (Recommended)
```batch
run_gui.bat
```
**Features:**
- Interactive configuration form
- Test switch connection
- Install/manage Windows service
- Build executables
- Real-time status monitoring

#### Option B: Console Mode (for testing)
```batch
run_console.bat
```

#### Option C: Windows Service
```batch
# Install and start service (run as Administrator)
install_service.bat

# Uninstall service (run as Administrator)
uninstall_service.bat
```

#### Option D: Executable
```batch
# Build executables
build_exe.bat

# This creates:
# - dist/VLANSwitcherService.exe (service version)
# - dist/VLANSwitcherConsole.exe (console version)
# - dist/VLANSwitcherGUI.exe (GUI configuration)
```

## Deployment to Another Computer

### Option 1: Portable Python Version

1. **Create portable package**: Run `create_portable.bat`
2. **Copy folder**: Copy the `VLANSwitcher_Portable` folder to target computer
3. **Install Python** on target computer (if not installed):
   - Download from https://python.org
   - Check "Add Python to PATH" during installation
4. **Install dependencies**: Run `install_dependencies.bat` (as Administrator)
5. **Configure**: Run `run_gui.bat` and configure your settings
6. **Deploy**: Run `install_service.bat` (as Administrator) or `run_console.bat`

### Option 2: Standalone Executable (No Python Required)

1. **Build executables**: Run `build_exe.bat`
2. **Copy folder**: Copy the `dist\portable` folder to target computer
3. **Configure**: Double-click `run_gui.bat` to configure settings
4. **Deploy**: Run `install_service.bat` (as Administrator) or `run_console.bat`

**✅ Recommended: Use Option 2 for easiest deployment**

## Installation Steps

### For Easy Setup (Recommended):

1. **Run GUI**: Execute `run_gui.bat`
2. **Configure**: Fill in all the fields in the GUI
3. **Test**: Click "Test Connection" to verify settings
4. **Deploy**: Choose your deployment option:
   - **Console Mode**: Click "Run Console Mode" for testing
   - **Windows Service**: Click "Install Service" then "Start Service"
   - **Executable**: Click "Build Executable" for standalone deployment

### For Development/Testing:

1. **Clone/Download** the project files
2. **Edit** `config.json` with your switch credentials
3. **Run** `run_console.bat` to test

### For Production Deployment:

1. **Build executable**: Run `build_exe.bat`
2. **Copy files** to target machine:
   - `dist/VLANSwitcherService.exe`
   - `config.json`
3. **Install as service**:
   ```cmd
   VLANSwitcherService.exe install
   VLANSwitcherService.exe start
   ```

## Service Management

### Manual Service Commands:
```cmd
# Install service
VLANSwitcherService.exe install

# Start service
VLANSwitcherService.exe start

# Stop service
VLANSwitcherService.exe stop

# Remove service
VLANSwitcherService.exe remove

# Debug mode
VLANSwitcherService.exe debug
```

### Windows Services Manager:
1. Open `services.msc`
2. Find "VLAN Switcher Service"
3. Right-click to Start/Stop/Configure

## Logging

Logs are written to the `logs/` directory:
- `vlan_switcher.log` - Application logs
- `service.log` - Service-specific logs

## Configuration Options

| Setting | Description | Example |
|---------|-------------|---------|
| `switch_ip` | IP address of the Cisco switch | `"192.168.1.1"` |
| `username` | Switch username | `"admin"` |
| `password` | Switch password | `"password"` |
| `enable_password` | Enable mode password | `"enable_pass"` |
| `interface` | Interface to configure | `"1/0/10"` |
| `schedule_minutes` | Interval between VLAN changes | `1` |
| `vlans` | List of VLANs to rotate through | `["811", "813", ...]` |

## Troubleshooting

### Common Issues:

1. **Service won't start**: Check logs in `logs/service.log`
2. **Can't connect to switch**: Verify IP, credentials, and network connectivity
3. **Permission errors**: Run as Administrator when installing/managing service

### Testing Connection:
Run the console version first to test connectivity:
```batch
run_console.bat
```

### Viewing Logs:
Check the `logs/` folder for detailed error messages.

## Security Notes

- Store `config.json` securely as it contains passwords
- Consider using encrypted credentials for production
- Ensure switch credentials have minimal required privileges
- Run service with a dedicated service account

## Requirements

- Windows 10/Server 2016 or later
- Network access to Cisco switch
- Administrator privileges (for service installation)
