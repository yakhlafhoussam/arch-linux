
#!/usr/bin/env python3

import os
import shutil
import subprocess
import sys


def run_command(command):
    return subprocess.run(command, check=False).returncode


def check_root():
    if os.geteuid() != 0:
        print("Run this script as root:")
        print("  sudo python arch_installer.py")
        sys.exit(1)


def check_archinstall():
    if shutil.which("archinstall") is None:
        print("archinstall is not installed.")
        print("Connect to the internet and run:")
        print("  pacman -Sy archinstall")
        sys.exit(1)


def check_live_environment():
    if not os.path.exists("/run/archiso"):
        print("This script should be run from Arch Linux Live USB.")
        sys.exit(1)


def show_disks():
    print("\nAvailable disks:\n")

    subprocess.run([
        "lsblk",
        "-d",
        "-o", "NAME,SIZE,MODEL,TYPE"
    ])

    print()


def choose_disk():
    show_disks()

    disk = input(
        "Enter the disk to install Arch on "
        "(example: /dev/nvme0n1): "
    ).strip()

    if not disk.startswith("/dev/"):
        print("Invalid disk path.")
        sys.exit(1)

    if not os.path.exists(disk):
        print("Disk does not exist.")
        sys.exit(1)

    print("\nWARNING: The selected disk may be erased.")
    print(f"Selected disk: {disk}")

    confirmation = input(
        f"Type ERASE {disk} to continue: "
    ).strip()

    if confirmation != f"ERASE {disk}":
        print("Installation cancelled.")
        sys.exit(0)

    return disk


def start_installer():
    check_root()
    check_archinstall()
    check_live_environment()

    print("=== Arch Linux Installer ===")

    disk = choose_disk()

    print("\nStarting the official Arch installer...")
    print("Choose your disk and partitioning options carefully.")
    print("Continue through the installer to select your desktop.")

    result = run_command(["archinstall"])

    if result == 0:
        print("\nArchinstall finished.")
        print("Follow its instructions to reboot.")
    else:
        print("\nArchinstall exited with an error.")
        print("Check the installer logs before trying again.")


if __name__ == "__main__":
    start_installer()
