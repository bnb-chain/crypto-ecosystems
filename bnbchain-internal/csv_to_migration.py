#!/usr/bin/env python3
"""
CSV to Migration File Converter
Converts the cleaned sheet_with_status.csv into a migration file for the crypto-ecosystems project.
"""

import csv
import os
from datetime import datetime
from pathlib import Path

def clean_github_url(url):
    """Clean GitHub URL to remove query parameters and fragments."""
    if not url or url == '-':
        return None
    
    # Remove query parameters and fragments
    base_url = url.split('?')[0].split('#')[0]
    
    # Handle special cases
    if 'github.com/settings/applications' in base_url:
        return None  # Skip GitHub settings URLs
    if 'github.com/features/copilot' in base_url:
        return None  # Skip GitHub features URLs
    if 'github.com/Coinsult/Audits' in base_url:
        return None  # Skip audit PDF URLs
    if 'github.com/slowmist/Knowledge-Base' in base_url:
        return None  # Skip audit report URLs
    if 'github.com/bnb-chain/bsc/blob/master/cmd/faucet' in base_url:
        return None  # Skip BNB Chain internal URLs
    
    return base_url

def extract_repo_info(github_url):
    """Extract repository information from GitHub URL."""
    if not github_url:
        return None, None
    
    # Handle different GitHub URL formats
    if github_url.startswith('https://github.com/'):
        parts = github_url.replace('https://github.com/', '').split('/')
        if len(parts) >= 2:
            owner = parts[0]
            repo = parts[1]
            return owner, repo
    
    return None, None

def generate_migration_content(csv_data):
    """Generate migration file content from CSV data."""
    lines = []
    
    # Add header comment
    lines.append("-- Migration: Add BNB Chain repositories")
    lines.append(f"-- Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"-- Total repositories: {len(csv_data)}")
    lines.append("")
    
    # Add ecosystem if not exists (optional, since bnb-chain should already exist)
    lines.append("-- Ensure bnb-chain ecosystem exists")
    lines.append("ecoadd bnb-chain")
    lines.append("")
    
    # Add repositories
    lines.append("-- Add repositories to bnb-chain ecosystem")
    
    for row in csv_data:
        name = row.get('Name', '').strip()
        github_link = row.get('Github Link', '').strip()
        
        if not name or not github_link:
            continue
        
        # Clean the GitHub URL
        clean_url = clean_github_url(github_link)
        if not clean_url:
            continue
        
        # Extract owner and repo
        owner, repo = extract_repo_info(clean_url)
        if not owner or not repo:
            continue
        
        # Create the repadd command
        # Use the project name as a tag/description
        tag = name.replace(' ', '-').replace(',', '').replace('(', '').replace(')', '')
        tag = ''.join(c for c in tag if c.isalnum() or c in '-_')
        
        repadd_line = f"repadd bnb-chain {clean_url} #{tag}"
        lines.append(repadd_line)
    
    lines.append("")
    lines.append("-- Migration completed successfully!")
    
    return '\n'.join(lines)

def main():
    """Main function to convert CSV to migration file."""
    # Input CSV file
    csv_path = "sheet_with_status.csv"
    
    # Check if CSV exists
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found!")
        print("Make sure the CSV file is in the same directory as this script.")
        return
    
    # Read CSV data
    csv_data = []
    try:
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            csv_data = list(reader)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return
    
    print(f"Found {len(csv_data)} rows in CSV")
    
    # Filter only REPO status entries
    repo_data = [row for row in csv_data if row.get('Link Status', '').strip() == 'REPO']
    print(f"Found {len(repo_data)} repositories to add")
    
    if not repo_data:
        print("No repositories found with REPO status!")
        return
    
    # Generate migration content
    migration_content = generate_migration_content(repo_data)
    
    # Create migrations directory if it doesn't exist
    migrations_dir = Path("../migrations")
    migrations_dir.mkdir(exist_ok=True)
    
    # Generate migration filename with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%dT%H%M%S")
    migration_filename = f"{timestamp}_add_bnb_chain_repos"
    migration_path = migrations_dir / migration_filename
    
    # Write migration file
    try:
        with open(migration_path, 'w', encoding='utf-8') as file:
            file.write(migration_content)
        
        print(f"\n✅ Migration file created successfully!")
        print(f"📁 Location: {migration_path}")
        print(f"📊 Repositories: {len(repo_data)}")
        print(f"🔗 Sample entries:")
        
        # Show first few entries as preview
        for i, row in enumerate(repo_data[:5]):
            name = row.get('Name', '').strip()
            github_link = clean_github_url(row.get('Github Link', '').strip())
            if github_link:
                print(f"   - {name} -> {github_link}")
        
        if len(repo_data) > 5:
            print(f"   ... and {len(repo_data) - 5} more")
        
        print(f"\n📝 Migration file preview:")
        print("=" * 50)
        print(migration_content[:500] + "..." if len(migration_content) > 500 else migration_content)
        print("=" * 50)
        
    except Exception as e:
        print(f"Error writing migration file: {e}")

if __name__ == "__main__":
    main()
