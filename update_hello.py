#!/usr/bin/env python3
"""
JSON Data Updater Script
Updates hello.json with data from either paid.json or Free.json based on user choice.
"""

import json
import sys
import os
from typing import Dict, Any

# ============================================================================
# CONFIGURATION - Change this value to switch between data sources
# ============================================================================
# Set to "free" to use Free.json data
# Set to "paid" to use paid.json data
DATA_SOURCE = "free"  # Change this to "paid" when you want paid data
# ============================================================================

def load_json_file(filename: str) -> Dict[Any, Any]:
    """Load and return JSON data from a file."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: {filename} not found!")
        return {}
    except json.JSONDecodeError:
        print(f"Error: {filename} is not a valid JSON file!")
        return {}

def save_json_file(filename: str, data: Dict[Any, Any]) -> bool:
    """Save JSON data to a file with proper formatting."""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving {filename}: {e}")
        return False

def create_backup(filename: str) -> None:
    """Create a backup of the original file."""
    backup_name = f"{filename}.backup"
    try:
        with open(filename, 'r', encoding='utf-8') as original:
            with open(backup_name, 'w', encoding='utf-8') as backup:
                backup.write(original.read())
        print(f"✅ Backup created: {backup_name}")
    except Exception as e:
        print(f"⚠️  Warning: Could not create backup: {e}")

def display_source_info(data: Dict[Any, Any], source_name: str) -> None:
    """Display information about the source data."""
    print(f"\n📋 {source_name} contains:")
    for category, items in data.items():
        if isinstance(items, list):
            print(f"  • {category}: {len(items)} items")
        else:
            print(f"  • {category}: {type(items).__name__}")
    print()

def update_hello_json(source_choice: str) -> None:
    """Main function to update hello.json with chosen source data."""
    
    # File paths
    hello_file = "hello.json"
    source_files = {
        "free": "Free.json",
        "paid": "paid.json"
    }
    
    if source_choice not in source_files:
        print("❌ Invalid choice! Please choose 'free' or 'paid'")
        return
    
    source_file = source_files[source_choice]
    
    # Check if files exist
    if not os.path.exists(hello_file):
        print(f"❌ {hello_file} not found!")
        return
    
    if not os.path.exists(source_file):
        print(f"❌ {source_file} not found!")
        return
    
    print(f"🔄 Updating {hello_file} with data from {source_file}...")
    
    # Load source data
    source_data = load_json_file(source_file)
    if not source_data:
        return
    
    # Display source information
    display_source_info(source_data, source_file)
    
    # Create backup of hello.json
    create_backup(hello_file)
    
    # Update hello.json with source data
    if save_json_file(hello_file, source_data):
        print(f"✅ Successfully updated {hello_file} with data from {source_file}!")
        
        # Display summary
        total_items = sum(len(items) if isinstance(items, list) else 0 
                         for items in source_data.values())
        print(f"📊 Total wallpapers updated: {total_items}")
    else:
        print(f"❌ Failed to update {hello_file}")

def main():
    """Main function - uses configuration variable or command line."""
    print("🎨 JSON Data Updater")
    print("=" * 30)
    
    # Check if command line argument is provided
    if len(sys.argv) > 1:
        choice = sys.argv[1].lower()
        if choice in ['free', 'paid']:
            print(f"Using command line argument: {choice}")
            update_hello_json(choice)
        else:
            print("❌ Invalid argument! Use 'free' or 'paid'")
            print("Usage: python update_hello.py [free|paid]")
    else:
        # Use the configuration variable
        print(f"Using configured data source: {DATA_SOURCE}")
        print("(To change this, edit the DATA_SOURCE variable at the top of this file)")
        print()
        
        if DATA_SOURCE.lower() in ['free', 'paid']:
            update_hello_json(DATA_SOURCE.lower())
        else:
            print("❌ Invalid DATA_SOURCE configuration!")
            print("Please set DATA_SOURCE to either 'free' or 'paid' at the top of this file.")

if __name__ == "__main__":
    main() 
