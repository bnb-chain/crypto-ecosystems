#!/usr/bin/env python3
"""
Repository Analyzer for BNB Chain Projects
This script analyzes GitHub repositories from projects with USER/ORG Link Status
and adds relevant BNB Chain repositories to the CSV.
"""

import csv
import os
import re
import time
import requests
from urllib.parse import urlparse
from typing import List, Dict, Optional, Tuple
import json
from pathlib import Path

class BNBChainRepoAnalyzer:
    def __init__(self, csv_path: str, github_token: Optional[str] = None):
        self.csv_path = csv_path
        self.github_token = github_token or os.getenv('GITHUB_TOKEN')
        self.session = requests.Session()
        if self.github_token:
            self.session.headers.update({
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            })
        
        # Import configuration
        try:
            from config import BNB_KEYWORDS, README_INDICATORS, SCORING_CONFIG, GITHUB_CONFIG, OUTPUT_CONFIG, LOGGING_CONFIG
            self.bnb_keywords = BNB_KEYWORDS
            self.bnb_readme_indicators = README_INDICATORS
            self.scoring_config = SCORING_CONFIG
            self.github_config = GITHUB_CONFIG
            self.output_config = OUTPUT_CONFIG
            self.logging_config = LOGGING_CONFIG
        except ImportError:
            # Fallback to default values if config file not found
            self.bnb_keywords = [
                'bnb', 'binance', 'bsc', 'smart chain', 'beacon chain', 'defi', 'dex', 'swap',
                'yield', 'liquidity', 'staking', 'governance', 'dao', 'nft', 'gamefi', 'metaverse',
                'ai', 'artificial intelligence', 'machine learning', 'token', 'contract', 'solidity',
                'web3', 'blockchain', 'cryptocurrency', 'trading', 'finance', 'lending', 'borrowing'
            ]
            self.bnb_readme_indicators = [
                'bnb chain', 'binance smart chain', 'bsc', 'beacon chain', 'opbnb', 'zksync',
                'polygon zkevm', 'arbitrum', 'ethereum', 'defi', 'dex', 'swap', 'yield farming',
                'liquidity mining', 'staking', 'governance', 'dao', 'nft', 'gamefi', 'metaverse'
            ]
            self.scoring_config = {
                'MINIMUM_RELEVANCE_SCORE': 30,
                'MAX_SCORE': 100,
                'SCORES': {
                    'KEYWORD_IN_NAME': 15,
                    'KEYWORD_IN_DESCRIPTION': 10,
                    'SOLIDITY_LANGUAGE': 25,
                    'WEB3_LANGUAGE': 10,
                    'LARGE_SIZE': 5,
                    'MANY_STARS': 5,
                    'MANY_FORKS': 5,
                    'README_INDICATOR': 8,
                    'FORK_PENALTY': -10,
                    'ARCHIVED_PENALTY': -20,
                },
                'THRESHOLDS': {
                    'LARGE_SIZE_KB': 1000,
                    'MANY_STARS_COUNT': 10,
                    'MANY_FORKS_COUNT': 5,
                }
            }
            self.github_config = {
                'REPOS_PER_PAGE': 100,
                'REQUEST_DELAY': 0.1,
                'RATE_LIMIT_BUFFER': 60,
                'MAX_PAGES': 100,
            }
            self.output_config = {
                'DEFAULT_OUTPUT_SUFFIX': '_with_repos',
                'MAX_DESCRIPTION_LENGTH': 100,
                'INCLUDE_ADDITIONAL_FIELDS': True,
            }
            self.logging_config = {
                'VERBOSE': True,
                'SHOW_PROGRESS': True,
                'SHOW_SCORES': True,
                'SHOW_REJECTED': True,
            }

    def extract_github_username(self, github_url: str) -> Optional[str]:
        """Extract GitHub username from various GitHub URL formats."""
        if not github_url or github_url == '-':
            return None
            
        # Handle different GitHub URL formats
        patterns = [
            r'github\.com/([^/\s]+)/?$',  # github.com/username
            r'github\.com/([^/\s]+)/[^/\s]+',  # github.com/username/repo
            r'github\.com/([^/\s]+)\?',  # github.com/username?param
        ]
        
        for pattern in patterns:
            match = re.search(pattern, github_url)
            if match:
                return match.group(1)
        
        return None

    def get_user_repos(self, username: str) -> List[Dict]:
        """Fetch repositories for a GitHub user/organization."""
        repos = []
        page = 1
        
        while True:
            url = f"{self.github_config.get('BASE_URL', 'https://api.github.com')}/users/{username}/repos"
            params = {
                'page': page,
                'per_page': self.github_config['REPOS_PER_PAGE'],
                'sort': 'updated',
                'direction': 'desc'
            }
            
            try:
                response = self.session.get(url, params=params)
                response.raise_for_status()
                
                page_repos = response.json()
                if not page_repos:
                    break
                    
                repos.extend(page_repos)
                page += 1
                
                # Rate limiting
                if 'X-RateLimit-Remaining' in response.headers:
                    remaining = int(response.headers['X-RateLimit-Remaining'])
                    if remaining <= 1:
                        reset_time = int(response.headers['X-RateLimit-Reset'])
                        wait_time = reset_time - int(time.time()) + self.github_config['RATE_LIMIT_BUFFER']
                        if wait_time > 0:
                            print(f"Rate limited. Waiting {wait_time} seconds...")
                            time.sleep(wait_time)
                
                time.sleep(self.github_config['REQUEST_DELAY'])  # Be nice to GitHub API
                
                # Check page limit
                if page >= self.github_config['MAX_PAGES']:
                    print(f"Reached maximum page limit ({self.github_config['MAX_PAGES']}) for {username}")
                    break
                
            except requests.exceptions.RequestException as e:
                print(f"Error fetching repos for {username}: {e}")
                break
            except Exception as e:
                print(f"Unexpected error for {username}: {e}")
                break
        
        return repos

    def analyze_repo_content(self, repo: Dict) -> Tuple[bool, float]:
        """
        Analyze repository content to determine if it's BNB Chain related.
        Returns (is_related, confidence_score)
        """
        score = 0.0
        max_score = self.scoring_config['MAX_SCORE']
        
        # Check repository name
        repo_name = repo.get('name', '') or ''
        repo_name = repo_name.lower()
        
        # Check repository description (handle None values)
        repo_description = repo.get('description', '') or ''
        repo_description = repo_description.lower()
        
        # Score based on name and description
        for keyword in self.bnb_keywords:
            if keyword in repo_name:
                score += self.scoring_config['SCORES']['KEYWORD_IN_NAME']
            if keyword in repo_description:
                score += self.scoring_config['SCORES']['KEYWORD_IN_DESCRIPTION']
        
        # Check if it's a fork (usually less relevant)
        if repo.get('fork', False):
            score += self.scoring_config['SCORES']['FORK_PENALTY']
        
        # Check repository size and activity
        if repo.get('size', 0) > self.scoring_config['THRESHOLDS']['LARGE_SIZE_KB']:
            score += self.scoring_config['SCORES']['LARGE_SIZE']
        
        if repo.get('stargazers_count', 0) > self.scoring_config['THRESHOLDS']['MANY_STARS_COUNT']:
            score += self.scoring_config['SCORES']['MANY_STARS']
        
        if repo.get('forks_count', 0) > self.scoring_config['THRESHOLDS']['MANY_FORKS_COUNT']:
            score += self.scoring_config['SCORES']['MANY_FORKS']
        
        # Check if it's archived
        if repo.get('archived', False):
            score += self.scoring_config['SCORES']['ARCHIVED_PENALTY']
        
        # Check language (Solidity is a strong indicator)
        language = repo.get('language', '') or ''
        language = language.lower()
        if language == 'solidity':
            score += self.scoring_config['SCORES']['SOLIDITY_LANGUAGE']
        elif language in ['javascript', 'typescript', 'python', 'go', 'rust']:
            score += self.scoring_config['SCORES']['WEB3_LANGUAGE']
        
        # Try to analyze README content if available
        readme_score = self.analyze_readme(repo)
        score += readme_score
        
        # Normalize score
        score = max(0, min(score, max_score))
        
        # Determine if related (threshold can be adjusted)
        is_related = score >= self.scoring_config['MINIMUM_RELEVANCE_SCORE']
        
        return is_related, score

    def analyze_readme(self, repo: Dict) -> float:
        """Analyze README content for BNB Chain indicators."""
        try:
            # Try to get README content
            readme_url = f"https://api.github.com/repos/{repo['full_name']}/readme"
            response = self.session.get(readme_url)
            
            if response.status_code == 200:
                readme_data = response.json()
                content = readme_data.get('content', '')
                
                if content:
                    # Decode base64 content
                    import base64
                    decoded_content = base64.b64decode(content).decode('utf-8', errors='ignore').lower()
                    
                    score = 0.0
                    for indicator in self.bnb_readme_indicators:
                        if indicator in decoded_content:
                            score += self.scoring_config['SCORES']['README_INDICATOR']
                    
                    return min(score, 40)  # Cap README score at 40
            
        except Exception as e:
            print(f"Error analyzing README for {repo['full_name']}: {e}")
        
        return 0.0

    def process_csv(self) -> List[Dict]:
        """Process the CSV and return new repository entries."""
        new_repos = []
        
        # Create output file for continuous appending
        output_path = self.csv_path.replace('.csv', self.output_config['DEFAULT_OUTPUT_SUFFIX'] + '.csv')
        output_exists = os.path.exists(output_path)
        
        # Prepare CSV writer for continuous appending
        if not output_exists:
            # Create new file with headers
            with open(output_path, 'w', encoding='utf-8', newline='') as file:
                fieldnames = ['Name', 'Chain', 'Github Link', 'Link Status', 'Original Project', 
                             'Confidence Score', 'Language', 'Stars', 'Forks', 'Size', 'Description']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
        
        print(f"Results will be continuously saved to: {output_path}")
        
        with open(self.csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                link_status = row.get('Link Status', '')
                github_link = row.get('Github Link', '')
                
                if link_status in ['USER', 'ORG'] and github_link:
                    username = self.extract_github_username(github_link)
                    if username:
                        print(f"\nProcessing {username} (Link Status: {link_status})...")
                        
                        repos = self.get_user_repos(username)
                        print(f"Found {len(repos)} repositories")
                        
                        # Add progress counter
                        processed_count = 0
                        relevant_count = 0
                        
                        for repo in repos:
                            # Validate repository data structure
                            if not isinstance(repo, dict):
                                print(f"    ⚠️ Skipping invalid repo data: {type(repo)}")
                                continue
                            
                            if 'name' not in repo:
                                print(f"    ⚠️ Skipping repo without name: {repo}")
                                continue
                            
                            is_related, confidence = self.analyze_repo_content(repo)
                            
                            if is_related:
                                repo_entry = {
                                    'Name': repo['name'],
                                    'Chain': 'bnb-chain',
                                    'Github Link': repo['html_url'],
                                    'Link Status': 'REPO',
                                    'Original Project': row.get('Name', ''),
                                    'Confidence Score': f"{confidence:.1f}",
                                    'Language': repo.get('language', ''),
                                    'Stars': repo.get('stargazers_count', 0),
                                    'Size': repo.get('size', 0),
                                    'Forks': repo.get('forks_count', 0),
                                    'Description': (repo.get('description') or '')[:self.output_config['MAX_DESCRIPTION_LENGTH']] + '...' if repo.get('description') and len(repo.get('description', '')) > self.output_config['MAX_DESCRIPTION_LENGTH'] else (repo.get('description') or '')
                                }
                                
                                # Append to memory list
                                new_repos.append(repo_entry)
                                
                                # Immediately append to CSV file
                                with open(output_path, 'a', encoding='utf-8', newline='') as file:
                                    writer = csv.DictWriter(file, fieldnames=repo_entry.keys())
                                    writer.writerow(repo_entry)
                                
                                if self.logging_config['SHOW_SCORES']:
                                    print(f"  ✓ {repo['name']} (Score: {confidence:.1f}) - SAVED")
                                else:
                                    print(f"  ✓ {repo['name']} - SAVED")
                                relevant_count += 1
                            elif self.logging_config['SHOW_REJECTED']:
                                if self.logging_config['SHOW_SCORES']:
                                    print(f"  ✗ {repo['name']} (Score: {confidence:.1f})")
                                else:
                                    print(f"  ✗ {repo['name']}")
                            
                            processed_count += 1
                            
                            # Show progress every 100 repositories
                            if processed_count % 100 == 0:
                                print(f"    Progress: {processed_count}/{len(repos)} repos processed, {relevant_count} relevant found")
                        
                        # Show user summary
                        print(f"    Completed {username}: {relevant_count}/{processed_count} repositories relevant")
                        
                        # Be nice to GitHub API
                        time.sleep(1)
        
        return new_repos

    def save_results(self, new_repos: List[Dict], output_path: str = None):
        """Save the new repository entries to a CSV file."""
        if not output_path:
            output_path = self.csv_path.replace('.csv', self.output_config['DEFAULT_OUTPUT_SUFFIX'] + '.csv')
        
        # Read existing CSV
        existing_rows = []
        with open(self.csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            existing_rows = list(reader)
        
        # Combine existing and new data
        all_rows = existing_rows + new_repos
        
        # Write combined data
        with open(output_path, 'w', encoding='utf-8', newline='') as file:
            if all_rows:
                fieldnames = all_rows[0].keys()
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(all_rows)
        
        print(f"\nResults saved to: {output_path}")
        print(f"Added {len(new_repos)} new repository entries")

def main():
    """Main function to run the repository analyzer."""
    csv_path = "sheet_with_status.csv"
    
    # Check if GitHub token is available
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("Warning: GITHUB_TOKEN environment variable not set.")
        print("You may hit rate limits. Set GITHUB_TOKEN for better performance.")
        print("You can set it with: export GITHUB_TOKEN=your_token_here")
        print()
    
    # Initialize analyzer
    analyzer = BNBChainRepoAnalyzer(csv_path, github_token)
    
    print("Starting BNB Chain Repository Analysis...")
    print("=" * 50)
    
    # Process CSV and get new repositories
    new_repos = analyzer.process_csv()
    
    if new_repos:
        print(f"\nFound {len(new_repos)} relevant repositories!")
        
        # Show summary
        print("\nSummary of new repositories:")
        for repo in new_repos[:10]:  # Show first 10
            print(f"  - {repo['Name']} (Score: {repo['Confidence Score']})")
        
        if len(new_repos) > 10:
            print(f"  ... and {len(new_repos) - 10} more")
        
        # Save results
        analyzer.save_results(new_repos)
        
    else:
        print("\nNo new relevant repositories found.")

if __name__ == "__main__":
    main()
