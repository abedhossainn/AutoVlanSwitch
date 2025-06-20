@echo off
echo Building Secure VLAN Switcher Executable...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Install/update required packages
echo Installing required packages...
pip install -r requirements.txt

REM Clean previous build
echo Cleaning previous build...
if exist "build" rmdir /s /q "build"
if exist "dist\SecureVLANSwitcher" rmdir /s /q "dist\SecureVLANSwitcher"

REM Build executable
echo.
echo Building executable with PyInstaller...
pyinstaller SecureVLANSwitcher.spec

REM Check if build was successful
if exist "dist\SecureVLANSwitcher\SecureVLANSwitcherGUI.exe" (
    echo.
    echo ========================================
    echo BUILD SUCCESSFUL!
    echo ========================================
    echo.
    echo Files created in dist\SecureVLANSwitcher\:
    echo   - SecureVLANSwitcherGUI.exe     ^(GUI Application^)
    echo   - SecureVLANSwitcherService.exe ^(Service Application^)
    echo   - config_template.json          ^(Configuration Template^)
    echo   - SECURITY_FEATURES.md          ^(Documentation^)
    echo.
    
    REM Copy additional files
    echo Copying additional files...
    copy "run_secure_gui.bat" "dist\SecureVLANSwitcher\"
    copy "requirements.txt" "dist\SecureVLANSwitcher\"
    
    REM Create logs directory
    if not exist "dist\SecureVLANSwitcher\logs" mkdir "dist\SecureVLANSwitcher\logs"
    
    echo.
    echo Additional files copied:
    echo   - run_secure_gui.bat           ^(Startup Script^)
    echo   - requirements.txt             ^(Dependencies^)
    echo   - logs\                        ^(Log Directory^)
    echo.
    echo To distribute the application:
    echo 1. Copy the entire 'dist\SecureVLANSwitcher' folder
    echo 2. On target machine, run 'run_secure_gui.bat'
    echo 3. Or directly run 'SecureVLANSwitcherGUI.exe'
    echo.
) else (
    echo.
    echo BUILD FAILED!
    echo Check the error messages above.
    echo.
)

pause
