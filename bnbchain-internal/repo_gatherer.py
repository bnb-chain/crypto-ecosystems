#!/usr/bin/env python3
"""
Repository Link Gatherer
This script takes GitHub user/organization links and gathers all their repositories into a CSV file.
"""

import csv
import json
import os
import time
import requests
from pathlib import Path
from typing import List, Dict, Optional
import re

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

class RepoGatherer:
    def __init__(self, output_csv: str = "gathered_repos.csv"):
        self.output_csv = output_csv
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.headers = {}
        
        if self.github_token:
            self.headers['Authorization'] = f'token {self.github_token}'
            print("✓ GitHub token found - higher rate limits available")
        else:
            print("⚠ No GitHub token found - limited to 60 requests/hour")
        
        # Initialize output CSV
        self.init_output_csv()
    
    def init_output_csv(self):
        """Initialize the output CSV with headers."""
        headers = [
            'Name',
            'Chain', 
            'Github Link',
            'Link Status',
            'Original Source',
            'Language',
            'Stars',
            'Forks',
            'Description'
        ]
        
        # Create CSV if it doesn't exist
        if not Path(self.output_csv).exists():
            with open(self.output_csv, 'w', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(headers)
            print(f"Created new CSV file: {self.output_csv}")
        else:
            print(f"Using existing CSV file: {self.output_csv}")
    
    def extract_github_username(self, github_url: str) -> Optional[str]:
        """Extract GitHub username from URL."""
        if not github_url or github_url == '-':
            return None
            
        patterns = [
            r'github\.com/([^/\s]+)/?$',
            r'github\.com/([^/\s]+)/[^/\s]+',
            r'github\.com/([^/\s]+)\?',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, github_url)
            if match:
                return match.group(1)
        
        return None
    
    def get_user_repos(self, username: str) -> List[Dict]:
        """Get all repositories for a GitHub user/organization."""
        repos = []
        page = 1
        per_page = 100  # Maximum allowed by GitHub API
        
        print(f"  Gathering repositories for {username}...")
        
        while True:
            url = f"https://api.github.com/users/{username}/repos"
            params = {
                'page': page,
                'per_page': per_page,
                'sort': 'updated',
                'direction': 'desc'
            }
            
            try:
                response = requests.get(url, headers=self.headers, params=params)
                
                if response.status_code == 200:
                    page_repos = response.json()
                    
                    # Validate that we got a list of repositories
                    if not isinstance(page_repos, list):
                        print(f"    ❌ Unexpected API response format: {type(page_repos)}")
                        print(f"    Response: {page_repos}")
                        break
                    
                    if not page_repos:  # No more repos
                        break
                    
                    # Validate each repo entry
                    valid_repos = []
                    for repo in page_repos:
                        if isinstance(repo, dict) and 'name' in repo and 'html_url' in repo:
                            valid_repos.append(repo)
                        else:
                            print(f"    ⚠️ Skipping invalid repo entry: {repo}")
                    
                    repos.extend(valid_repos)
                    print(f"    Page {page}: Found {len(valid_repos)} valid repos")
                    
                    if len(page_repos) < per_page:  # Last page
                        break
                    
                    page += 1
                    
                    # Rate limiting
                    if not self.github_token:
                        time.sleep(1)  # Be nice to GitHub API
                        
                elif response.status_code == 404:
                    print(f"    ❌ User/Organization '{username}' not found")
                    break
                elif response.status_code == 403:
                    print(f"    ❌ Rate limit exceeded!")
                    if not self.github_token:
                        print(f"    ⏰ Rate limit: 60 requests/hour for unauthenticated requests")
                        print(f"    💡 Set GITHUB_TOKEN environment variable for 5,000 requests/hour")
                        print(f"    ⏳ Wait about 1 hour before resuming, or get a GitHub token")
                    else:
                        print(f"    ⏰ Rate limit: 5,000 requests/hour for authenticated requests")
                        print(f"    ⏳ Wait about 1 hour before resuming")
                    break
                else:
                    print(f"    ❌ API error: {response.status_code}")
                    try:
                        error_data = response.json()
                        print(f"    Error details: {error_data}")
                    except:
                        print(f"    Error response: {response.text}")
                    break
                    
            except Exception as e:
                print(f"    ❌ Error fetching repos: {e}")
                break
        
        return repos
    
    def process_github_link(self, github_url: str, project_name: str = "") -> List[Dict]:
        """Process a GitHub link and return repository data."""
        username = self.extract_github_username(github_url)
        
        if not username:
            print(f"❌ Could not extract username from: {github_url}")
            return []
        
        print(f"Processing: {github_url}")
        print(f"Extracted username: {username}")
        
        # Get repositories
        repos = self.get_user_repos(username)
        
        if not repos:
            print(f"  No repositories found for {username}")
            return []
        
        # Convert to our format
        repo_entries = []
        for repo in repos:
            # Validate repo structure
            if not isinstance(repo, dict):
                print(f"    ⚠️ Skipping non-dict repo entry: {type(repo)}")
                continue
                
            if 'name' not in repo or 'html_url' not in repo:
                print(f"    ⚠️ Skipping repo missing required fields: {repo}")
                continue
            
            try:
                repo_entry = {
                    'Name': repo['name'],
                    'Chain': 'bnb-chain',
                    'Github Link': repo['html_url'],
                    'Link Status': 'REPO',
                    'Original Source': project_name or username,
                    'Language': repo.get('language', ''),
                    'Stars': repo.get('stargazers_count', 0),
                    'Forks': repo.get('forks_count', 0),
                    'Description': (repo.get('description') or '')[:100] + '...' if repo.get('description') and len(repo.get('description', '')) > 100 else (repo.get('description') or '')
                }
                repo_entries.append(repo_entry)
            except Exception as e:
                print(f"    ⚠️ Error processing repo {repo.get('name', 'unknown')}: {e}")
                continue
        
        print(f"  ✓ Found {len(repo_entries)} repositories")
        return repo_entries
    
    def append_to_csv(self, repo_entries: List[Dict]):
        """Append repository entries to the CSV file."""
        if not repo_entries:
            return
        
        with open(self.output_csv, 'a', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=repo_entries[0].keys())
            writer.writerows(repo_entries)
        
        print(f"  ✓ Added {len(repo_entries)} repositories to {self.output_csv}")
    
    def process_csv_links(self, input_csv: str):
        """Process all GitHub links from an input CSV file."""
        print(f"Processing CSV file: {input_csv}")
        
        if not Path(input_csv).exists():
            print(f"❌ Input CSV file not found: {input_csv}")
            return
        
        # Clear any existing progress and output files
        progress_file = "gatherer_progress.json"
        if Path(progress_file).exists():
            os.remove(progress_file)
            print("🗑️  Cleared previous progress - starting fresh!")
        
        # Clear output CSV to start fresh
        if Path(self.output_csv).exists():
            os.remove(self.output_csv)
            print(f"🗑️  Cleared previous output CSV - starting fresh!")
            self.init_output_csv()
        
        total_repos = 0
        processed_count = 0
        
        with open(input_csv, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            
            for row_num, row in enumerate(rows, 1):
                github_link = row.get('Github Link', '')
                project_name = row.get('Name', '')
                link_status = row.get('Link Status', '')
                
                if not github_link or github_link == '-':
                    continue
                
                print(f"\n[{row_num}] Processing: {project_name}")
                
                # Process the GitHub link
                repo_entries = self.process_github_link(github_link, project_name)
                
                if repo_entries:
                    # Append to output CSV
                    self.append_to_csv(repo_entries)
                    total_repos += len(repo_entries)
                
                processed_count += 1
                
                # Rate limiting
                if not self.github_token:
                    print("  Waiting 1 second before next request...")
                    time.sleep(1)
                
                # Check rate limit status
                if not self.github_token and processed_count % 50 == 0:
                    print(f"\n⚠ Processed {processed_count} entries. Rate limit approaching.")
                    print("   Consider setting GITHUB_TOKEN for higher limits.")
                    response = input("Continue? (y/n): ").lower().strip()
                    if response not in ['y', 'yes']:
                        print("Stopping. You can resume later.")
                        break
        
        print(f"\n{'='*60}")
        print("PROCESSING COMPLETED!")
        print(f"{'='*60}")
        print(f"Total repositories gathered: {total_repos}")
        print(f"Results saved to: {self.output_csv}")
    
    def load_progress(self, progress_file: str) -> Dict:
        """Load progress from file."""
        if Path(progress_file).exists():
            try:
                with open(progress_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading progress: {e}")
        return {}
    
    def save_progress(self, progress_file: str, progress: Dict):
        """Save progress to file."""
        try:
            with open(progress_file, 'w') as f:
                json.dump(progress, f, indent=2)
        except Exception as e:
            print(f"Error saving progress: {e}")
    
    def process_single_link(self, github_url: str, project_name: str = ""):
        """Process a single GitHub URL."""
        print(f"Processing single GitHub URL: {github_url}")
        
        repo_entries = self.process_github_link(github_url, project_name)
        
        if repo_entries:
            self.append_to_csv(repo_entries)
            print(f"\n✓ Successfully processed {len(repo_entries)} repositories")
        else:
            print("\n❌ No repositories found or error occurred")

def main():
    """Main function."""
    print("GitHub Repository Link Gatherer")
    print("=" * 40)
    
    gatherer = RepoGatherer()
    
    # Check if input CSV exists
    input_csv = "sheet_with_status.csv"
    
    if Path(input_csv).exists():
        print(f"Found input CSV: {input_csv}")
        response = input("Process all links from this CSV? (y/n): ").lower().strip()
        
        if response in ['y', 'yes']:
            gatherer.process_csv_links(input_csv)
        else:
            print("Processing single link mode.")
            github_url = input("Enter GitHub URL: ").strip()
            project_name = input("Enter project name (optional): ").strip()
            
            if github_url:
                gatherer.process_single_link(github_url, project_name)
            else:
                print("No URL provided.")
    else:
        print(f"Input CSV not found: {input_csv}")
        print("Single link mode.")
        github_url = input("Enter GitHub URL: ").strip()
        project_name = input("Enter project name (optional): ").strip()
        
        if github_url:
            gatherer.process_single_link(github_url, project_name)
        else:
            print("No URL provided.")

if __name__ == "__main__":
    main()
