# Browser Manager for Linux

A comprehensive Python script for managing web browsers on Linux systems. This tool provides an interactive terminal interface to install, uninstall, and manage various web browsers.

## 🌟 Features

- Detects and manages multiple web browsers:
  - Mozilla Firefox
  - Google Chrome
  - Chromium
  - Tor Browser
  - Brave Browser
  - Vivaldi
  - Opera
  - Microsoft Edge
  - Falkon
  - Midori
  - Pale Moon

- Supports multiple package managers:
  - APT (Debian/Ubuntu)
  - DNF (Fedora)
  - Pacman (Arch)
  - Zypper (openSUSE)
  - Snap
  - Flatpak

- Enhanced Chrome installation with universal Linux compatibility
  - Works across all major distributions (Debian, Ubuntu, Kali, ParrotOS, Fedora, Arch, etc.)
  - Intelligent dependency resolution
  - Multiple installation methods with automatic fallbacks
  - Robust error handling

- Beautiful terminal interface with colored output
- Cross-distribution compatibility
- Multiple installation methods (system packages, Snap, Flatpak)
- Automatic browser detection
- System information display

## 📋 Requirements

- Python 3.x
- Linux operating system
- Required Python packages (auto-installed):
  - distro
  - requests
  - termcolor

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/shahzadafaisal6/browsers_manager.git
   cd browsers_manager
   ```

2. Make the script executable:
   ```bash
   chmod +x browsers_manager.py
   ```

3. Run the script:
   ```bash
   ./browsers_manager.py
   ```

## 💡 Usage

The script provides an interactive menu-driven interface:

1. **Install Browser**: Choose from available browsers and installation methods
2. **Uninstall Browser**: Remove installed browsers
3. **Refresh Browser List**: Update the list of installed browsers
4. **Exit**: Quit the application

## 🔄 Recent Updates (May 2025)

- Enhanced Chrome installation for universal Linux compatibility
- Improved dependency resolution for Debian-based distributions (including Kali Linux)
- Added multiple fallback methods for browser installation
- Improved error handling and recovery
- Better support for diverse Linux distributions

## 📝 Note

- Some browsers may require additional setup after installation
- Tor Browser will launch its setup wizard after installation
- Administrative privileges (sudo) are required for installation/uninstallation

## 👨‍💻 Developer

- **Developer**: Faisal
- **Organization**: HAMNA TEC
- **Contact**: 
  - +923367866994
  - +923013116258

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.