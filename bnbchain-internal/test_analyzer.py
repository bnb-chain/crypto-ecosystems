#!/usr/bin/env python3
"""
Test script for the BNB Chain Repository Analyzer
This script demonstrates the analyzer functionality with sample data.
"""

import csv
import tempfile
import os
from repo_analyzer import BNBChainRepoAnalyzer

def create_test_csv():
    """Create a test CSV file with sample data."""
    test_data = [
        {
            'Name': 'Test Project 1',
            'Chain': 'bnb-chain',
            'Github Link': 'https://github.com/fstswap',
            'Link Status': 'USER'
        },
        {
            'Name': 'Test Project 2',
            'Chain': 'bnb-chain',
            'Github Link': 'https://github.com/ultiverse-io',
            'Link Status': 'ORG'
        },
        {
            'Name': 'Test Project 3',
            'Chain': 'bnb-chain',
            'Github Link': 'https://github.com/someuser/somerepo',
            'Link Status': 'REPO'
        }
    ]
    
    # Create temporary CSV file
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='', encoding='utf-8')
    
    with temp_file:
        writer = csv.DictWriter(temp_file, fieldnames=test_data[0].keys())
        writer.writeheader()
        writer.writerows(test_data)
    
    return temp_file.name

def test_username_extraction():
    """Test the GitHub username extraction functionality."""
    analyzer = BNBChainRepoAnalyzer("dummy.csv")
    
    test_cases = [
        ("https://github.com/fstswap", "fstswap"),
        ("https://github.com/ultiverse-io/", "ultiverse-io"),
        ("https://github.com/someuser/somerepo", "someuser"),
        ("https://github.com/orgname?tab=repositories", "orgname"),
        ("https://github.com", None),
        ("-", None),
        ("", None)
    ]
    
    print("Testing GitHub username extraction:")
    print("=" * 40)
    
    for url, expected in test_cases:
        result = analyzer.extract_github_username(url)
        status = "✓" if result == expected else "✗"
        print(f"{status} {url} -> {result} (expected: {expected})")
    
    print()

def test_scoring_system():
    """Test the repository scoring system."""
    analyzer = BNBChainRepoAnalyzer("dummy.csv")
    
    # Mock repository data
    test_repos = [
        {
            'name': 'bnb-swap-contracts',
            'description': 'Smart contracts for BNB Chain DEX',
            'language': 'Solidity',
            'fork': False,
            'size': 2000,
            'stargazers_count': 50,
            'forks_count': 20,
            'archived': False,
            'full_name': 'testuser/bnb-swap-contracts'
        },
        {
            'name': 'random-project',
            'description': 'A generic web application',
            'language': 'JavaScript',
            'fork': True,
            'size': 500,
            'stargazers_count': 2,
            'forks_count': 1,
            'archived': False,
            'full_name': 'testuser/random-project'
        },
        {
            'name': 'defi-yield-farming',
            'description': 'Yield farming protocol on BSC',
            'language': 'Solidity',
            'fork': False,
            'size': 1500,
            'stargazers_count': 100,
            'forks_count': 30,
            'archived': False,
            'full_name': 'testuser/defi-yield-farming'
        }
    ]
    
    print("Testing repository scoring system:")
    print("=" * 40)
    
    for repo in test_repos:
        is_related, score = analyzer.analyze_repo_content(repo)
        status = "✓" if is_related else "✗"
        print(f"{status} {repo['name']}: Score {score:.1f} (Related: {is_related})")
    
    print()

def main():
    """Run all tests."""
    print("BNB Chain Repository Analyzer - Test Suite")
    print("=" * 50)
    print()
    
    # Test username extraction
    test_username_extraction()
    
    # Test scoring system
    test_scoring_system()
    
    print("Test suite completed!")
    print("\nTo run the full analyzer on your CSV file:")
    print("1. Make sure your sheet_with_status.csv is in the same directory")
    print("2. Run: python repo_analyzer.py")
    print("3. Optionally set GITHUB_TOKEN environment variable for better rate limits")

if __name__ == "__main__":
    main()
