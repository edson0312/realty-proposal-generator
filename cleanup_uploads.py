#!/usr/bin/env python3
"""
Cleanup script to remove old files from the uploads folder.
Run this script to clean up any existing generated PDFs and uploaded images.
"""
import os
import shutil
from datetime import datetime

def cleanup_uploads_folder(uploads_path='uploads'):
    """
    Clean up the uploads folder by removing all files.
    
    Args:
        uploads_path: Path to the uploads folder
    """
    if not os.path.exists(uploads_path):
        print(f"✓ Uploads folder '{uploads_path}' does not exist. Nothing to clean.")
        return
    
    print(f"Cleaning up uploads folder: {uploads_path}")
    
    # Count files
    file_count = 0
    total_size = 0
    
    for root, dirs, files in os.walk(uploads_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                file_size = os.path.getsize(file_path)
                total_size += file_size
                file_count += 1
            except Exception as e:
                print(f"  ⚠ Could not get size of {file}: {e}")
    
    if file_count == 0:
        print("✓ Uploads folder is already empty.")
        return
    
    print(f"  Found {file_count} file(s) totaling {total_size / 1024:.2f} KB")
    
    # Ask for confirmation
    response = input(f"\nDo you want to delete all {file_count} file(s)? (yes/no): ").strip().lower()
    
    if response not in ['yes', 'y']:
        print("✗ Cleanup cancelled.")
        return
    
    # Delete all files
    deleted_count = 0
    error_count = 0
    
    for root, dirs, files in os.walk(uploads_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                os.remove(file_path)
                deleted_count += 1
                print(f"  ✓ Deleted: {file}")
            except Exception as e:
                error_count += 1
                print(f"  ✗ Error deleting {file}: {e}")
    
    print(f"\n{'='*60}")
    print(f"Cleanup Summary:")
    print(f"  Files deleted: {deleted_count}")
    print(f"  Errors: {error_count}")
    print(f"  Space freed: {total_size / 1024:.2f} KB")
    print(f"{'='*60}")
    
    if deleted_count > 0:
        print("\n✓ Cleanup completed successfully!")
    else:
        print("\n⚠ No files were deleted.")

def main():
    """Main function."""
    print("="*60)
    print("Uploads Folder Cleanup Script")
    print("="*60)
    print("\nThis script will remove all files from the uploads folder.")
    print("Generated PDFs are now created in temporary storage and")
    print("automatically deleted after download, so these files are")
    print("no longer needed.\n")
    
    cleanup_uploads_folder()
    
    print("\nNote: The uploads folder will remain empty going forward.")
    print("All generated PDFs are now handled in temporary storage.")

if __name__ == '__main__':
    main()

