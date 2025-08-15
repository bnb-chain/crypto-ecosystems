# BNB Chain Repository Analyzer

This script analyzes GitHub repositories from projects with "USER" or "ORG" Link Status in your CSV file and adds relevant BNB Chain repositories to the CSV.

## Features

- **Smart Repository Filtering**: Uses multiple criteria to determine if a repository is BNB Chain related
- **Content Analysis**: Analyzes README files and repository metadata for relevance
- **Confidence Scoring**: Provides confidence scores for each repository match
- **Rate Limiting**: Respects GitHub API rate limits and includes automatic retry logic
- **Comprehensive Output**: Adds detailed information including language, stars, forks, and description

## Prerequisites

1. **Python 3.7+** installed on your system
2. **GitHub Personal Access Token** (recommended for better rate limits)

## Installation

1. Install the required dependencies:
   ```bash
   pip install -r requirements_repo_analyzer.txt
   ```

2. Set your GitHub token (optional but recommended):
   ```bash
   # On Windows (PowerShell)
   $env:GITHUB_TOKEN="your_github_token_here"
   
   # On Linux/Mac
   export GITHUB_TOKEN="your_github_token_here"
   ```

## Usage

1. Make sure your `sheet_with_status.csv` file is in the same directory as the script
2. Run the script:
   ```bash
   python repo_analyzer.py
   ```

## How It Works

### 1. Repository Discovery
- Scans your CSV for projects with "USER" or "ORG" Link Status
- Extracts GitHub usernames from the GitHub links
- Fetches all repositories for each user/organization

### 2. Relevance Analysis
The script uses a scoring system based on multiple factors:

- **Repository Name & Description**: Matches against BNB Chain keywords
- **Programming Language**: Solidity gets high scores, other web3 languages get moderate scores
- **Repository Activity**: Stars, forks, and size contribute to relevance
- **README Content**: Analyzes README files for BNB Chain indicators
- **Repository Status**: Penalizes archived or forked repositories

### 3. Output
Creates a new CSV file (`sheet_with_status_with_repos.csv`) containing:
- Original project data
- New repository entries with:
  - Repository name
  - Chain (set to "bnb-chain")
  - GitHub link
  - Link Status (set to "REPO")
  - Original project reference
  - Confidence score
  - Language, stars, forks, size
  - Description

## Configuration

You can adjust the relevance threshold by modifying the `is_related = score >= 30` line in the `analyze_repo_content` method. Higher thresholds mean stricter filtering.

## BNB Chain Keywords

The script looks for these terms in repository names, descriptions, and READMEs:
- Blockchain: `bnb`, `binance`, `bsc`, `smart chain`, `beacon chain`
- DeFi: `defi`, `dex`, `swap`, `yield`, `liquidity`, `staking`
- Web3: `web3`, `blockchain`, `cryptocurrency`, `nft`, `gamefi`
- AI: `ai`, `artificial intelligence`, `machine learning`
- Development: `solidity`, `contract`, `token`

## Rate Limiting

Without a GitHub token, you're limited to 60 requests per hour. With a token, you get 5,000 requests per hour. The script automatically handles rate limiting and waits when necessary.

## Output Example

```csv
Name,Chain,Github Link,Link Status,Original Project,Confidence Score,Language,Stars,Forks,Size,Description
fstswap-core,bnb-chain,https://github.com/fstswap/fstswap-core,REPO,FstSwap,85.0,Solidity,45,12,2048,Core smart contracts for FstSwap DEX...
fstswap-interface,bnb-chain,https://github.com/fstswap/fstswap-interface,REPO,FstSwap,72.0,TypeScript,23,8,1536,Frontend interface for FstSwap...
```

## Troubleshooting

- **Rate Limit Errors**: Set a GitHub token or wait for the rate limit to reset
- **Permission Errors**: Ensure the script has read/write access to the CSV file
- **Network Errors**: Check your internet connection and GitHub API availability

## Notes

- The script processes repositories in batches to be respectful to GitHub's API
- Large organizations with many repositories may take longer to process
- Confidence scores are normalized from 0-100, with 30+ considered relevant
- The script automatically handles pagination for users with many repositories
