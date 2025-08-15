#!/usr/bin/env python3
"""
GitHub Link Checker Script
Checks GitHub links in a CSV file and categorizes them by type.
"""

import csv
import requests
import time
from urllib.parse import urlparse
import sys
from typing import Dict, List, Tuple

class GitHubLinkChecker:
    def __init__(self, csv_file_path: str):
        self.csv_file_path = csv_file_path
        self.session = requests.Session()
        # Set a realistic user agent to avoid being blocked
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.results = []
        
    def check_github_link(self, url: str) -> str:
        """
        Check a GitHub link and return its status.
        
        Args:
            url: The GitHub URL to check
            
        Returns:
            Status string: "ORG", "USER", "REPO", "INVALID", or "NO_LINK"
        """
        if not url or url.strip() == "-":
            return "NO_LINK"
            
        # Clean the URL
        url = url.strip()
        if not url.startswith("https://github.com/"):
            return "INVALID"
            
        try:
            # Add delay to be respectful to GitHub's servers
            time.sleep(1)
            
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 404:
                return "INVALID"
            elif response.status_code == 403:
                # Private repository or organization
                return "INVALID"
            elif response.status_code == 200:
                # Parse the URL to determine the type
                parsed_url = urlparse(url)
                path_parts = parsed_url.path.strip('/').split('/')
                
                if len(path_parts) == 1:
                    # Single path component - could be user or org
                    return "USER" if self._is_user_page(response.text) else "ORG"
                elif len(path_parts) == 2:
                    # Two path components - repository
                    return "REPO"
                else:
                    # More than 2 components - likely a specific file or directory
                    return "REPO"
            else:
                return "INVALID"
                
        except requests.exceptions.RequestException as e:
            print(f"Error checking {url}: {e}")
            return "INVALID"
        except Exception as e:
            print(f"Unexpected error checking {url}: {e}")
            return "INVALID"
    
    def _is_user_page(self, html_content: str) -> bool:
        """
        Determine if a page is a user page by checking for user-specific elements.
        This is a simple heuristic - GitHub user pages typically have different content than org pages.
        """
        # Look for indicators that suggest it's a user page
        user_indicators = [
            'class="avatar avatar-user"',
            'class="avatar avatar-8"',
            'data-testid="user-profile"',
            'class="user-profile-nav"'
        ]
        
        org_indicators = [
            'class="avatar avatar-8"',
            'data-testid="organization-profile"',
            'class="org-profile-nav"'
        ]
        
        # Count indicators
        user_count = sum(1 for indicator in user_indicators if indicator in html_content)
        org_count = sum(1 for indicator in org_indicators if indicator in html_content)
        
        # If we have more user indicators, it's likely a user page
        if user_count > org_count:
            return True
        elif org_count > user_count:
            return False
        else:
            # Default to USER if we can't determine
            return True
    
    def process_csv(self) -> None:
        """Process the CSV file and add link status information."""
        try:
            with open(self.csv_file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                rows = list(reader)
                
            print(f"Processing {len(rows)} rows...")
            
            for i, row in enumerate(rows):
                github_link = row.get('Github Link', '')
                print(f"Processing row {i+1}/{len(rows)}: {row.get('Name', 'Unknown')}")
                
                status = self.check_github_link(github_link)
                row['Link Status'] = status
                
                print(f"  {github_link} -> {status}")
                
                # Add a small delay between requests to be respectful
                if i < len(rows) - 1:  # Don't delay after the last request
                    time.sleep(0.5)
            
            # Save the updated CSV
            output_file = self.csv_file_path.replace('.csv', '_with_status.csv')
            with open(output_file, 'w', encoding='utf-8', newline='') as file:
                fieldnames = list(rows[0].keys())
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            
            print(f"\nProcessing complete! Results saved to: {output_file}")
            
            # Print summary
            status_counts = {}
            for row in rows:
                status = row['Link Status']
                status_counts[status] = status_counts.get(status, 0) + 1
            
            print("\nSummary:")
            for status, count in status_counts.items():
                print(f"  {status}: {count}")
                
        except FileNotFoundError:
            print(f"Error: File '{self.csv_file_path}' not found.")
        except Exception as e:
            print(f"Error processing CSV: {e}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python github_link_checker.py <csv_file_path>")
        print("Example: python github_link_checker.py 'bnbchain-internal/Sheet1.csv'")
        sys.exit(1)
    
    csv_file_path = sys.argv[1]
    
    print("GitHub Link Checker")
    print("==================")
    print(f"Processing file: {csv_file_path}")
    print()
    
    checker = GitHubLinkChecker(csv_file_path)
    checker.process_csv()

if __name__ == "__main__":
    main()
