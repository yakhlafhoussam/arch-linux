#!/usr/bin/env python3

import os
import shutil
import subprocess
import sys

TARGET_PARTITION = "/dev/nvme0n1p6"


def run(command):
    print(f"\n$ {' '.join(command)}")
    return subprocess.run(command, check=False)


def check_root():
    if os.geteuid() != 0:
        print("Please run:")
        print("sudo python arch_installer.py")
        sys.exit(1)


def check_archinstall():
    if shutil.which("archinstall") is None:
        print("archinstall is not installed.")
        print("Run:")
        print("pacman -Sy archinstall")
        sys.exit(1)


def check_partition():
    if not os.path.exists(TARGET_PARTITION):
        print(f"ERROR: {TARGET_PARTITION} does not exist.")
        print("\nAvailable partitions:")
        run(["lsblk", "-o", "NAME,SIZE,FSTYPE,TYPE,MOUNTPOINTS"])
        sys.exit(1)


def show_partition():
    print("\n======================================")
    print("        HYK ARCH INSTALLER")
    print("======================================")

    print("\nTarget partition:")
    run([
        "lsblk",
        "-o",
        "NAME,SIZE,FSTYPE,TYPE,MOUNTPOINTS",
        TARGET_PARTITION
    ])

    print("\nWARNING!")
    print(f"Arch Linux will be installed on {TARGET_PARTITION}.")
    print("The filesystem on this partition may be formatted.")
    print("Make sure this partition contains NO important data.")


def confirm():
    expected = f"INSTALL ARCH ON {TARGET_PARTITION}"

    answer = input(
        f"\nType exactly:\n{expected}\n\n> "
    ).strip()

    if answer != expected:
        print("\nInstallation cancelled.")
        sys.exit(0)


def start_archinstall():
    print("\nStarting archinstall...")
    print("--------------------------------------")

    result = run(["archinstall"])

    if result.returncode == 0:
        print("\nArchinstall finished successfully.")
    else:
        print("\nArchinstall exited with an error.")
        sys.exit(result.returncode)


def main():
    check_root()
    check_archinstall()
    check_partition()

    show_partition()
    confirm()

    start_archinstall()


if __name__ == "__main__":
    main()