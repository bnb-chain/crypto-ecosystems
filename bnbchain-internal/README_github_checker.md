# GitHub Link Checker

This Python script checks GitHub links in a CSV file and categorizes them by type.

## Features

- **Link Validation**: Checks if GitHub links are accessible (not 404 or private)
- **Link Categorization**: Identifies links as:
  - `ORG`: Organization page
  - `USER`: User profile page  
  - `REPO`: Repository page
  - `INVALID`: 404, private, or inaccessible links
  - `NO_LINK`: Entries with no GitHub link (marked as "-")

## Requirements

- Python 3.6+
- `requests` library

## Installation

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script with your CSV file as an argument:

```bash
python github_link_checker.py "bnbchain-internal/EC Submission Final GitHub - Sheet1.csv"
```

## Output

The script will:
1. Process each GitHub link in the CSV
2. Add a new "Link Status" column with the categorization
3. Save the results to a new file: `EC Submission Final GitHub - Sheet1_with_status.csv`
4. Display progress and a summary of results

## Example Output

```
GitHub Link Checker
==================
Processing file: bnbchain-internal/EC Submission Final GitHub - Sheet1.csv

Processing 419 rows...
Processing row 1/419: FstSwap
  https://github.com/fstswap/fstswap.github.io -> REPO
Processing row 2/419: Ultiverse
  https://github.com/ultiverse-io/ -> ORG
...

Processing complete! Results saved to: bnbchain-internal/EC Submission Final GitHub - Sheet1_with_status.csv

Summary:
  REPO: 245
  ORG: 89
  USER: 45
  INVALID: 32
  NO_LINK: 8
```

## Important Notes

- **Rate Limiting**: The script includes delays between requests to be respectful to GitHub's servers
- **User Agent**: Uses a realistic browser user agent to avoid being blocked
- **Error Handling**: Gracefully handles network errors and invalid URLs
- **Progress Tracking**: Shows real-time progress as it processes each link

## CSV Format

The script expects a CSV file with these columns:
- `Name`: Project/company name
- `Chain`: Blockchain name
- `Github Link`: GitHub URL

The output will include an additional `Link Status` column.

## Troubleshooting

- **Network Errors**: If you encounter network issues, the script will mark those links as "INVALID"
- **Large Files**: For very large CSV files, the script may take some time due to rate limiting
- **GitHub Blocking**: If GitHub temporarily blocks requests, wait a few minutes and try again
