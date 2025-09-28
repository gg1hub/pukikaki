#!/usr/bin/env python3
"""
Snake Game Auto-Installer
Automatically installs all required dependencies for the Snake game.
"""

import subprocess
import sys
import os
import platform

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 6):
        print("❌ Python 3.6 or higher is required!")
        print(f"Current version: {sys.version}")
        return False
    
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_pip():
    """Check if pip is available"""
    try:
        import pip
        print("✅ pip is available")
        return True
    except ImportError:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "--version"], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("✅ pip is available")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ pip is not available!")
            print("Please install pip first.")
            return False

def install_package(package):
    """Install a package using pip"""
    try:
        print(f"📦 Installing {package}...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", package, "--user"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        print(f"✅ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}")
        if e.stderr:
            print(f"Error: {e.stderr.decode()}")
        return False

def check_package_installed(package_name):
    """Check if a package is already installed"""
    try:
        __import__(package_name)
        print(f"✅ {package_name} is already installed")
        return True
    except ImportError:
        return False

def install_dependencies():
    """Install all required dependencies"""
    print("🎮 Installing Snake Game dependencies...\n")
    
    # Read requirements
    requirements_file = "requirements.txt"
    if not os.path.exists(requirements_file):
        print(f"❌ {requirements_file} not found!")
        return False
    
    with open(requirements_file, 'r') as f:
        packages = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    success = True
    
    for package_line in packages:
        # Extract package name (remove version specifiers)
        package_name = package_line.split('>=')[0].split('==')[0].split('<')[0].split('>')[0]
        
        if not check_package_installed(package_name):
            if not install_package(package_line):
                success = False
    
    return success

def create_desktop_shortcut():
    """Create a desktop shortcut (Windows only)"""
    if platform.system() != "Windows":
        return
    
    try:
        import winshell
        from win32com.client import Dispatch
        
        desktop = winshell.desktop()
        path = os.path.join(desktop, "Snake Game.lnk")
        target = os.path.join(os.getcwd(), "main.py")
        wDir = os.getcwd()
        icon = target
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = sys.executable
        shortcut.Arguments = f'"{target}"'
        shortcut.WorkingDirectory = wDir
        shortcut.IconLocation = icon
        shortcut.save()
        
        print("✅ Desktop shortcut created")
        
    except ImportError:
        print("ℹ️  Could not create desktop shortcut (winshell not available)")
    except Exception as e:
        print(f"ℹ️  Could not create desktop shortcut: {e}")

def test_installation():
    """Test if the game can be imported and basic functionality works"""
    print("\n🧪 Testing installation...")
    
    try:
        import pygame
        pygame.init()
        pygame.quit()
        print("✅ Pygame test passed")
        
        # Test game imports
        sys.path.insert(0, os.getcwd())
        from game.config import SCREEN_WIDTH, SCREEN_HEIGHT
        from game.snake import Snake, GameEngine
        from game.menu import MenuManager
        from game.score_manager import ScoreManager
        from game.sound_manager import SoundManager
        
        print("✅ Game modules import successfully")
        return True
        
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def print_banner():
    """Print installation banner"""
    print("=" * 60)
    print("🐍 SNAKE GAME AUTO-INSTALLER 🐍")
    print("=" * 60)
    print("This installer will set up everything needed to run Snake Game.")
    print()

def print_completion_message():
    """Print completion message"""
    print("\n" + "=" * 60)
    print("🎉 INSTALLATION COMPLETE! 🎉")
    print("=" * 60)
    print()
    print("To play the game, run:")
    print("  python main.py")
    print()
    print("Or double-click on main.py")
    print()
    print("Game controls:")
    print("  • Arrow keys or WASD - Move snake")
    print("  • Space - Pause/Restart")
    print("  • ESC - Main menu")
    print()
    print("Have fun playing Snake Game! 🐍")

def main():
    """Main installer function"""
    print_banner()
    
    # Check system requirements
    if not check_python_version():
        return 1
    
    if not check_pip():
        return 1
    
    print()
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Some dependencies failed to install!")
        print("Please check the error messages above.")
        return 1
    
    print()
    
    # Test installation
    if not test_installation():
        print("\n❌ Installation test failed!")
        print("There might be an issue with the installation.")
        return 1
    
    # Create desktop shortcut on Windows
    create_desktop_shortcut()
    
    # Print completion message
    print_completion_message()
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        if exit_code == 0:
            # Ask if user wants to run the game now
            try:
                response = input("\nWould you like to run the game now? (y/N): ").strip().lower()
                if response in ['y', 'yes']:
                    print("\n🎮 Starting Snake Game...")
                    subprocess.call([sys.executable, "main.py"])
            except KeyboardInterrupt:
                print("\nGoodbye!")
        
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nInstallation cancelled by user.")
        sys.exit(1)