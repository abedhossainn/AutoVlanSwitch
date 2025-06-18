# Files to Copy to Target Computer

## For STANDALONE EXECUTABLE Deployment (Recommended):

Copy the entire `dist\portable\` folder to your target computer. This folder should contain:

### ✅ **Required Files:**
```
dist\portable\
├── VLANSwitcherService.exe     # Windows service executable
├── VLANSwitcherConsole.exe     # Console mode executable  
├── VLANSwitcherGUI.exe         # GUI configuration executable
├── config.json                 # Configuration file
├── run_gui.bat                 # Start GUI (double-click this)
├── run_console.bat             # Test in console mode
├── install_service.bat         # Install Windows service (Run as Admin)
├── uninstall_service.bat       # Remove Windows service (Run as Admin)
├── README.txt                  # Quick start instructions
└── logs\                       # Logs directory (created automatically)
```

### 🎯 **What You Actually Need to Copy:**
**JUST COPY THE ENTIRE `dist\portable\` FOLDER**

---

## For PYTHON-BASED Deployment (If you prefer):

Copy the entire `VLANSwitcher_Portable\` folder (created by `create_portable.bat`):

### ✅ **Required Files:**
```
VLANSwitcher_Portable\
├── vlan_switcher_service.py    # Main service script
├── vlan_switcher_gui.py        # GUI application
├── windows_service.py          # Windows service wrapper
├── config.json                 # Configuration file
├── requirements.txt            # Python dependencies
├── run_gui.bat                 # Start GUI
├── run_console.bat             # Console mode
├── install_service.bat         # Install service (Run as Admin)
├── uninstall_service.bat       # Remove service (Run as Admin)
├── install_dependencies.bat    # Install Python packages (Run as Admin)
├── SETUP_INSTRUCTIONS.md       # Setup guide
├── README.md                   # Documentation
└── logs\                       # Logs directory
```

---

## 🚀 **Quick Deployment Steps:**

### **Option 1: Executable (No Python needed on target)** ⭐ **RECOMMENDED**
1. Copy entire `dist\portable\` folder to target computer
2. On target computer: Double-click `run_gui.bat` 
3. Configure your settings and save
4. Right-click `install_service.bat` → "Run as Administrator"

### **Option 2: Python-based (Requires Python on target)**
1. Copy entire `VLANSwitcher_Portable\` folder to target computer  
2. On target computer: Install Python from python.org
3. Right-click `install_dependencies.bat` → "Run as Administrator"
4. Double-click `run_gui.bat`
5. Configure your settings and save
6. Right-click `install_service.bat` → "Run as Administrator"

---

## ❌ **Files You DON'T Need to Copy:**
- `.venv\` folder (virtual environment)
- `build\` folder (build artifacts)  
- `__pycache__\` folders (Python cache)
- `.pyc` files (compiled Python)
- `switch_vlan_HC.py` (original script - backup only)
- Development batch files (`build_exe.bat`, `create_portable.bat`)
- PyInstaller spec files (`.spec`)

---

## 📝 **Summary:**
**For easiest deployment: Copy just the `dist\portable\` folder!**

This contains everything needed to run on the target computer without any Python installation required.
