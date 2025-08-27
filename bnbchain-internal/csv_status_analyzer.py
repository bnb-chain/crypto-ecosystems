#!/usr/bin/env python3
"""
CSV Status Analyzer
This script analyzes sheet.csv and determines the Link Status for each GitHub link,
then creates sheet_with_status.csv format.
"""

import csv
import os
import time
import requests
import re
from pathlib import Path
from typing import List, Dict, Optional
from urllib.parse import urlparse

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✓ Loaded .env file")
except ImportError:
    print("⚠ python-dotenv not installed, using system environment variables")
    # Fallback: manually load .env file
    env_file = Path('.env')
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value
        print("✓ Loaded .env file manually")

class CSVStatusAnalyzer:
    def __init__(self, input_csv: str = "sheet.csv", output_csv: str = "sheet_with_status.csv"):
        self.input_csv = input_csv
        self.output_csv = output_csv
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.headers = {}
        
        if self.github_token:
            self.headers['Authorization'] = f'token {self.github_token}'
            print("✓ GitHub token found - higher rate limits available")
        else:
            print("⚠ No GitHub token found - limited to 60 requests/hour")
    
    def analyze_github_url(self, url: str) -> str:
        """Analyze a GitHub URL and determine its status."""
        if not url or url == '-' or url.strip() == '':
            return 'INVALID'
        
        # Clean the URL
        url = url.strip()
        
        # Check for invalid/malformed URLs
        if not url.startswith('http'):
            return 'INVALID'
        
        # Parse the URL
        try:
            parsed = urlparse(url)
            if parsed.netloc != 'github.com':
                return 'INVALID'
        except:
            return 'INVALID'
        
        # Extract path components
        path_parts = parsed.path.strip('/').split('/')
        
        if len(path_parts) == 0:
            return 'INVALID'
        
        if len(path_parts) == 1:
            # Just username: github.com/username
            username = path_parts[0]
            if self.is_valid_github_user(username):
                # Check if it's an organization
                if self.is_github_organization(username):
                    return 'ORG'
                else:
                    return 'USER'
            else:
                return 'INVALID'
        
        elif len(path_parts) == 2:
            # username/repo: github.com/username/repo
            username, repo = path_parts[0], path_parts[1]
            
            # Check if it's a valid repository
            if self.is_valid_github_repo(username, repo):
                return 'REPO'
            elif self.is_valid_github_user(username):
                # Check if it's an organization
                if self.is_github_organization(username):
                    return 'ORG'
                else:
                    return 'USER'
            else:
                return 'INVALID'
        
        elif len(path_parts) > 2:
            # username/repo/path: github.com/username/repo/path
            username, repo = path_parts[0], path_parts[1]
            
            if self.is_valid_github_repo(username, repo):
                return 'REPO'
            elif self.is_valid_github_user(username):
                # Check if it's an organization
                if self.is_github_organization(username):
                    return 'ORG'
                else:
                    return 'USER'
            else:
                return 'INVALID'
        
        return 'INVALID'
    
    def is_valid_github_user(self, username: str) -> bool:
        """Check if a GitHub username is valid."""
        if not username or username == '':
            return False
        
        # Skip obvious invalid usernames
        if username in ['settings', 'features', '?', '']:
            return False
        
        # Check via GitHub API
        url = f"https://api.github.com/users/{username}"
        
        try:
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                return True
            elif response.status_code == 404:
                return False
            elif response.status_code == 403:
                print(f"  ⚠️ Rate limit hit while checking user {username}")
                return False  # Assume invalid to be safe
            else:
                print(f"  ⚠️ API error {response.status_code} for user {username}")
                return False
                
        except Exception as e:
            print(f"  ⚠️ Error checking user {username}: {e}")
            return False
    
    def is_github_organization(self, username: str) -> bool:
        """Check if a GitHub username is an organization."""
        if not username or username == '':
            return False
        
        # Check via GitHub API
        url = f"https://api.github.com/users/{username}"
        
        try:
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                user_data = response.json()
                return user_data.get('type') == 'Organization'
            else:
                return False
                
        except Exception as e:
            print(f"  ⚠️ Error checking org status for {username}: {e}")
            return False
    
    def is_valid_github_repo(self, username: str, repo: str) -> bool:
        """Check if a GitHub repository is valid."""
        if not username or not repo:
            return False
        
        # Skip obvious invalid repos
        if repo in ['', '?', 'no-public-repos']:
            return False
        
        # Check via GitHub API
        url = f"https://api.github.com/repos/{username}/{repo}"
        
        try:
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                return True
            elif response.status_code == 404:
                return False
            elif response.status_code == 403:
                print(f"  ⚠️ Rate limit hit while checking repo {username}/{repo}")
                return False  # Assume invalid to be safe
            else:
                print(f"  ⚠️ API error {response.status_code} for repo {username}/{repo}")
                return False
                
        except Exception as e:
            print(f"  ⚠️ Error checking repo {username}/{repo}: {e}")
            return False
    
    def process_csv(self):
        """Process the input CSV and create the output CSV with status."""
        print(f"Processing {self.input_csv}...")
        
        if not Path(self.input_csv).exists():
            print(f"❌ Input CSV file not found: {self.input_csv}")
            return
        
        # Read input CSV
        rows = []
        with open(self.input_csv, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
        
        print(f"Found {len(rows)} entries to process")
        
        # Process each row
        processed_rows = []
        total_processed = 0
        
        for i, row in enumerate(rows, 1):
            github_link = row.get('Github Link', '')
            project_name = row.get('Name', '')
            
            print(f"\n[{i}/{len(rows)}] Processing: {project_name}")
            print(f"  URL: {github_link}")
            
            # Analyze the GitHub URL
            link_status = self.analyze_github_url(github_link)
            
            # Create new row with status
            new_row = {
                'Name': project_name,
                'Chain': row.get('Chain', 'bnb-chain'),
                'Github Link': github_link,
                'Link Status': link_status
            }
            
            processed_rows.append(new_row)
            total_processed += 1
            
            print(f"  Status: {link_status}")
            
            # Rate limiting for unauthenticated requests
            if not self.github_token:
                print("  Waiting 1 second before next request...")
                time.sleep(1)
            
            # Progress update
            if i % 50 == 0:
                print(f"\n--- Processed {i}/{len(rows)} entries ({i/len(rows)*100:.1f}%) ---")
                
                if not self.github_token:
                    print("⚠️ Rate limit approaching. Consider setting GITHUB_TOKEN.")
                    response = input("Continue? (y/n): ").lower().strip()
                    if response not in ['y', 'yes']:
                        print("Stopping. You can resume later.")
                        break
        
        # Write output CSV
        print(f"\nWriting results to {self.output_csv}...")
        
        with open(self.output_csv, 'w', encoding='utf-8', newline='') as file:
            fieldnames = ['Name', 'Chain', 'Github Link', 'Link Status']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(processed_rows)
        
        # Summary
        print(f"\n{'='*60}")
        print("PROCESSING COMPLETED!")
        print(f"{'='*60}")
        print(f"Total entries processed: {total_processed}")
        print(f"Results saved to: {self.output_csv}")
        
        # Status summary
        status_counts = {}
        for row in processed_rows:
            status = row['Link Status']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        print(f"\nStatus Summary:")
        for status, count in sorted(status_counts.items()):
            print(f"  {status}: {count}")
        
        # Recommendations
        print(f"\nRecommendations:")
        if 'INVALID' in status_counts:
            print(f"  - {status_counts['INVALID']} entries have invalid or non-GitHub links")
        if 'USER' in status_counts:
            print(f"  - {status_counts['USER']} entries are GitHub users (can be processed by repo_gatherer.py)")
        if 'ORG' in status_counts:
            print(f"  - {status_counts['ORG']} entries are GitHub organizations (can be processed by repo_gatherer.py)")
        if 'REPO' in status_counts:
            print(f"  - {status_counts['REPO']} entries are valid GitHub repositories")

def main():
    """Main function."""
    print("CSV Status Analyzer")
    print("=" * 40)
    
    analyzer = CSVStatusAnalyzer()
    analyzer.process_csv()

if __name__ == "__main__":
    main()
