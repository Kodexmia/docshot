@echo off
REM DocShot v3.6.2 Build Script for Windows
REM ========================================

echo.
echo ==========================================
echo   DocShot v3.6.2 Build Script
echo   Working folder: %CD%
echo ==========================================
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>NUL
if errorlevel 1 (
    echo PyInstaller not found in this Python environment.
    echo Installing PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo FAILED to install PyInstaller
        pause
        exit /b 1
    )
) else (
    echo PyInstaller already installed.
)

echo.
echo Installing/refreshing DocShot dependencies from requirements.txt...
if exist "requirements.txt" (
    pip install -r requirements.txt
    if errorlevel 1 (
        echo FAILED to install requirements
        pause
        exit /b 1
    )
) else (
    echo WARNING: requirements.txt not found in this folder.
    echo Make sure PyQt6 and other dependencies are installed manually.
)

REM Clean previous builds
echo.
echo Cleaning previous builds...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "DocShot_Portable" rmdir /s /q "DocShot_Portable"
echo Done.
echo.

REM Build with PyInstaller
echo Building DocShot.exe...
echo This may take a few minutes...
echo.

pyinstaller docshot.spec --clean --noconfirm

if errorlevel 1 (
    echo.
    echo ==========================================
    echo   BUILD FAILED!
    echo ==========================================
    echo.
    echo Check the error messages above.
    pause
    exit /b 1
)

REM Check if EXE was created
if not exist "dist\DocShot.exe" (
    echo.
    echo ERROR: DocShot.exe was not created!
    pause
    exit /b 1
)

echo.
echo Build successful!
echo.

REM Create portable folder
echo Creating portable distribution...
mkdir "DocShot_Portable" 2>NUL
copy "dist\DocShot.exe" "DocShot_Portable\" >NUL
if exist "README.md" copy "README.md" "DocShot_Portable\" >NUL
if exist "VERSION" copy "VERSION" "DocShot_Portable\" >NUL

REM Create README for portable version
echo Creating portable README...
(
echo DocShot v3.6.2 - Portable Version
echo ==================================
echo.
echo This is a standalone executable version of DocShot.
echo No installation required!
echo.
echo QUICK START:
echo 1. Double-click DocShot.exe
echo 2. Click "New Session" to start
echo 3. Press Ctrl+Alt+S to capture screenshots
echo 4. Annotate and save your entries
echo.
echo FEATURES:
echo - Screenshot capture with global hotkey
echo - 4 annotation tools ^(arrow, box, pen, text^)
echo - Entry management ^(edit, reorder, delete^)
echo - HTML report export
echo - AI Auto-Fill ^(optional - requires API key^)
echo.
echo For more information, see README.md
echo.
echo Version: 3.6.2
echo Build Date: %date% %time%
) > "DocShot_Portable\PORTABLE_README.txt"

echo Done.
echo.

REM Get file size
for %%A in ("DocShot_Portable\DocShot.exe") do set size=%%~zA
set /a size_mb=size/1048576

echo.
echo ==========================================
echo   BUILD COMPLETE!
echo ==========================================
echo.
echo Location: DocShot_Portable\DocShot.exe
echo Size: %size_mb% MB
echo.
echo To distribute:
echo 1. Zip the DocShot_Portable folder
echo 2. Share DocShot_v3.6.2_Windows.zip
echo.

REM Create distribution ZIP
echo Creating distribution ZIP...
powershell -command "Compress-Archive -Path 'DocShot_Portable\*' -DestinationPath 'DocShot_v3.6.2_Windows.zip' -Force"

if exist "DocShot_v3.6.2_Windows.zip" (
    echo.
    echo ==========================================
    echo   READY TO DISTRIBUTE!
    echo ==========================================
    echo.
    echo File: DocShot_v3.6.2_Windows.zip
    for %%A in ("DocShot_v3.6.2_Windows.zip") do set zip_size=%%~zA
    set /a zip_size_mb=zip_size/1048576
    echo Size: %zip_size_mb% MB
    echo.
    echo This ZIP contains:
    echo - DocShot.exe ^(standalone^)
    echo - README.md
    echo - VERSION
    echo - PORTABLE_README.txt
    echo.
) else (
    echo Warning: Could not create distribution ZIP
    echo You can manually zip the DocShot_Portable folder
)

echo Press any key to open the output folder...
pause >nul
explorer "DocShot_Portable"

echo.
echo Build script completed!
