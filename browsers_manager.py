#!/usr/bin/env python3
"""
Browsers-Manager: A comprehensive Python script for managing browsers on Linux systems
Developed by: Faisal
Organization: HAMNA TEC
Contact: +923367866994, +923013116258
"""

import os
import sys
import json
import platform
import subprocess
from datetime import datetime

def check_and_install_dependencies():
    """Check and install required system packages"""
    required_packages = {
        'python3-distro': 'distro',
        'python3-requests': 'requests',
        'python3-termcolor': 'termcolor'
    }
    
    missing_packages = []
    for system_package, python_module in required_packages.items():
        try:
            __import__(python_module)
        except ImportError:
            missing_packages.append(system_package)
    
    if missing_packages:
        print("Installing required system packages...")
        install_cmd = f"sudo apt-get install -y {' '.join(missing_packages)}"
        try:
            subprocess.run(install_cmd, shell=True, check=True)
            print("Packages installed successfully!")
            print("Please run the script again.")
            sys.exit(0)
        except subprocess.CalledProcessError:
            print("Failed to install required packages. Please install them manually:")
            print(f"sudo apt-get install {' '.join(missing_packages)}")
            sys.exit(1)

# Check dependencies before importing
check_and_install_dependencies()

# Now import the required modules
import distro
import requests
from termcolor import colored


