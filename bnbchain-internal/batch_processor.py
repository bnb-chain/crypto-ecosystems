#!/usr/bin/env python3
"""
Batch Processor for BNB Chain Repository Analysis
This script processes large datasets in batches with progress tracking and resume functionality.
"""

import csv
import json
import os
import time
from pathlib import Path
from typing import List, Dict, Optional
from repo_analyzer import BNBChainRepoAnalyzer

class BatchProcessor:
    def __init__(self, csv_path: str, batch_size: int = 10, output_dir: str = "output"):
        self.csv_path = csv_path
        self.batch_size = batch_size
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Progress tracking
        self.progress_file = self.output_dir / "progress.json"
        self.results_file = self.output_dir / "all_results.csv"
        
        # Load existing progress
        self.progress = self.load_progress()
        
    def load_progress(self) -> Dict:
        """Load existing progress from file."""
        if self.progress_file.exists():
            try:
                with open(self.progress_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading progress: {e}")
        
        return {
            'processed_users': [],
            'total_users': 0,
            'current_batch': 0,
            'total_repos_found': 0,
            'start_time': time.time()
        }
    
    def save_progress(self):
        """Save current progress to file."""
        try:
            with open(self.progress_file, 'w') as f:
                json.dump(self.progress, f, indent=2)
        except Exception as e:
            print(f"Error saving progress: {e}")
    
    def get_users_to_process(self) -> List[Dict]:
        """Get list of users that need to be processed."""
        users = []
        
        with open(self.csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                link_status = row.get('Link Status', '')
                github_link = row.get('Github Link', '')
                
                if link_status in ['USER', 'ORG'] and github_link:
                    username = self.extract_github_username(github_link)
                    if username and username not in self.progress['processed_users']:
                        users.append({
                            'username': username,
                            'project_name': row.get('Name', ''),
                            'link_status': link_status,
                            'github_link': github_link
                        })
        
        self.progress['total_users'] = len(users) + len(self.progress['processed_users'])
        return users
    
    def extract_github_username(self, github_url: str) -> Optional[str]:
        """Extract GitHub username from URL."""
        import re
        
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
    
    def process_batch(self, users: List[Dict], analyzer: BNBChainRepoAnalyzer) -> List[Dict]:
        """Process a batch of users."""
        batch_results = []
        
        for i, user in enumerate(users):
            print(f"\nProcessing batch {self.progress['current_batch'] + 1}, user {i + 1}/{len(users)}: {user['username']}")
            
            try:
                # Get repositories for this user
                repos = analyzer.get_user_repos(user['username'])
                print(f"  Found {len(repos)} repositories")
                
                # Analyze repositories
                user_repos = []
                for repo in repos:
                    is_related, confidence = analyzer.analyze_repo_content(repo)
                    
                    if is_related:
                        repo_entry = {
                            'Name': repo['name'],
                            'Chain': 'bnb-chain',
                            'Github Link': repo['html_url'],
                            'Link Status': 'REPO',
                            'Original Project': user['project_name'],
                            'Confidence Score': f"{confidence:.1f}",
                            'Language': repo.get('language', ''),
                            'Stars': repo.get('stargazers_count', 0),
                            'Forks': repo.get('forks_count', 0),
                            'Size': repo.get('size', 0),
                            'Description': (repo.get('description') or '')[:100] + '...' if repo.get('description') and len(repo.get('description', '')) > 100 else (repo.get('description') or '')
                        }
                        
                        user_repos.append(repo_entry)
                        print(f"    ✓ {repo['name']} (Score: {confidence:.1f})")
                
                batch_results.extend(user_repos)
                self.progress['total_repos_found'] += len(user_repos)
                
                # Mark user as processed
                self.progress['processed_users'].append(user['username'])
                self.save_progress()
                
                # Be nice to GitHub API
                time.sleep(1)
                
            except Exception as e:
                print(f"  Error processing {user['username']}: {e}")
                continue
        
        return batch_results
    
    def save_batch_results(self, batch_results: List[Dict], batch_num: int):
        """Save batch results to a separate file."""
        if not batch_results:
            return
            
        batch_file = self.output_dir / f"batch_{batch_num:03d}.csv"
        
        with open(batch_file, 'w', encoding='utf-8', newline='') as file:
            if batch_results:
                fieldnames = batch_results[0].keys()
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(batch_results)
        
        print(f"Batch {batch_num} results saved to: {batch_file}")
    
    def merge_all_results(self):
        """Merge all batch results into a single file."""
        all_results = []
        
        # Read original CSV
        with open(self.csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            all_results = list(reader)
        
        # Read all batch files
        batch_files = sorted(self.output_dir.glob("batch_*.csv"))
        
        for batch_file in batch_files:
            try:
                with open(batch_file, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    batch_results = list(reader)
                    all_results.extend(batch_results)
                    print(f"Added {len(batch_results)} results from {batch_file.name}")
            except Exception as e:
                print(f"Error reading {batch_file}: {e}")
        
        # Save merged results
        with open(self.results_file, 'w', encoding='utf-8', newline='') as file:
            if all_results:
                fieldnames = all_results[0].keys()
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(all_results)
        
        print(f"\nAll results merged into: {self.results_file}")
        print(f"Total entries: {len(all_results)}")
    
    def run(self):
        """Run the batch processor."""
        print("BNB Chain Repository Analyzer - Batch Processor")
        print("=" * 50)
        
        # Check if GitHub token is available
        github_token = os.getenv('GITHUB_TOKEN')
        if not github_token:
            print("Warning: GITHUB_TOKEN environment variable not set.")
            print("You may hit rate limits. Set GITHUB_TOKEN for better performance.")
            print()
        
        # Initialize analyzer
        analyzer = BNBChainRepoAnalyzer(self.csv_path, github_token)
        
        # Get users to process
        users = self.get_users_to_process()
        
        if not users:
            print("No new users to process. All users have been processed.")
            if self.progress['processed_users']:
                print("Merging existing results...")
                self.merge_all_results()
            return
        
        print(f"Found {len(users)} users to process")
        print(f"Already processed: {len(self.progress['processed_users'])} users")
        print(f"Total users: {self.progress['total_users']}")
        print()
        
        # Process in batches
        for i in range(0, len(users), self.batch_size):
            batch_users = users[i:i + self.batch_size]
            batch_num = self.progress['current_batch']
            
            print(f"\n{'='*60}")
            print(f"Processing Batch {batch_num + 1}")
            print(f"Users {i + 1}-{min(i + self.batch_size, len(users))} of {len(users)}")
            print(f"{'='*60}")
            
            # Process batch
            batch_results = self.process_batch(batch_users, analyzer)
            
            # Save batch results
            self.save_batch_results(batch_results, batch_num)
            
            # Update progress
            self.progress['current_batch'] += 1
            self.save_progress()
            
            # Progress summary
            processed = len(self.progress['processed_users'])
            total = self.progress['total_users']
            repos_found = self.progress['total_repos_found']
            
            print(f"\nBatch {batch_num + 1} completed!")
            print(f"Progress: {processed}/{total} users processed ({processed/total*100:.1f}%)")
            print(f"Total repositories found: {repos_found}")
            
            # Ask if user wants to continue
            if i + self.batch_size < len(users):
                try:
                    response = input("\nContinue to next batch? (y/n): ").lower().strip()
                    if response not in ['y', 'yes']:
                        print("Stopping batch processing. You can resume later.")
                        break
                except KeyboardInterrupt:
                    print("\nStopping batch processing. You can resume later.")
                    break
        
        # Merge all results
        print("\nMerging all results...")
        self.merge_all_results()
        
        # Final summary
        elapsed_time = time.time() - self.progress['start_time']
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        print(f"\n{'='*60}")
        print("BATCH PROCESSING COMPLETED!")
        print(f"{'='*60}")
        print(f"Total users processed: {len(self.progress['processed_users'])}")
        print(f"Total repositories found: {self.progress['total_repos_found']}")
        print(f"Total time: {int(hours)}h {int(minutes)}m {int(seconds)}s")
        print(f"Results saved to: {self.results_file}")

def main():
    """Main function to run the batch processor."""
    csv_path = "sheet_with_status.csv"
    
    # Configuration
    batch_size = 5  # Process 5 users at a time
    output_dir = "batch_output"
    
    # Initialize and run processor
    processor = BatchProcessor(csv_path, batch_size, output_dir)
    processor.run()

if __name__ == "__main__":
    main()
