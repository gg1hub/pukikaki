#!/usr/bin/env python3
"""
Snake Game Build Script
Creates an executable (.exe) file from the Snake game using PyInstaller.
"""

import subprocess
import sys
import os
import shutil
import platform

def check_pyinstaller():
    """Check if PyInstaller is available"""
    try:
        import PyInstaller
        print("✅ PyInstaller is available")
        return True
    except ImportError:
        print("❌ PyInstaller not found!")
        print("Installing PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✅ PyInstaller installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install PyInstaller")
            return False

def create_spec_file():
    """Create a PyInstaller spec file for better control"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('game', 'game'),
    ],
    hiddenimports=[
        'pygame',
        'pygame.mixer',
        'pygame.math',
        'pygame.sndarray'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SnakeGame',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None
)
'''

    with open('snake_game.spec', 'w') as f:
        f.write(spec_content)
    
    print("✅ Created PyInstaller spec file")

def build_executable():
    """Build the executable using PyInstaller"""
    print("🔨 Building executable...")
    
    # Build command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",              # Single executable file
        "--windowed",             # No console window (GUI only)
        "--name", "SnakeGame",    # Output filename
        "--clean",                # Clean cache and temporary files
        "main.py"
    ]
    
    # Add icon if available
    if os.path.exists("assets/icon.ico"):
        cmd.extend(["--icon", "assets/icon.ico"])
    
    try:
        # Run PyInstaller
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Build completed successfully!")
            return True
        else:
            print("❌ Build failed!")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Build failed with exception: {e}")
        return False

def create_icon():
    """Create a simple icon file if it doesn't exist"""
    icon_dir = "assets"
    if not os.path.exists(icon_dir):
        os.makedirs(icon_dir)
    
    # Skip icon creation for now - would require PIL/Pillow
    print("ℹ️  No icon file found, building without custom icon")

def clean_build_files():
    """Clean up build artifacts"""
    build_dirs = ["build", "__pycache__"]
    files_to_remove = ["snake_game.spec"]
    
    for directory in build_dirs:
        if os.path.exists(directory):
            shutil.rmtree(directory)
            print(f"🧹 Removed {directory}/")
    
    for pattern in ["*.pyc", "*.pyo"]:
        for root, dirs, files in os.walk("."):
            for file in files:
                if file.endswith(pattern[1:]):  # Remove the *
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
    
    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)
            print(f"🧹 Removed {file}")

def find_executable():
    """Find the built executable"""
    dist_dir = "dist"
    if not os.path.exists(dist_dir):
        return None
    
    # Look for the executable
    exe_name = "SnakeGame.exe" if platform.system() == "Windows" else "SnakeGame"
    exe_path = os.path.join(dist_dir, exe_name)
    
    if os.path.exists(exe_path):
        return exe_path
    
    # Fallback: look for any executable in dist
    for file in os.listdir(dist_dir):
        file_path = os.path.join(dist_dir, file)
        if os.path.isfile(file_path):
            return file_path
    
    return None

def test_executable():
    """Test the built executable"""
    exe_path = find_executable()
    if not exe_path:
        print("❌ Could not find built executable!")
        return False
    
    print(f"🧪 Testing executable: {exe_path}")
    
    # Get file size
    file_size = os.path.getsize(exe_path)
    size_mb = file_size / (1024 * 1024)
    print(f"📊 Executable size: {size_mb:.1f} MB")
    
    # Test if it's executable
    if not os.access(exe_path, os.X_OK):
        try:
            os.chmod(exe_path, 0o755)
            print("✅ Made file executable")
        except OSError:
            print("❌ Could not make file executable")
            return False
    
    print("✅ Executable appears to be built correctly")
    return True

def create_installer():
    """Create a simple batch installer (Windows only)"""
    if platform.system() != "Windows":
        return
    
    exe_path = find_executable()
    if not exe_path:
        return
    
    installer_content = f'''@echo off
echo Installing Snake Game...
echo.

if not exist "%USERPROFILE%\\Desktop\\Games" mkdir "%USERPROFILE%\\Desktop\\Games"
copy "{os.path.basename(exe_path)}" "%USERPROFILE%\\Desktop\\Games\\" >nul

echo Creating desktop shortcut...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\Snake Game.lnk'); $Shortcut.TargetPath = '%USERPROFILE%\\Desktop\\Games\\{os.path.basename(exe_path)}'; $Shortcut.Save()"

echo.
echo ✅ Snake Game installed successfully!
echo You can now run it from your Desktop or Games folder.
echo.
pause
'''

    with open("install_game.bat", "w") as f:
        f.write(installer_content)
    
    print("✅ Created Windows installer batch file")

def print_completion_message():
    """Print build completion message"""
    exe_path = find_executable()
    if not exe_path:
        return
    
    print("\n" + "=" * 60)
    print("🎉 BUILD COMPLETE! 🎉")
    print("=" * 60)
    print()
    print(f"Executable created: {exe_path}")
    
    file_size = os.path.getsize(exe_path)
    size_mb = file_size / (1024 * 1024)
    print(f"File size: {size_mb:.1f} MB")
    print()
    
    print("The executable is ready to distribute!")
    print("It includes all dependencies and can run on any compatible system.")
    print()
    
    if platform.system() == "Windows" and os.path.exists("install_game.bat"):
        print("Windows installer created: install_game.bat")
        print("Run this to install the game to Desktop/Games folder.")
        print()
    
    print("To run the game:")
    print(f"  ./{os.path.basename(exe_path)}")

def main():
    """Main build function"""
    print("=" * 60)
    print("🔨 SNAKE GAME BUILD SCRIPT 🔨")
    print("=" * 60)
    print("Building executable from Snake Game source...")
    print()
    
    # Check requirements
    if not check_pyinstaller():
        return 1
    
    # Create icon if needed
    create_icon()
    
    # Build executable
    if not build_executable():
        return 1
    
    print()
    
    # Test the executable
    if not test_executable():
        print("⚠️  Warning: Executable test failed, but build might still work")
    
    # Create installer for Windows
    create_installer()
    
    # Show completion message
    print_completion_message()
    
    # Ask about cleanup
    try:
        response = input("\nClean up build files? (Y/n): ").strip().lower()
        if response != 'n':
            clean_build_files()
            print("🧹 Build files cleaned up")
    except KeyboardInterrupt:
        print()
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nBuild cancelled by user.")
        sys.exit(1)