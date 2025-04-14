#!/usr/bin/env python3
"""
CFC Number v1.0
A simple script to automate icon tagging for Telegram number lists.
"""

import os
import sys
import datetime
import re
from typing import List, Dict, Tuple, Optional

# Define the preset icons
ICONS: Dict[int, str] = {
    1: "🐼",
    2: "🍚",
    3: "🥷",
    4: "🦎",
    5: "🔋",
    6: "🔥",
    7: "👮",
    8: "🚗",
    9: "✨"
}

# Icon names for display
ICON_NAMES: Dict[int, str] = {
    1: "PANDA",
    2: "NASI",
    3: "NINJA",
    4: "KADAL",
    5: "BATERAI",
    6: "API",
    7: "POLISI",
    8: "MOBIL",
    9: "BINTANG"
}

def clear_screen() -> None:
    """Clear the terminal screen for better UX."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_welcome() -> None:
    """Print a welcome message with basic instructions."""
    clear_screen()
    print("=" * 60)
    print("🧩 Welcome to CFC Number v1.0")
    print("=" * 60)
    print("This script helps you organize Telegram number lists with automatic")
    print("icon tagging and grouping for cleaner, more readable layouts.")
    print("\n✨ Features:")
    print(" • Select an icon (1-9) from a preset list")
    print(" • Import links from a .txt file")
    print(" • Auto-split into groups of 8 entries")
    print(" • Save results with icon and date stamps")
    print("=" * 60)
    print()

def get_icon_choice() -> str:
    """Prompt user to select an icon from the preset list."""
    print("Available icons:")
    for num, icon in ICONS.items():
        print(f"{num}. {icon}")
    
    while True:
        try:
            choice = int(input("\nSelect an icon (1-9): "))
            if 1 <= choice <= 9:
                return ICONS[choice]
            else:
                print("Please select a number between 1 and 9.")
        except ValueError:
            print("Please enter a valid number.")

def get_input_file() -> str:
    """Get the input file path from the user and validate it."""
    while True:
        file_path = input("\nEnter the path to your .txt file with links/numbers: ")
        
        # Check if file exists
        if not os.path.exists(file_path):
            print("❌ File not found. Please enter a valid file path.")
            continue
            
        # Check if it's a .txt file
        if not file_path.lower().endswith('.txt'):
            print("❌ Only .txt files are supported. Please select a .txt file.")
            continue
            
        return file_path

def read_links(file_path: str) -> List[str]:
    """Read links/numbers from the input file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Read all lines and strip whitespace
            links = [line.strip() for line in file.readlines() if line.strip()]
        return links
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        sys.exit(1)

def split_into_groups(links: List[str], group_size: int = 8) -> List[List[str]]:
    """Split the list into groups of specified size."""
    return [links[i:i + group_size] for i in range(0, len(links), group_size)]

def format_groups(groups: List[List[str]], icon: str, icon_id: int = 1, link_format: str = '+', part_number: str = "1") -> List[str]:
    """Format each group with the selected icon and date."""
    formatted_groups = []
    icon_name = ICON_NAMES.get(icon_id, "ICON")
    
    for group in groups:
        formatted_lines = []
        for line in group:
            formatted_lines.append(f"{link_format}{line} {icon} Part_{part_number}")
        formatted_group = '\n'.join(formatted_lines) + '\n\n'
        formatted_groups.append(formatted_group)
    
    return formatted_groups

def save_results(formatted_groups: List[str], icon_id: int, link_format: str = '+', part_number: str = "1") -> str:
    """Save the formatted groups to a new file."""
    # Create output directory if it doesn't exist
    if not os.path.exists("output"):
        os.makedirs("output")
    
    # Create output filename with icon name and date
    today = datetime.datetime.now().strftime("%d_%m_%y")
    icon_name = ICON_NAMES.get(icon_id, "ICON")
    format_prefix = 'A_' if link_format == '+' else 'B_'
    output_filename = f"{format_prefix}{icon_name}_{today}_Part_{part_number}.txt"
    output_path = os.path.join("output", output_filename)
    
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(''.join(formatted_groups))
        return output_path
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        sys.exit(1)

def extract_part_number(file_path: str) -> str:
    """Extract part number from filename if available."""
    filename = os.path.basename(file_path)
    part_match = re.search(r'_Part_(\d+)', filename)
    return part_match.group(1) if part_match else "unknown"

def main() -> None:
    """Main function to run the script."""
    print_welcome()
    
    # Get user inputs
    icon_id = 1
    selected_icon = ICONS[icon_id]
    input_file = get_input_file()
    
    # Process the file
    print("\n⏳ Processing your file...")
    links = read_links(input_file)
    
    # Check if file has contents
    if not links:
        print("❌ The input file is empty. Please provide a file with links/numbers.")
        sys.exit(1)
    
    # Get part number from filename
    part_number = extract_part_number(input_file)
    
    # Use default format (+)
    link_format = "+"
    
    # Split and format
    groups = split_into_groups(links)
    formatted_groups = format_groups(groups, selected_icon, icon_id, link_format, part_number)
    
    # Save results
    output_file = save_results(formatted_groups, icon_id, link_format, part_number)
    
    # Show summary
    print("\n✅ Processing complete!")
    print(f"📊 Total entries processed: {len(links)}")
    print(f"📦 Split into {len(groups)} groups of 8")
    print(f"💾 Results saved to: {output_file}")
    
    print("\nThanks for using CFC Number! 🧩")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user. Goodbye! 👋")
        sys.exit(0)
