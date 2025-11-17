#!/usr/bin/env python3
"""
Script to extract .txt files from TEXT-20251117T065242Z-1-001.zip
Renames duplicate files by appending '_from_zip' before the extension
Logs all extracted filenames and indicates which were renamed
"""

import os
import zipfile
from pathlib import Path
from typing import List, Tuple

def extract_txt_files(zip_path: str, target_dir: str) -> Tuple[List[str], List[str]]:
    """
    Extract all .txt files from the zip archive to the target directory.
    
    Args:
        zip_path: Path to the ZIP file
        target_dir: Directory to extract files to
    
    Returns:
        Tuple of (all_extracted_files, renamed_files)
    """
    extracted_files = []
    renamed_files = []
    
    # Get list of existing .txt files in target directory
    existing_files = set()
    for file in os.listdir(target_dir):
        if file.endswith('.txt'):
            existing_files.add(file)
    
    print(f"Found {len(existing_files)} existing .txt files in repository")
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # Get all .txt files from the ZIP
        txt_files = [f for f in zip_ref.namelist() if f.endswith('.txt')]
        print(f"Found {len(txt_files)} .txt files in ZIP archive")
        
        for file_path in txt_files:
            # Get just the filename (not the full path within ZIP)
            original_filename = os.path.basename(file_path)
            
            # Check if file already exists
            if original_filename in existing_files:
                # Rename by adding '_from_zip' before the extension
                name_without_ext = original_filename[:-4]  # Remove '.txt'
                new_filename = f"{name_without_ext}_from_zip.txt"
                renamed_files.append((original_filename, new_filename))
                target_filename = new_filename
            else:
                target_filename = original_filename
            
            # Extract the file
            file_data = zip_ref.read(file_path)
            target_path = os.path.join(target_dir, target_filename)
            
            with open(target_path, 'wb') as f:
                f.write(file_data)
            
            extracted_files.append(target_filename)
    
    return extracted_files, renamed_files

def generate_log(extracted_files: List[str], renamed_files: List[Tuple[str, str]], log_path: str):
    """
    Generate a log file with extraction results.
    
    Args:
        extracted_files: List of all extracted filenames
        renamed_files: List of tuples (original_name, new_name) for renamed files
        log_path: Path to write the log file
    """
    with open(log_path, 'w') as log:
        log.write("ZIP EXTRACTION LOG\n")
        log.write("=" * 80 + "\n\n")
        
        log.write(f"Total files extracted: {len(extracted_files)}\n")
        log.write(f"Files renamed due to duplication: {len(renamed_files)}\n\n")
        
        if renamed_files:
            log.write("RENAMED FILES (due to existing file with same name):\n")
            log.write("-" * 80 + "\n")
            for original, new in sorted(renamed_files):
                log.write(f"  {original} -> {new}\n")
            log.write("\n")
        
        log.write("ALL EXTRACTED FILES:\n")
        log.write("-" * 80 + "\n")
        for filename in sorted(extracted_files):
            # Mark renamed files with an asterisk
            is_renamed = any(new == filename for _, new in renamed_files)
            marker = " *" if is_renamed else ""
            log.write(f"  {filename}{marker}\n")
        
        if renamed_files:
            log.write("\n")
            log.write("* = File was renamed due to duplicate filename\n")

def main():
    # Paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    zip_file = os.path.join(script_dir, "TEXT-20251117T065242Z-1-001.zip")
    target_dir = script_dir
    log_file = os.path.join(script_dir, "extraction_log.txt")
    
    # Verify ZIP file exists
    if not os.path.exists(zip_file):
        print(f"ERROR: ZIP file not found: {zip_file}")
        return 1
    
    print(f"Starting extraction from: {zip_file}")
    print(f"Target directory: {target_dir}")
    print()
    
    # Extract files
    extracted_files, renamed_files = extract_txt_files(zip_file, target_dir)
    
    # Generate log
    generate_log(extracted_files, renamed_files, log_file)
    
    # Print summary
    print()
    print("=" * 80)
    print("EXTRACTION COMPLETE")
    print("=" * 80)
    print(f"Total files extracted: {len(extracted_files)}")
    print(f"Files renamed due to duplication: {len(renamed_files)}")
    print(f"Log file created: {log_file}")
    
    if renamed_files:
        print()
        print("Sample renamed files (showing first 10):")
        for original, new in renamed_files[:10]:
            print(f"  {original} -> {new}")
        if len(renamed_files) > 10:
            print(f"  ... and {len(renamed_files) - 10} more")
    
    return 0

if __name__ == "__main__":
    exit(main())
