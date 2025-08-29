#!/usr/bin/env python3
"""
Debug script to see what's happening with CSV parsing
"""

import csv
import sys

def debug_csv(csv_file_path):
    """Debug the CSV file to see what's happening"""
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            # Print the column names
            print(f"Column names: {reader.fieldnames}")
            print()
            
            # Read first few rows to see the data
            for i, row in enumerate(reader):
                if i >= 5:  # Only show first 5 rows
                    break
                    
                print(f"Row {i+1}:")
                print(f"  Name: '{row.get('Name', 'MISSING')}'")
                print(f"  Chain: '{row.get('Chain', 'MISSING')}'")
                print(f"  github_link: '{row.get('github_link', 'MISSING')}'")
                print(f"  project_name: '{row.get('project_name', 'MISSING')}'")
                print(f"  is_deployed_on_bsc: '{row.get('is_deployed_on_bsc', 'MISSING')}'")
                print()
                
                # Check if this is a BNB Chain project
                if row.get('Chain', '').strip().lower() == 'bnb-chain' and row.get('is_deployed_on_bsc', '').strip().upper() == 'TRUE':
                    print(f"  ✓ This is a BNB Chain project!")
                    print(f"  ✓ GitHub link: {row.get('github_link', 'MISSING')}")
                    print(f"  ✓ Project name: {row.get('Name', 'MISSING')}")
                    print()
            
    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)

def main():
    """Main function"""
    csv_file = "sheet2.csv"
    
    print("Debugging CSV file...")
    print("=" * 50)
    debug_csv(csv_file)

if __name__ == "__main__":
    main()