class BrowserManager:
    """
    Main class for browser management functionality on Linux systems
    """
    def __init__(self):
        """Initialize the BrowserManager class"""
        self.os_info = self.get_system_info()
        self.package_manager = self.detect_package_manager()
        self.browsers = {
            'firefox': {
                'name': 'Mozilla Firefox',
                'package': {
                    'debian': ['firefox-esr', 'firefox'],
                    'ubuntu': ['firefox'],
                    'fedora': ['firefox'],
                    'arch': ['firefox'],
                    'opensuse': ['MozillaFirefox'],
                    'default': ['firefox', 'firefox-esr']
                },
                'snap': 'firefox',
                'flatpak': 'org.mozilla.firefox',
                'description': 'Popular open-source web browser from Mozilla'
            },
            'chromium': {
                'name': 'Chromium',
                'package': {
                    'debian': ['chromium', 'chromium-browser'],
                    'ubuntu': ['chromium-browser'],
                    'fedora': ['chromium'],
                    'arch': ['chromium'],
                    'opensuse': ['chromium'],
                    'default': ['chromium', 'chromium-browser']
                },
                'snap': 'chromium',
                'flatpak': 'org.chromium.Chromium',
                'description': 'Open-source browser project that forms the basis for Chrome'
            },
            'chrome': {
                'name': 'Google Chrome',
                'package': {
                    'debian': ['google-chrome-stable'],
                    'ubuntu': ['google-chrome-stable'],
                    'fedora': ['google-chrome-stable'],
                    'arch': ['google-chrome'],
                    'opensuse': ['google-chrome-stable'],
                    'default': ['google-chrome-stable', 'google-chrome']
                },
                'snap': 'google-chrome',
                'flatpak': 'com.google.Chrome',
                'description': 'Google\'s web browser'
            },
            'tor-browser': {
                'name': 'Tor Browser',
                'package': {
                    'debian': ['torbrowser-launcher'],
                    'ubuntu': ['torbrowser-launcher'],
                    'fedora': ['torbrowser-launcher'],
                    'arch': ['tor-browser'],
                    'opensuse': ['torbrowser-launcher'],
                    'default': ['torbrowser-launcher', 'tor-browser']
                },
                'snap': 'tor-browser',
                'flatpak': 'com.github.micahflee.torbrowser-launcher',
                'description': 'Privacy-focused browser for anonymous browsing'
            },
            'brave': {
                'name': 'Brave Browser',
                'package': {
                    'debian': ['brave-browser'],
                    'ubuntu': ['brave-browser'],
                    'fedora': ['brave-browser'],
                    'arch': ['brave-bin'],
                    'opensuse': ['brave-browser'],
                    'default': ['brave-browser', 'brave-bin']
                },
                'snap': 'brave',
                'flatpak': 'com.brave.Browser',
                'description': 'Privacy-focused browser based on Chromium'
            },
            'vivaldi': {
                'name': 'Vivaldi',
                'package': {
                    'debian': ['vivaldi-stable'],
                    'ubuntu': ['vivaldi-stable'],
                    'fedora': ['vivaldi-stable'],
                    'arch': ['vivaldi'],
                    'opensuse': ['vivaldi'],
                    'default': ['vivaldi-stable', 'vivaldi']
                },
                'snap': 'vivaldi',
                'flatpak': 'com.vivaldi.Vivaldi',
                'description': 'Feature-rich browser based on Chromium'
            },
            'opera': {
                'name': 'Opera',
                'package': {
                    'debian': ['opera-stable'],
                    'ubuntu': ['opera-stable'],
                    'fedora': ['opera-stable'],
                    'arch': ['opera'],
                    'opensuse': ['opera'],
                    'default': ['opera-stable', 'opera']
                },
                'snap': 'opera',
                'flatpak': 'com.opera.Opera',
                'description': 'Feature-rich browser with built-in VPN'
            },
            'edge': {
                'name': 'Microsoft Edge',
                'package': {
                    'debian': ['microsoft-edge-stable'],
                    'ubuntu': ['microsoft-edge-stable'],
                    'fedora': ['microsoft-edge-stable'],
                    'arch': ['microsoft-edge-stable-bin'],
                    'opensuse': ['microsoft-edge'],
                    'default': ['microsoft-edge-stable', 'microsoft-edge']
                },
                'snap': 'microsoft-edge',
                'flatpak': 'com.microsoft.Edge',
                'description': 'Microsoft\'s Chromium-based browser'
            },
            'falkon': {
                'name': 'Falkon',
                'package': {
                    'debian': ['falkon'],
                    'ubuntu': ['falkon'],
                    'fedora': ['falkon'],
                    'arch': ['falkon'],
                    'opensuse': ['falkon'],
                    'default': ['falkon']
                },
                'snap': 'falkon',
                'flatpak': 'org.kde.falkon',
                'description': 'KDE web browser using QtWebEngine'
            },
            'midori': {
                'name': 'Midori',
                'package': {
                    'debian': ['midori'],
                    'ubuntu': ['midori'],
                    'fedora': ['midori'],
                    'arch': ['midori'],
                    'opensuse': ['midori'],
                    'default': ['midori']
                },
                'snap': 'midori',
                'flatpak': 'org.midori_browser.Midori',
                'description': 'Lightweight web browser'
            }
        }
        self.installed_browsers = self.detect_installed_browsers()

    def get_system_info(self):
        """Get detailed system information including distribution family"""
        system_info = {
            'os': platform.system(),
            'distro': distro.name(pretty=True),
            'version': distro.version(),
            'codename': distro.codename(),
            'python_version': platform.python_version(),
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'distro_id': distro.id()
        }
        
        # Determine distribution family
        distro_id = distro.id().lower()
        if distro_id in ['debian', 'raspbian']:
            system_info['distro_family'] = 'debian'
        elif distro_id in ['ubuntu', 'linuxmint', 'pop', 'elementary']:
            system_info['distro_family'] = 'ubuntu'
        elif distro_id in ['fedora', 'rhel', 'centos', 'rocky', 'almalinux']:
            system_info['distro_family'] = 'fedora'
        elif distro_id in ['arch', 'manjaro', 'endeavouros']:
            system_info['distro_family'] = 'arch'
        elif distro_id in ['opensuse-leap', 'opensuse-tumbleweed', 'suse']:
            system_info['distro_family'] = 'opensuse'
        else:
            system_info['distro_family'] = 'default'
        
        return system_info

    def detect_package_manager(self):
        """Detect the system's package manager with enhanced detection"""
        package_managers = {
            'apt': {
                'name': 'apt',
                'install': 'apt install -y',
                'remove': 'apt remove -y',
                'update': 'apt update',
                'type': 'system',
                'check_cmd': 'which apt'
            },
            'dnf': {
                'name': 'dnf',
                'install': 'dnf install -y',
                'remove': 'dnf remove -y',
                'update': 'dnf check-update',
                'type': 'system',
                'check_cmd': 'which dnf'
            },
            'yum': {
                'name': 'yum',
                'install': 'yum install -y',
                'remove': 'yum remove -y',
                'update': 'yum check-update',
                'type': 'system',
                'check_cmd': 'which yum'
            },
            'pacman': {
                'name': 'pacman',
                'install': 'pacman -S --noconfirm',
                'remove': 'pacman -R --noconfirm',
                'update': 'pacman -Sy',
                'type': 'system',
                'check_cmd': 'which pacman'
            },
            'zypper': {
                'name': 'zypper',
                'install': 'zypper install -y',
                'remove': 'zypper remove -y',
                'update': 'zypper refresh',
                'type': 'system',
                'check_cmd': 'which zypper'
            }
        }

        # Check for system package managers
        for pm_name, pm_info in package_managers.items():
            if self.command_exists(pm_name):
                return pm_info

        # Check for alternative package managers
        if self.command_exists('snap'):
            return {'name': 'snap', 'install': 'snap install', 'remove': 'snap remove', 'type': 'snap'}
        elif self.command_exists('flatpak'):
            return {'name': 'flatpak', 'install': 'flatpak install -y', 'remove': 'flatpak uninstall -y', 'type': 'flatpak'}

        # Default to APT if couldn't detect
        return package_managers['apt']

    def detect_installed_browsers(self):
        """Detect installed browsers on the system with enhanced detection"""
        installed = {}
        distro_family = self.os_info['distro_family']
        
        # Check for system package manager installed browsers
        for browser_id, browser_info in self.browsers.items():
            package_names = browser_info['package'].get(distro_family, browser_info['package']['default'])
            
            # Check using different methods based on package manager
            if self.package_manager['name'] == 'apt':
                for package_name in package_names:
                    check_cmd = f"dpkg-query -W -f='${{Status}}' {package_name} 2>/dev/null | grep -c 'ok installed'"
                    installed_check = self.run_command(check_cmd, capture_output=True)
                    if installed_check and installed_check != "0":
                        installed[browser_id] = {**browser_info, 'installation_type': 'system', 'installed_package': package_name}
                        break
            
            elif self.package_manager['name'] in ['dnf', 'yum']:
                for package_name in package_names:
                    check_cmd = f"rpm -q {package_name}"
                    if self.run_command(check_cmd, capture_output=False):
                        installed[browser_id] = {**browser_info, 'installation_type': 'system', 'installed_package': package_name}
                        break
            
            elif self.package_manager['name'] == 'pacman':
                for package_name in package_names:
                    check_cmd = f"pacman -Q {package_name} 2>/dev/null"
                    if self.run_command(check_cmd, capture_output=False):
                        installed[browser_id] = {**browser_info, 'installation_type': 'system', 'installed_package': package_name}
                        break
            
            elif self.package_manager['name'] == 'zypper':
                for package_name in package_names:
                    check_cmd = f"rpm -q {package_name}"
                    if self.run_command(check_cmd, capture_output=False):
                        installed[browser_id] = {**browser_info, 'installation_type': 'system', 'installed_package': package_name}
                        break
        
        # Check for Snap installed browsers
        if self.command_exists('snap'):
            snap_list = self.run_command("snap list", capture_output=True)
            if snap_list:
                for browser_id, browser_info in self.browsers.items():
                    if browser_info['snap'] in snap_list:
                        installed[browser_id] = {**browser_info, 'installation_type': 'snap'}
        
        # Check for Flatpak installed browsers
        if self.command_exists('flatpak'):
            flatpak_list = self.run_command("flatpak list", capture_output=True)
            if flatpak_list:
                for browser_id, browser_info in self.browsers.items():
                    if browser_info['flatpak'] in flatpak_list:
                        installed[browser_id] = {**browser_info, 'installation_type': 'flatpak'}
        
        # Additional detection methods for special cases
        # Check for Firefox from Mozilla's official binaries
        if not 'firefox' in installed and os.path.exists('/opt/firefox/firefox'):
            installed['firefox'] = {**self.browsers['firefox'], 'installation_type': 'manual', 'installed_package': 'firefox-mozilla'}
        
        # Check for Chrome/Chromium in alternative locations
        chrome_paths = [
            '/usr/bin/google-chrome',
            '/usr/bin/chromium',
            '/usr/bin/chromium-browser',
            '/snap/bin/chromium',
            '/var/lib/flatpak/app/org.chromium.Chromium'
        ]
        for path in chrome_paths:
            if os.path.exists(path):
                browser_id = 'chrome' if 'google-chrome' in path else 'chromium'
                if browser_id not in installed:
                    installed[browser_id] = {**self.browsers[browser_id], 'installation_type': 'manual', 'installed_package': os.path.basename(path)}
        
        return installed

    def install_browser(self, browser_id, installation_type='system'):
        """Install a browser with enhanced installation support"""
        browser = self.browsers.get(browser_id)
        if not browser:
            print(colored("Browser not found in available list", "red"))
            return False
        
        print(colored(f"\nInstalling {browser['name']}...", "blue"))
        print(colored(f"Description: {browser['description']}", "cyan"))
        
        if installation_type == 'system':
            distro_family = self.os_info['distro_family']
            package_names = browser['package'].get(distro_family, browser['package']['default'])
            
            # Special handling for different browsers and distributions
            if browser_id == 'chrome':
                if distro_family in ['debian', 'ubuntu']:
                    try:
                        print(colored("Adding Google Chrome repository...", "yellow"))
                        self.run_command("wget -q -O /tmp/linux_signing_key.pub https://dl.google.com/linux/linux_signing_key.pub")
                        self.run_command("sudo apt-key add /tmp/linux_signing_key.pub")
                        self.run_command("echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list")
                        self.run_command("sudo apt update")
                    except Exception as e:
                        print(colored("Failed to add Google Chrome repository. Trying alternative installation...", "yellow"))
                        # Try downloading and installing the DEB package directly
                        try:
                            print(colored("Downloading Google Chrome...", "yellow"))
                            self.run_command("wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O /tmp/chrome.deb")
                            print(colored("Installing Google Chrome...", "yellow"))
                            self.run_command("sudo dpkg -i /tmp/chrome.deb || sudo apt-get -f install -y")
                            self.run_command("rm /tmp/chrome.deb")
                            print(colored("Google Chrome installed successfully!", "green"))
                            return True
                        except Exception as e:
                            print(colored(f"Failed to install Google Chrome: {str(e)}", "red"))
                            return False
                elif distro_family == 'fedora':
                    print(colored("Adding Google Chrome repository...", "yellow"))
                    self.run_command("sudo dnf config-manager --add-repo https://dl.google.com/linux/chrome/rpm/stable/x86_64")
                    self.run_command("sudo rpm --import https://dl.google.com/linux/linux_signing_key.pub")
                elif distro_family == 'arch':
                    print(colored("Installing Google Chrome using yay...", "yellow"))
                    if self.command_exists('yay'):
                        self.run_command("yay -S --noconfirm google-chrome")
                    else:
                        print(colored("yay is not installed. Installing from AUR helper...", "yellow"))
                        self.run_command("git clone https://aur.archlinux.org/google-chrome.git /tmp/google-chrome")
                        self.run_command("cd /tmp/google-chrome && makepkg -si --noconfirm")
                    return True
            
            elif browser_id == 'brave':
                if distro_family in ['debian', 'ubuntu']:
                    try:
                        print(colored("Adding Brave Browser repository...", "yellow"))
                        self.run_command("sudo apt install apt-transport-https curl -y")
                        self.run_command("sudo curl -fsSLo /usr/share/keyrings/brave-browser-archive-keyring.gpg https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg")
                        self.run_command("echo 'deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg arch=amd64] https://brave-browser-apt-release.s3.brave.com/ stable main' | sudo tee /etc/apt/sources.list.d/brave-browser-release.list")
                        self.run_command("sudo apt update")
                    except Exception as e:
                        print(colored(f"Failed to add Brave repository: {str(e)}", "red"))
                        return False
                elif distro_family == 'fedora':
                    print(colored("Adding Brave Browser repository...", "yellow"))
                    self.run_command("sudo dnf config-manager --add-repo https://brave-browser-rpm-release.s3.brave.com/x86_64/")
                    self.run_command("sudo rpm --import https://brave-browser-rpm-release.s3.brave.com/brave-core.asc")
            
            elif browser_id == 'tor-browser':
                if distro_family in ['debian', 'ubuntu']:
                    print(colored("Adding universe repository and updating...", "yellow"))
                    self.run_command("sudo apt install -y apt-transport-https")
                    self.run_command("sudo add-apt-repository universe")
                    self.run_command("sudo apt update")
                elif distro_family == 'arch':
                    # For Arch Linux, tor-browser is in the community repository
                    package_names = ['tor-browser']
            
            # Install using the system package manager
            for package_name in package_names:
                print(colored(f"Installing {package_name}...", "yellow"))
                install_command = f"sudo {self.package_manager['install']} {package_name}"
                if self.run_command(install_command):
                    print(colored(f"{browser['name']} installed successfully!", "green"))
                    
                    # Post-installation setup for Tor Browser
                    if browser_id == 'tor-browser':
                        print(colored("Launching Tor Browser setup...", "yellow"))
                        self.run_command("torbrowser-launcher")
                    
                    self.installed_browsers = self.detect_installed_browsers()
                    return True
            
            print(colored(f"Failed to install {browser['name']}", "red"))
            return False
            
        elif installation_type == 'snap':
            # Install using Snap
            package_name = browser['snap']
            install_command = f"sudo snap install {package_name}"
            
        elif installation_type == 'flatpak':
            # Add Flathub repository if not already added
            if not self.run_command("flatpak remotes | grep -q flathub"):
                self.run_command("flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo")
            
            # Install using Flatpak
            package_name = browser['flatpak']
            install_command = f"flatpak install flathub {package_name} -y"
        
        else:
            print(colored("Invalid installation type", "red"))
            return False
        
        print(colored(f"Running: {install_command}", "yellow"))
        if self.run_command(install_command):
            print(colored(f"{browser['name']} installed successfully!", "green"))
            self.installed_browsers = self.detect_installed_browsers()
            return True
        else:
            print(colored(f"Failed to install {browser['name']}", "red"))
            return False

    def command_exists(self, command):
        """Check if a command exists in the system"""
        return subprocess.call(['which', command], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

    def run_command(self, command, capture_output=False):
        """Run a shell command and return the output"""
        try:
            if capture_output:
                result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
                return result.stdout.strip()
            else:
                subprocess.run(command, shell=True, check=True)
                return True
        except subprocess.CalledProcessError:
            return False

    def uninstall_browser(self, browser_id):
        """Uninstall a browser from the system"""
        browser_info = self.installed_browsers.get(browser_id)
        if not browser_info:
            print(colored("Browser not installed or not found", "red"))
            return False
        
        print(colored(f"\nUninstalling {browser_info['name']}...", "blue"))
        
        installation_type = browser_info.get('installation_type', 'system')
        
        if installation_type == 'system':
            # Uninstall using the system package manager
            uninstall_command = f"sudo {self.package_manager['remove']} {browser_info['package']}"
        elif installation_type == 'snap':
            # Uninstall using Snap
            uninstall_command = f"sudo snap remove {browser_info['snap']}"
        elif installation_type == 'flatpak':
            # Uninstall using Flatpak
            uninstall_command = f"flatpak uninstall {browser_info['flatpak']} -y"
        else:
            print(colored("Unknown installation type", "red"))
            return False
        
        print(colored(f"Running: {uninstall_command}", "yellow"))
        if self.run_command(uninstall_command):
            print(colored(f"{browser_info['name']} uninstalled successfully!", "green"))
            # Update the installed browsers list
            self.installed_browsers = self.detect_installed_browsers()
            return True
        else:
            print(colored(f"Failed to uninstall {browser_info['name']}", "red"))
            return False

    def display_system_info(self):
        """Display system information in a nice format"""
        print(colored("\n╔═══════════════════════════════════════╗", "blue"))
        print(colored("║          SYSTEM INFORMATION           ║", "blue"))
        print(colored("╚═══════════════════════════════════════╝", "blue"))
        print(colored(f"Operating System: {self.os_info['distro']} {self.os_info['version']}", "yellow"))
        print(colored(f"Codename: {self.os_info['codename']}", "yellow"))
        print(colored(f"Python Version: {self.os_info['python_version']}", "yellow"))
        print(colored(f"Package Manager: {self.package_manager['name'].upper()}", "yellow"))
        print(colored(f"Date & Time: {self.os_info['date']}", "yellow"))

    def display_installed_browsers(self):
        """Display installed browsers in a nice format"""
        if not self.installed_browsers:
            print(colored("\nNo browsers detected on your system!", "red"))
            return
        
        print(colored("\n╔═══════════════════════════════════════╗", "green"))
        print(colored("║          INSTALLED BROWSERS           ║", "green"))
        print(colored("╚═══════════════════════════════════════╝", "green"))
        
        for browser_id, browser_info in self.installed_browsers.items():
            installation_type = browser_info.get('installation_type', 'system').upper()
            print(colored(f"• {browser_info['name']} [{installation_type}]", "cyan"))

    def display_main_menu(self):
        """Display the main menu and handle user interaction"""
        while True:
            self.display_system_info()
            self.display_installed_browsers()
            
            print(colored("\nMenu Options:", "blue"))
            print("1. Install a Browser")
            print("2. Uninstall a Browser")
            print("3. Refresh Browser List")
            print("4. Exit")
            
            choice = input(colored("\nEnter your choice (1-4): ", "yellow"))
            
            if choice == "1":
                self.display_install_menu()
            elif choice == "2":
                self.display_uninstall_menu()
            elif choice == "3":
                self.installed_browsers = self.detect_installed_browsers()
                print(colored("\nBrowser list refreshed!", "green"))
            elif choice == "4":
                print(colored("\nThank you for using Browser Manager!", "blue"))
                print(colored("Developed by Faisal - HAMNA TEC", "blue"))
                print(colored("Contact: +923367866994, +923013116258", "blue"))
                sys.exit(0)
            else:
                print(colored("Invalid choice! Please try again.", "red"))

    def display_install_menu(self):
        """Display the browser installation menu"""
        available_browsers = [browser_id for browser_id in self.browsers 
                             if browser_id not in self.installed_browsers]
        
        if not available_browsers:
            print(colored("\nAll browsers are already installed!", "yellow"))
            input(colored("Press Enter to continue...", "blue"))
            return
        
        print(colored("\nAvailable Browsers:", "blue"))
        for i, browser_id in enumerate(available_browsers, 1):
            browser = self.browsers[browser_id]
            print(f"{i}. {browser['name']}")
            print(colored(f"   {browser['description']}", "cyan"))
        print(f"{len(available_browsers) + 1}. Back to Main Menu")
        
        try:
            choice = int(input(colored("\nEnter your choice: ", "yellow")))
            if choice < 1 or choice > len(available_browsers) + 1:
                raise ValueError
            
            if choice == len(available_browsers) + 1:
                return
            
            browser_id = available_browsers[choice - 1]
            
            print(colored("\nInstallation Type:", "blue"))
            print("1. System Package Manager")
            print("2. Snap (if available)")
            print("3. Flatpak (if available)")
            print("4. Back")
            
            install_type = input(colored("\nEnter your choice (1-4): ", "yellow"))
            
            if install_type == "1":
                self.install_browser(browser_id, "system")
            elif install_type == "2":
                self.install_browser(browser_id, "snap")
            elif install_type == "3":
                self.install_browser(browser_id, "flatpak")
            
            input(colored("Press Enter to continue...", "blue"))
        except (ValueError, IndexError):
            print(colored("Invalid choice! Please try again.", "red"))
            input(colored("Press Enter to continue...", "blue"))

    def display_uninstall_menu(self):
        """Display the browser uninstallation menu"""
        if not self.installed_browsers:
            print(colored("\nNo browsers installed to remove!", "yellow"))
            input(colored("Press Enter to continue...", "blue"))
            return
        
        print(colored("\nInstalled Browsers:", "blue"))
        browser_list = list(self.installed_browsers.items())
        for i, (browser_id, browser_info) in enumerate(browser_list, 1):
            installation_type = browser_info.get('installation_type', 'system').upper()
            print(f"{i}. {browser_info['name']} [{installation_type}]")
        print(f"{len(browser_list) + 1}. Back to Main Menu")
        
        try:
            choice = int(input(colored("\nEnter your choice: ", "yellow")))
            if choice < 1 or choice > len(browser_list) + 1:
                raise ValueError
            
            if choice == len(browser_list) + 1:
                return
            
            browser_id = browser_list[choice - 1][0]
            confirm = input(colored(f"\nAre you sure you want to uninstall {self.installed_browsers[browser_id]['name']}? (y/N): ", "yellow"))
            
            if confirm.lower() == 'y':
                self.uninstall_browser(browser_id)
            
            input(colored("Press Enter to continue...", "blue"))
        except (ValueError, IndexError):
            print(colored("Invalid choice! Please try again.", "red"))
            input(colored("Press Enter to continue...", "blue"))


def print_header():
    """Print a nice header for the application"""
    header = """
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║   ██████╗ ██████╗  ██████╗ ██╗    ██╗███████╗███████╗██████╗   ║
║   ██╔══██╗██╔══██╗██╔═══██╗██║    ██║██╔════╝██╔════╝██╔══██╗  ║
║   ██████╔╝██████╔╝██║   ██║██║ █╗ ██║███████╗█████╗  ██████╔╝  ║
║   ██╔══██╗██╔══██╗██║   ██║██║███╗██║╚════██║██╔══╝  ██╔══██╗  ║
║   ██████╔╝██║  ██║╚██████╔╝╚███╔███╔╝███████║███████╗██║  ██║  ║
║   ╚═════╝ ╚═╝  ╚═╝ ╚═════╝  ╚══╝╚══╝ ╚══════╝╚══════╝╚═╝  ╚═╝  ║
║                                                            ║
║   ███╗   ███╗ █████╗ ███╗   ██╗ █████╗  ██████╗ ███████╗██████╗   ║
║   ████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝ ██╔════╝██╔══██╗  ║
║   ██╔████╔██║███████║██╔██╗ ██║███████║██║  ███╗█████╗  ██████╔╝  ║
║   ██║╚██╔╝██║██╔══██║██║╚██╗██║██╔══██║██║   ██║██╔══╝  ██╔══██╗  ║
║   ██║ ╚═╝ ██║██║  ██║██║ ╚████║██║  ██║╚██████╔╝███████╗██║  ██║  ║
║   ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝  ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
    """
    print(colored(header, "cyan"))
    print(colored("A comprehensive tool to manage web browsers on Linux", "yellow"))
    print(colored("Version: 1.0.0 | Date: April 30, 2025", "yellow"))
    print(colored("────────────────────────────────────────────────────────────", "blue"))
    print(colored("Developed by: Faisal", "green"))
    print(colored("Organization: HAMNA TEC", "green"))
    print(colored("Contact: +923367866994, +923013116258", "green"))
    print(colored("────────────────────────────────────────────────────────────", "blue"))

def main():
    """Main function to run the browser manager"""
    print_header()
    manager = BrowserManager()
    try:
        manager.display_main_menu()
    except KeyboardInterrupt:
        print(colored("\n\nThank you for using Browser Manager!", "blue"))
        print(colored("Developed by Faisal - HAMNA TEC", "blue"))
        print(colored("Contact: +923367866994, +923013116258", "blue"))
        sys.exit(0)


if __name__ == "__main__":
    main()