# Repository Link Gatherer

A simple script to gather all repository links from GitHub users/organizations and append them to a CSV file.

## Features

- **Batch Processing**: Process multiple GitHub links from a CSV file
- **Single Link Processing**: Process individual GitHub URLs
- **Rate Limiting**: Respects GitHub API rate limits
- **Progress Tracking**: Shows progress and results
- **CSV Output**: Appends results to a CSV file

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements_repo_gatherer.txt
   ```

2. **Optional: Set GitHub token** (recommended for higher rate limits):
   ```bash
   export GITHUB_TOKEN=your_github_token_here
   ```

## Usage

### Process all links from existing CSV

```bash
python repo_gatherer.py
```

The script will:
1. Look for `sheet_with_status.csv` in the current directory
2. Ask if you want to process all links from the CSV
3. Extract usernames from GitHub URLs
4. Gather all repositories for each user/organization
5. Append results to `gathered_repos.csv`

### Process a single GitHub link

```bash
python repo_gatherer.py
```

When prompted, choose "n" to enter single link mode, then provide:
- GitHub URL (e.g., `https://github.com/username`)
- Project name (optional)

## Output Format

The script creates/updates `gathered_repos.csv` with the following columns:

- **Name**: Repository name
- **Chain**: Set to "bnb-chain"
- **Github Link**: Full repository URL
- **Link Status**: Set to "REPO"
- **Original Source**: Project name or username
- **Language**: Primary programming language
- **Stars**: Number of stars
- **Forks**: Number of forks
- **Description**: Repository description (truncated to 100 chars)

## Rate Limiting

- **Without GitHub token**: 60 requests/hour (1 second delay between requests)
- **With GitHub token**: 5,000 requests/hour (no delay)

## Example

Input CSV with GitHub user links:
```csv
Name,Chain,Github Link,Link Status
Project A,bnb-chain,https://github.com/username1,USER
Project B,bnb-chain,https://github.com/username2,ORG
```

Output CSV with gathered repositories:
```csv
Name,Chain,Github Link,Link Status,Original Source,Language,Stars,Forks,Description
repo1,bnb-chain,https://github.com/username1/repo1,REPO,Project A,Python,10,5,Description...
repo2,bnb-chain,https://github.com/username1/repo2,REPO,Project A,JavaScript,25,12,Description...
repo3,bnb-chain,https://github.com/username2/repo3,REPO,Project B,Go,5,2,Description...
```

## Notes

- The script automatically handles pagination for users with many repositories
- Repositories are sorted by last updated (most recent first)
- Existing CSV files are appended to, not overwritten
- Error handling includes rate limits, 404s, and API errors
