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
                # Universal Chrome installation for all Linux distributions
                try:
                    # Create a temporary directory for downloading
                    temp_dir = "/tmp/chrome_install"
                    os.makedirs(temp_dir, exist_ok=True)
                    os.chdir(temp_dir)
                    
                    # Step 1: Download Chrome .deb package
                    print(colored("Downloading Google Chrome...", "yellow"))
                    chrome_url = "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"
                    chrome_deb = os.path.join(temp_dir, "chrome.deb")
                    
                    try:
                        self.run_command(f"wget {chrome_url} -O {chrome_deb}")
                    except Exception:
                        # Fallback to curl if wget fails
                        try:
                            self.run_command(f"curl -L {chrome_url} -o {chrome_deb}")
                        except Exception as e:
                            print(colored(f"Failed to download Chrome: {str(e)}", "red"))
                            return False
                    
                    # Step 2: Install based on package manager and distribution
                    print(colored("Installing Google Chrome...", "yellow"))
                    success = False
                    
                    if distro_family in ['debian', 'ubuntu'] or self.package_manager['name'] in ['apt', 'apt-get']:
                        # For Debian/Ubuntu/Kali/ParrotOS
                        try:
                            # First install dependencies that Chrome needs
                            deps = "libappindicator1 libindicator7 libxss1 fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 libgtk-3-0 libgbm1 xdg-utils"
                            self.run_command(f"sudo apt-get update && sudo apt-get install -y {deps}")
                        except Exception:
                            print(colored("Attempting to install dependencies with alternative method...", "yellow"))
                            # Some packages might have different names in different distributions
                            try:
                                alternative_deps = "libxss1 fonts-liberation libasound2 libatk-bridge2.0-0 libgbm1 libgtk-3-0 xdg-utils"
                                self.run_command(f"sudo apt-get update && sudo apt-get install -y {alternative_deps}")
                            except Exception:
                                print(colored("Continuing without installing all dependencies...", "yellow"))
                        
                        # Install the .deb package
                        try:
                            # First try with dpkg
                            self.run_command(f"sudo dpkg -i {chrome_deb}")
                            # Fix any dependency issues
                            self.run_command("sudo apt-get install -f -y")
                            # Verify installation
                            if self.command_exists('google-chrome-stable'):
                                success = True
                            else:
                                # Try direct apt install as a fallback
                                self.run_command(f"sudo apt install {chrome_deb} -y")
                                success = self.command_exists('google-chrome-stable')
                        except Exception as e:
                            print(colored(f"Error during Chrome installation: {str(e)}", "red"))
                            
                    elif distro_family == 'fedora' or self.package_manager['name'] in ['dnf', 'yum']:
                        # For Fedora/RHEL based
                        try:
                            # Convert .deb to .rpm using alien
                            print(colored("Converting .deb package to .rpm...", "yellow"))
                            self.run_command("sudo dnf install alien -y")
                            self.run_command(f"sudo alien --to-rpm {chrome_deb}")
                            rpm_file = self.run_command("find . -name '*.rpm'", capture_output=True)
                            if rpm_file:
                                self.run_command(f"sudo dnf install {rpm_file} -y")
                                success = self.command_exists('google-chrome-stable')
                        except Exception as e:
                            print(colored(f"Error converting or installing RPM: {str(e)}", "red"))
                            
                            # Try adding Google repository directly
                            try:
                                print(colored("Trying repository method...", "yellow"))
                                self.run_command("sudo dnf config-manager --add-repo https://dl.google.com/linux/chrome/rpm/stable/x86_64")
                                self.run_command("sudo rpm --import https://dl.google.com/linux/linux_signing_key.pub")
                                self.run_command("sudo dnf install google-chrome-stable -y")
                                success = self.command_exists('google-chrome-stable')
                            except Exception:
                                pass
                            
                    elif distro_family == 'arch' or self.package_manager['name'] == 'pacman':
                        # For Arch-based systems
                        try:
                            # Try using AUR helper if available
                            if self.command_exists('yay'):
                                self.run_command("yay -S --noconfirm google-chrome")
                                success = self.command_exists('google-chrome')
                            elif self.command_exists('pamac'):
                                self.run_command("pamac install google-chrome --no-confirm")
                                success = self.command_exists('google-chrome')
                            else:
                                # Manual AUR installation
                                print(colored("Installing from AUR manually...", "yellow"))
                                self.run_command("git clone https://aur.archlinux.org/google-chrome.git /tmp/google-chrome")
                                self.run_command("cd /tmp/google-chrome && makepkg -si --noconfirm")
                                success = self.command_exists('google-chrome')
                        except Exception as e:
                            print(colored(f"Error installing Chrome on Arch: {str(e)}", "red"))
                            
                    elif distro_family == 'opensuse' or self.package_manager['name'] == 'zypper':
                        # For openSUSE
                        try:
                            self.run_command("sudo rpm --import https://dl.google.com/linux/linux_signing_key.pub")
                            self.run_command("sudo zypper addrepo http://dl.google.com/linux/chrome/rpm/stable/x86_64 google-chrome")
                            self.run_command("sudo zypper refresh")
                            self.run_command("sudo zypper install -y google-chrome-stable")
                            success = self.command_exists('google-chrome-stable')
                        except Exception as e:
                            print(colored(f"Error installing Chrome on openSUSE: {str(e)}", "red"))
                    
                    else:
                        # Generic approach for other distributions - try with dpkg and apt
                        print(colored("Using generic installation approach...", "yellow"))
                        try:
                            # Try to use dpkg and apt-get first as many distributions have compatibility
                            self.run_command(f"sudo dpkg -i {chrome_deb}")
                            self.run_command("sudo apt-get install -f -y")
                            success = self.command_exists('google-chrome-stable')
                        except Exception:
                            # Try gdebi as another option
                            try:
                                self.run_command("sudo apt-get install gdebi-core -y")
                                self.run_command(f"sudo gdebi --non-interactive {chrome_deb}")
                                success = self.command_exists('google-chrome-stable')
                            except Exception as e:
                                print(colored(f"Failed to install Chrome using generic methods: {str(e)}", "red"))
                    
                    # Cleanup
                    try:
                        self.run_command(f"rm -rf {temp_dir}")
                    except:
                        pass
                    
                    if success:
                        print(colored("Google Chrome installed successfully!", "green"))
                        # Update installed browsers
                        self.installed_browsers = self.detect_installed_browsers()
                        return True
                    else:
                        # Last resort - try using flatpak or snap if available
                        if self.command_exists('flatpak'):
                            print(colored("Attempting installation via Flatpak...", "yellow"))
                            self.run_command("flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo")
                            if self.run_command("flatpak install flathub com.google.Chrome -y"):
                                print(colored("Google Chrome installed successfully via Flatpak!", "green"))
                                self.installed_browsers = self.detect_installed_browsers()
                                return True
                        
                        if self.command_exists('snap'):
                            print(colored("Attempting installation via Snap...", "yellow"))
                            if self.run_command("sudo snap install google-chrome"):
                                print(colored("Google Chrome installed successfully via Snap!", "green"))
                                self.installed_browsers = self.detect_installed_browsers()
                                return True
                        
                        print(colored("All installation methods failed. Please install Chrome manually.", "red"))
                        return False
                
                except Exception as e:
                    print(colored(f"Unexpected error during Chrome installation: {str(e)}", "red"))
                    return False
                    
            # Continue with other browsers installation
            elif browser_id == 'brave':
                # Special handling for Brave browser
                try:
                    print(colored("Setting up Brave browser repository...", "yellow"))
                    if distro_family in ['debian', 'ubuntu'] or self.package_manager['name'] in ['apt', 'apt-get']:
                        # For Debian/Ubuntu/Kali/ParrotOS
                        try:
                            # Install dependencies
                            self.run_command("sudo apt-get install apt-transport-https curl gnupg -y")
                            # Add Brave repository
                            self.run_command("sudo curl -fsSLo /usr/share/keyrings/brave-browser-archive-keyring.gpg https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg")
                            arch = self.run_command("dpkg --print-architecture", capture_output=True) or "amd64"
                            self.run_command(f'echo "deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg] https://brave-browser-apt-release.s3.brave.com/ stable main" | sudo tee /etc/apt/sources.list.d/brave-browser-release.list')
                            # Update and install
                            self.run_command("sudo apt-get update")
                            self.run_command("sudo apt-get install brave-browser -y")
                            success = self.command_exists('brave-browser')
                        except Exception as e:
                            print(colored(f"Error during Brave repository setup: {str(e)}", "red"))
                            success = False
                    
                    elif distro_family == 'fedora' or self.package_manager['name'] in ['dnf', 'yum']:
                        # For Fedora/RHEL based
                        try:
                            # Add the repository
                            self.run_command("sudo dnf config-manager --add-repo https://brave-browser-rpm-release.s3.brave.com/x86_64/")
                            self.run_command("sudo rpm --import https://brave-browser-rpm-release.s3.brave.com/brave-core.asc")
                            # Install the browser
                            self.run_command("sudo dnf install brave-browser -y")
                            success = self.command_exists('brave-browser')
                        except Exception as e:
                            print(colored(f"Error installing Brave on Fedora: {str(e)}", "red"))
                            success = False
                            
                    elif distro_family == 'arch' or self.package_manager['name'] == 'pacman':
                        # For Arch-based systems
                        try:
                            if self.command_exists('yay'):
                                self.run_command("yay -S brave-bin --noconfirm")
                            elif self.command_exists('pamac'):
                                self.run_command("pamac build brave-bin --no-confirm")
                            else:
                                # Manual AUR installation
                                print(colored("Installing from AUR manually...", "yellow"))
                                self.run_command("git clone https://aur.archlinux.org/brave-bin.git /tmp/brave-bin")
                                self.run_command("cd /tmp/brave-bin && makepkg -si --noconfirm")
                            success = self.command_exists('brave')
                        except Exception as e:
                            print(colored(f"Error installing Brave on Arch: {str(e)}", "red"))
                            success = False
                    
                    else:
                        # Fallback for other distributions - try snap/flatpak
                        success = False
                        print(colored("No direct installation method for this distribution. Trying alternatives...", "yellow"))
                    
                    if not success:
                        # Try using flatpak or snap if traditional methods fail
                        if self.command_exists('flatpak'):
                            print(colored("Attempting installation via Flatpak...", "yellow"))
                            self.run_command("flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo")
                            if self.run_command("flatpak install flathub com.brave.Browser -y"):
                                print(colored("Brave Browser installed successfully via Flatpak!", "green"))
                                self.installed_browsers = self.detect_installed_browsers()
                                return True
                        
                        if self.command_exists('snap'):
                            print(colored("Attempting installation via Snap...", "yellow"))
                            if self.run_command("sudo snap install brave"):
                                print(colored("Brave Browser installed successfully via Snap!", "green"))
                                self.installed_browsers = self.detect_installed_browsers()
                                return True
                                
                    if success:
                        print(colored("Brave Browser installed successfully!", "green"))
                        self.installed_browsers = self.detect_installed_browsers()
                        return True
                    else:
                        print(colored("All installation methods failed. Please install Brave manually.", "red"))
                        return False
                        
                except Exception as e:
                    print(colored(f"Unexpected error during Brave installation: {str(e)}", "red"))
                    return False
                    
            # Standard installation for other browsers
            else:
                try:
                    # Try installing using the system's package manager
                    if distro_family in ['debian', 'ubuntu'] or self.package_manager['name'] in ['apt', 'apt-get']:
                        # For Debian/Ubuntu based
                        for package_name in package_names:
                            try:
                                self.run_command(f"sudo apt-get update")
                                self.run_command(f"sudo apt-get install {package_name} -y")
                                if self.command_exists(package_name) or self.run_command(f"dpkg -l | grep -q {package_name}", capture_output=False):
                                    print(colored(f"{browser['name']} installed successfully!", "green"))
                                    self.installed_browsers = self.detect_installed_browsers()
                                    return True
                            except Exception:
                                continue
                    
                    elif distro_family == 'fedora' or self.package_manager['name'] in ['dnf', 'yum']:
                        # For Fedora/RHEL based
                        for package_name in package_names:
                            try:
                                self.run_command(f"sudo dnf install {package_name} -y")
                                if self.command_exists(package_name.split('-')[0]) or self.run_command(f"rpm -q {package_name}", capture_output=False):
                                    print(colored(f"{browser['name']} installed successfully!", "green"))
                                    self.installed_browsers = self.detect_installed_browsers()
                                    return True
                            except Exception:
                                continue
                    
                    elif distro_family == 'arch' or self.package_manager['name'] == 'pacman':
                        # For Arch-based systems
                        for package_name in package_names:
                            try:
                                self.run_command(f"sudo pacman -S {package_name} --noconfirm")
                                if self.command_exists(package_name.split('-')[0]) or self.run_command(f"pacman -Q {package_name}", capture_output=False):
                                    print(colored(f"{browser['name']} installed successfully!", "green"))
                                    self.installed_browsers = self.detect_installed_browsers()
                                    return True
                            except Exception:
                                # Try AUR if official repos fail
                                try:
                                    if self.command_exists('yay'):
                                        self.run_command(f"yay -S {package_name} --noconfirm")
                                    elif self.command_exists('pamac'):
                                        self.run_command(f"pamac build {package_name} --no-confirm")
                                    else:
                                        continue
                                    
                                    if self.command_exists(package_name.split('-')[0]):
                                        print(colored(f"{browser['name']} installed successfully!", "green"))
                                        self.installed_browsers = self.detect_installed_browsers()
                                        return True
                                except Exception:
                                    continue
                    
                    elif distro_family == 'opensuse' or self.package_manager['name'] == 'zypper':
                        # For openSUSE
                        for package_name in package_names:
                            try:
                                self.run_command(f"sudo zypper install -y {package_name}")
                                if self.command_exists(package_name.split('-')[0]) or self.run_command(f"rpm -q {package_name}", capture_output=False):
                                    print(colored(f"{browser['name']} installed successfully!", "green"))
                                    self.installed_browsers = self.detect_installed_browsers()
                                    return True
                            except Exception:
                                continue
                    
                    # If we get here, system package manager installation failed or not supported
                    # Try using flatpak or snap if available
                    if installation_type == 'system': 
                        print(colored("System package installation failed. Trying alternative methods...", "yellow"))
                        
                        if self.command_exists('flatpak'):
                            print(colored("Attempting installation via Flatpak...", "yellow"))
                            self.run_command("flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo")
                            if self.run_command(f"flatpak install flathub {browser['flatpak']} -y"):
                                print(colored(f"{browser['name']} installed successfully via Flatpak!", "green"))
                                self.installed_browsers = self.detect_installed_browsers()
                                return True
                        
                        if self.command_exists('snap'):
                            print(colored("Attempting installation via Snap...", "yellow"))
                            if self.run_command(f"sudo snap install {browser['snap']}"):
                                print(colored(f"{browser['name']} installed successfully via Snap!", "green"))
                                self.installed_browsers = self.detect_installed_browsers()
                                return True
                    
                    print(colored(f"Failed to install {browser['name']}. Please install it manually.", "red"))
                    return False
                    
                except Exception as e:
                    print(colored(f"Error during installation: {str(e)}", "red"))
                    return False
        
        elif installation_type == 'snap':
            # Install using Snap
            if self.command_exists('snap'):
                try:
                    self.run_command(f"sudo snap install {browser['snap']}")
                    print(colored(f"{browser['name']} installed successfully via Snap!", "green"))
                    self.installed_browsers = self.detect_installed_browsers()
                    return True
                except Exception as e:
                    print(colored(f"Error during Snap installation: {str(e)}", "red"))
                    return False
            else:
                print(colored("Snap is not installed on your system. Please install it first.", "red"))
                return False
                
        elif installation_type == 'flatpak':
            # Install using Flatpak
            if self.command_exists('flatpak'):
                try:
                    self.run_command("flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo")
                    self.run_command(f"flatpak install flathub {browser['flatpak']} -y")
                    print(colored(f"{browser['name']} installed successfully via Flatpak!", "green"))
                    self.installed_browsers = self.detect_installed_browsers()
                    return True
                except Exception as e:
                    print(colored(f"Error during Flatpak installation: {str(e)}", "red"))
                    return False
            else:
                print(colored("Flatpak is not installed on your system. Please install it first.", "red"))
                return False
                
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