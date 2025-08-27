# CSV Status Analyzer

This script analyzes `sheet.csv` and determines the `Link Status` for each GitHub link, then creates `sheet_with_status.csv` format.

## What It Does

The script examines each GitHub link in your CSV and categorizes it as:

- **REPO**: Valid GitHub repository (e.g., `github.com/username/repo`)
- **USER**: Valid GitHub user (e.g., `github.com/username`)
- **ORG**: Valid GitHub organization (e.g., `github.com/orgname`)
- **INVALID**: Everything else (invalid URLs, non-GitHub links, empty, etc.)

## Input vs Output

### Input (`sheet.csv`):
```csv
Name,Chain,Github Link
FstSwap,bnb-chain,https://github.com/fstswap/fstswap.github.io
Ultiverse,bnb-chain,https://github.com/ultiverse-io/
LiveArt,bnb-chain,https://github.com/LiveArtx
```

### Output (`sheet_with_status.csv`):
```csv
Name,Chain,Github Link,Link Status
FstSwap,bnb-chain,https://github.com/fstswap/fstswap.github.io,REPO
Ultiverse,bnb-chain,https://github.com/ultiverse-io/,USER
LiveArt,bnb-chain,https://github.com/LiveArtx,USER
```

## Usage

### 1. **Install Dependencies**
```bash
pip install -r requirements_repo_gatherer.txt
```

### 2. **Set GitHub Token** (Recommended)
```bash
# Add to .env file
GITHUB_TOKEN=your_github_token_here
```

### 3. **Run the Script**
```bash
python csv_status_analyzer.py
```

## Features

- **Smart URL Analysis**: Automatically detects repository vs user links
- **GitHub API Validation**: Checks if users and repositories actually exist
- **Rate Limit Handling**: Respects GitHub API limits
- **Progress Tracking**: Shows progress and status updates
- **Detailed Summary**: Provides counts and recommendations
- **Error Handling**: Gracefully handles API errors and rate limits

## Rate Limiting

- **Without GitHub token**: 60 requests/hour (1 second delay)
- **With GitHub token**: 5,000 requests/hour (no delay)

## Output Summary

The script provides a detailed summary including:
- Total entries processed
- Count of each status type
- Recommendations for next steps
- Files that can be processed by `repo_gatherer.py`

## Next Steps

After running this script, you can:

1. **Review the status summary** to understand your data quality
2. **Use `repo_gatherer.py`** to process all `USER` entries
3. **Manually review** `INVALID_URL` and `NOT_GITHUB` entries
4. **Clean up** malformed URLs in your source data

## Example Output

```
Status Summary:
  REPO: 45
  USER: 23
  ORG: 12
  INVALID: 3

Recommendations:
  - 23 entries are GitHub users (can be processed by repo_gatherer.py)
  - 12 entries are GitHub organizations (can be processed by repo_gatherer.py)
  - 45 entries are valid GitHub repositories
  - 3 entries have invalid or non-GitHub links
```

This gives you a complete understanding of your GitHub links and prepares them for further processing!
