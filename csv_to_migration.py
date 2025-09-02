#!/usr/bin/env python3
"""
Script to convert sheet2.csv into a migration file with the format:
repadd "BNB Chain" https://github.com/... #ProjectName
"""

import csv
import sys
from datetime import datetime

def csv_to_migration(csv_file_path, output_file_path):
    """
    Convert CSV file to migration format, handling duplicates
    
    Args:
        csv_file_path (str): Path to the input CSV file
        output_file_path (str): Path to the output migration file
    """
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8-sig') as csvfile:  # Use utf-8-sig to handle BOM
            reader = csv.DictReader(csvfile)
            
            # Print column names for debugging
            print(f"Found columns: {reader.fieldnames}")
            
            # Track seen entries to handle duplicates
            seen_entries = set()
            duplicate_count = 0
            
            with open(output_file_path, 'w', encoding='utf-8') as outfile:
                count = 0
                for row_num, row in enumerate(reader, 1):
                    # Extract the required fields - use project_name for the repo URL
                    repo_url = row.get('project_name', '').strip()
                    
                    # Try to get the Name column, handling potential BOM
                    project_name = None
                    if 'Name' in row:
                        project_name = row['Name'].strip()
                    elif '\ufeffName' in row:  # Handle BOM character
                        project_name = row['\ufeffName'].strip()
                    
                    # Skip rows with missing data
                    if not repo_url or not project_name:
                        print(f"Skipping row {row_num}: repo_url='{repo_url}', project_name='{project_name}'")
                        continue
                    
                    # Create a unique identifier for this entry
                    entry_id = f'{project_name}|{repo_url}'
                    
                    # Check for duplicates
                    if entry_id in seen_entries:
                        print(f"Skipping duplicate row {row_num}: {project_name} - {repo_url}")
                        duplicate_count += 1
                        continue
                    
                    # Add to seen entries
                    seen_entries.add(entry_id)
                    
                    # Clean up the project name for the comment
                    # Remove special characters and replace spaces with hyphens
                    clean_name = project_name.replace(' ', '-').replace('&', 'and')
                    clean_name = ''.join(c for c in clean_name if c.isalnum() or c == '-')
                    
                    # Format the line according to the specified format
                    line = f'repadd "BNB Chain" {repo_url} #{clean_name}\n'
                    outfile.write(line)
                    count += 1
                
                print(f"Successfully processed {count} unique projects")
                if duplicate_count > 0:
                    print(f"Skipped {duplicate_count} duplicate entries")
            
            print(f"Migration file created successfully: {output_file_path}")
            
    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)

def main():
    """Main function"""
    csv_file = "sheet2.csv"
    output_file = "migration_output.txt"
    
    # Check if CSV file exists
    try:
        with open(csv_file, 'r') as f:
            pass
    except FileNotFoundError:
        print(f"Error: {csv_file} not found in current directory.")
        print("Please make sure the CSV file is in the same directory as this script.")
        sys.exit(1)
    
    # Convert CSV to migration format
    csv_to_migration(csv_file, output_file)
    
    # Display preview of the output
    print("\nPreview of generated migration file:")
    print("-" * 50)
    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for i, line in enumerate(lines[:10]):  # Show first 10 lines
                print(f"{i+1:2d}: {line.strip()}")
            if len(lines) > 10:
                print(f"... and {len(lines) - 10} more lines")
    except Exception as e:
        print(f"Error reading output file: {e}")

if __name__ == "__main__":
    main()
