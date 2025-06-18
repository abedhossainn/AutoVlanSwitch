@echo off
echo ================================================
echo Building VLAN Switcher Service
echo ================================================
echo.

echo Cleaning previous builds...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist *.spec del *.spec

echo.
echo Building executable...
pyinstaller --onefile --add-data "config.json;." --hidden-import "win32timezone" --name "VLANSwitcher" vlan_switcher.py

if %errorlevel% equ 0 (
    echo.
    echo ================================================
    echo Build completed successfully!
    echo ================================================
    echo.
    echo Creating deployment folder...
    
    if not exist "dist\VLANSwitcher" mkdir "dist\VLANSwitcher"
    
    echo Copying files...
    copy "dist\VLANSwitcher.exe" "dist\VLANSwitcher\"
    copy "config.json" "dist\VLANSwitcher\"
    
    if not exist "dist\VLANSwitcher\logs" mkdir "dist\VLANSwitcher\logs"
    
    echo Creating installation batch file...
    echo @echo off > "dist\VLANSwitcher\install.bat"
    echo echo Installing VLAN Switcher Service... >> "dist\VLANSwitcher\install.bat"
    echo echo. >> "dist\VLANSwitcher\install.bat"
    echo net session ^>nul 2^>^&1 >> "dist\VLANSwitcher\install.bat"
    echo if %%errorlevel%% neq 0 ^( >> "dist\VLANSwitcher\install.bat"
    echo     echo ERROR: Administrator privileges required! >> "dist\VLANSwitcher\install.bat"
    echo     echo Right-click this file and select 'Run as Administrator' >> "dist\VLANSwitcher\install.bat"
    echo     pause >> "dist\VLANSwitcher\install.bat"
    echo     exit /b 1 >> "dist\VLANSwitcher\install.bat"
    echo ^) >> "dist\VLANSwitcher\install.bat"
    echo VLANSwitcher.exe install >> "dist\VLANSwitcher\install.bat"
    echo VLANSwitcher.exe start >> "dist\VLANSwitcher\install.bat"
    echo echo Service installed and started! >> "dist\VLANSwitcher\install.bat"
    echo pause >> "dist\VLANSwitcher\install.bat"
    
    echo Creating uninstall batch file...
    echo @echo off > "dist\VLANSwitcher\uninstall.bat"
    echo echo Removing VLAN Switcher Service... >> "dist\VLANSwitcher\uninstall.bat"
    echo VLANSwitcher.exe stop >> "dist\VLANSwitcher\uninstall.bat"
    echo VLANSwitcher.exe remove >> "dist\VLANSwitcher\uninstall.bat"
    echo echo Service removed! >> "dist\VLANSwitcher\uninstall.bat"
    echo pause >> "dist\VLANSwitcher\uninstall.bat"
    
    echo Creating test batch file...
    echo @echo off > "dist\VLANSwitcher\test.bat"
    echo echo Testing VLAN Switcher in debug mode... >> "dist\VLANSwitcher\test.bat"
    echo echo Press Ctrl+C to stop >> "dist\VLANSwitcher\test.bat"
    echo echo. >> "dist\VLANSwitcher\test.bat"
    echo VLANSwitcher.exe debug >> "dist\VLANSwitcher\test.bat"
    
    echo Creating README...
    echo VLAN Switcher Service > "dist\VLANSwitcher\README.txt"
    echo ==================== >> "dist\VLANSwitcher\README.txt"
    echo. >> "dist\VLANSwitcher\README.txt"
    echo 1. Edit config.json with your switch details >> "dist\VLANSwitcher\README.txt"
    echo 2. Right-click install.bat and 'Run as Administrator' >> "dist\VLANSwitcher\README.txt"
    echo 3. Service will start automatically >> "dist\VLANSwitcher\README.txt"
    echo. >> "dist\VLANSwitcher\README.txt"
    echo Files: >> "dist\VLANSwitcher\README.txt"
    echo - VLANSwitcher.exe: Main service executable >> "dist\VLANSwitcher\README.txt"
    echo - config.json: Configuration file >> "dist\VLANSwitcher\README.txt"
    echo - install.bat: Install service (run as admin^) >> "dist\VLANSwitcher\README.txt"
    echo - uninstall.bat: Remove service >> "dist\VLANSwitcher\README.txt"
    echo - test.bat: Test in debug mode >> "dist\VLANSwitcher\README.txt"
    echo - logs/: Service log files >> "dist\VLANSwitcher\README.txt"
    
    echo.
    echo ================================================
    echo Deployment ready: dist\VLANSwitcher\
    echo ================================================
    echo.
    dir "dist\VLANSwitcher"
    echo.
) else (
    echo.
    echo ================================================
    echo Build failed!
    echo ================================================
)

pause
