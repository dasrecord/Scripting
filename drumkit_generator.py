#!/usr/bin/env python3
"""
Simple Randomized Drum Kit Generator

Run this script and it will ask you for:
- Input folder (where your samples are)
- Output folder (where to create drum kits)
- Number of files per kit
- File extensions to include
"""

import os
import random
import shutil
from pathlib import Path
from datetime import datetime


def get_audio_files(input_dir, extensions):
    """Find all audio files in the input directory and subdirectories."""
    audio_files = []
    
    # Convert extensions to lowercase for comparison
    extensions = [ext.lower().strip('.') for ext in extensions]
    
    print(f"Searching for audio files in: {input_dir}")
    
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            file_path = os.path.join(root, file)
            # Get file extension without the dot
            file_ext = os.path.splitext(file)[1].lower().strip('.')
            
            if file_ext in extensions:
                audio_files.append(file_path)
    
    return audio_files


def create_drum_kit(audio_files, output_dir, max_files, use_symlinks=False):
    """Create a drum kit by copying or symlinking random audio files."""
    if not audio_files:
        print("No audio files found!")
        return False
    
    # Create timestamp for unique folder name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    kit_name = f"DrumKit_{timestamp}"
    kit_dir = os.path.join(output_dir, kit_name)
    
    # Create the kit directory
    os.makedirs(kit_dir, exist_ok=True)
    
    # Select random files (up to max_files)
    num_files = min(len(audio_files), max_files)
    selected_files = random.sample(audio_files, num_files)
    
    print(f"\nCreating drum kit: {kit_name}")
    action = "Creating symlinks to" if use_symlinks else "Copying"
    print(f"{action} {num_files} files...")
    
    # Copy or symlink files to kit directory
    for i, source_file in enumerate(selected_files, 1):
        # Get just the filename from the full path
        filename = os.path.basename(source_file)
        # Add number prefix to avoid name conflicts
        new_filename = f"{i:02d}_{filename}"
        dest_path = os.path.join(kit_dir, new_filename)
        
        try:
            if use_symlinks:
                os.symlink(source_file, dest_path)
            else:
                shutil.copy2(source_file, dest_path)
            print(f"  {i:2d}. {filename}")
        except Exception as e:
            print(f"  Error {'linking' if use_symlinks else 'copying'} {filename}: {e}")
            return False
    
    print(f"\n✓ Drum kit created successfully!")
    print(f"  Location: {kit_dir}")
    return True


def main():
    print("=" * 60)
    print("          Randomized Drum Kit Generator")
    print("=" * 60)
    print()
    
    # Get input directory
    while True:
        input_dir = input("Enter the path to your sample library folder: ").strip()
        # Remove quotes if present (from drag & drop)
        input_dir = input_dir.strip('\'"')
        
        print(f"Checking path: '{input_dir}'")
        print(f"Path exists: {os.path.exists(input_dir)}")
        print(f"Is directory: {os.path.isdir(input_dir) if os.path.exists(input_dir) else 'N/A'}")
        
        if os.path.exists(input_dir) and os.path.isdir(input_dir):
            break
        print("That folder doesn't exist. Please try again.")
        
        # Suggest the parent directory if this one doesn't exist
        parent_dir = os.path.dirname(input_dir)
        if os.path.exists(parent_dir):
            print(f"Hint: Parent directory exists: {parent_dir}")
            print("Available folders in that directory:")
            try:
                items = os.listdir(parent_dir)
                folders = [item for item in items if os.path.isdir(os.path.join(parent_dir, item))]
                for folder in sorted(folders):
                    print(f"  - {folder}")
            except Exception as e:
                print(f"  Could not list directory: {e}")
            print("Maybe try one of these paths, or check the folder name spelling.")
    
    # Get output directory
    output_dir = input("Enter the output folder (where to save drum kits): ").strip()
    # Remove quotes if present (from drag & drop)
    output_dir = output_dir.strip('\'"')
    if not os.path.exists(output_dir):
        print(f"Creating output directory: {output_dir}")
        os.makedirs(output_dir, exist_ok=True)
    
    # Get number of files per kit
    while True:
        try:
            max_files = int(input("How many files per drum kit? (e.g., 10): ").strip())
            if max_files > 0:
                break
            print("Please enter a number greater than 0.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Get file extensions
    print("Which audio file types to include?")
    print("Default: wav, aif, aiff, mp3, flac")
    extensions_input = input("Press Enter for default, or type extensions (e.g., wav mp3 aif): ").strip()
    
    if extensions_input:
        extensions = extensions_input.split()
    else:
        extensions = ['wav', 'aif', 'aiff', 'mp3', 'flac']
    
    print(f"\nLooking for files with extensions: {', '.join(extensions)}")
    
    # Ask about copying vs symlinking
    print("\nFile handling options:")
    print("1. Copy files (duplicates files, uses more disk space)")
    print("2. Create symbolic links (points to originals, saves disk space)")
    while True:
        choice = input("Choose option (1 or 2): ").strip()
        if choice in ['1', '2']:
            use_symlinks = choice == '2'
            break
        print("Please enter 1 or 2.")
    
    print("-" * 60)
    
    # Find all audio files
    audio_files = get_audio_files(input_dir, extensions)
    
    if not audio_files:
        print("No audio files found!")
        print(f"Searched for: {', '.join(extensions)}")
        print("Make sure your sample library contains files with these extensions.")
        return
    
    print(f"Found {len(audio_files)} audio files")
    
    # Ask how many kits to generate
    while True:
        try:
            num_kits = int(input(f"\nHow many drum kits to generate? (1): ").strip() or "1")
            if num_kits > 0:
                break
            print("Please enter a number greater than 0.")
        except ValueError:
            print("Please enter a valid number.")
    
    print("\n" + "=" * 60)
    
    # Generate drum kits
    successful_kits = 0
    for kit_num in range(num_kits):
        if create_drum_kit(audio_files, output_dir, max_files, use_symlinks):
            successful_kits += 1
        
        # Wait a second between kits to ensure unique timestamps
        if kit_num < num_kits - 1:
            import time
            time.sleep(1)
    
    print("=" * 60)
    print(f"Generated {successful_kits}/{num_kits} drum kits successfully!")
    print("Done!")


if __name__ == "__main__":
    main()