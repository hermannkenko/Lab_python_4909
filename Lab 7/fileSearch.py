# Author : Hermann Kenko tanfoudie
# Date : 03/15/2025
# Description : This program is a file search program that searches for a file in a directory and its subdirectories.

import os
import hashlib

def menu():
    """Displays the menu and handles user choices."""
    while True:
        print("\n--- File Duplicate Finder ---")
        print("1. Enter directory to search")
        print("2. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            directory = input("Enter the directory path: ").strip()
            if os.path.isdir(directory):
                find_duplicates(directory)
            else:
                print("⚠ Invalid directory. Please try again.")
        elif choice == "2":
            print("👋 Exiting program.")
            break
        else:
            print("⚠ Invalid choice! Please enter 1 or 2.")

def find_duplicates(directory):
    """Searches for duplicate files by name and content using a checksum."""
    file_map = {}  # Stores file names and paths
    duplicates = {}  # Stores files with duplicate names

    print(f"\n🔍 Searching for duplicate files in: {directory}")

    # Step 1: Find files with the same name
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file in file_map:
                file_map[file].append(file_path)
            else:
                file_map[file] = [file_path]

    # Filter files that appear more than once
    duplicates = {name: paths for name, paths in file_map.items() if len(paths) > 1}

    if not duplicates:
        print("✅ No duplicate file names found.")
        return

    print("\n📌 Duplicate File Names Found:")
    for name, paths in duplicates.items():
        print(f"📝 {name}:")
        for path in paths:
            print(f"   ➡ {path}")

    # Step 2: Compare files by checksum
    identical_files = {}
    for name, paths in duplicates.items():
        identical_files.update(compare_files(paths))

    if identical_files:
        print("\n✅ Identical Files Based on Checksum:")
        for checksum, paths in identical_files.items():
            print(f"🔑 {checksum[:10]}...:")
            for path in paths:
                print(f"   ➡ {path}")
    else:
        print("\n⚠ No completely identical files found.")

def compare_files(file_paths):
    """Compares files using SHA-256 checksum to identify identical files."""
    file_hashes = {}  # Stores checksum as key and list of file paths
    identical_files = {}

    for file in file_paths:
        checksum = get_checksum(file)
        if checksum:
            if checksum in file_hashes:
                file_hashes[checksum].append(file)
            else:
                file_hashes[checksum] = [file]

    return {checksum: paths for checksum, paths in file_hashes.items() if len(paths) > 1}

def get_checksum(file_path):
    """Calculates the SHA-256 checksum of a file."""
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()
    except (PermissionError, FileNotFoundError):
        return None

if __name__ == "__main__":
    menu()
