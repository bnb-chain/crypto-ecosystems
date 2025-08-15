# BNB Chain Repository Analyzer

A comprehensive toolset for analyzing GitHub repositories from BNB Chain projects and automatically discovering relevant repositories from users and organizations.

## 🚀 Features

- **Smart Repository Discovery**: Automatically finds repositories from projects with "USER" or "ORG" Link Status
- **Intelligent Filtering**: Uses advanced scoring algorithms to identify BNB Chain related repositories
- **Content Analysis**: Analyzes README files and repository metadata for relevance
- **Batch Processing**: Handles large datasets with progress tracking and resume functionality
- **Configurable Scoring**: Customizable relevance thresholds and scoring criteria
- **Rate Limit Management**: Respects GitHub API limits with automatic retry logic
- **Comprehensive Output**: Detailed CSV output with confidence scores and metadata

## 📁 Project Structure

```
bnbchain-internal/
├── repo_analyzer.py          # Main repository analyzer script
├── batch_processor.py        # Batch processing for large datasets
├── test_analyzer.py          # Test suite for the analyzer
├── config.py                 # Configuration file for customization
├── requirements_repo_analyzer.txt  # Python dependencies
├── README.md                 # This file
├── README_repo_analyzer.md   # Detailed analyzer documentation
└── sheet_with_status.csv     # Input CSV file
```

## 🛠️ Installation

### Prerequisites

- Python 3.7 or higher
- GitHub Personal Access Token (recommended)

### Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements_repo_analyzer.txt
   ```

2. **Set GitHub token** (optional but recommended):
   ```bash
   # Windows (PowerShell)
   $env:GITHUB_TOKEN="your_github_token_here"
   
   # Linux/Mac
   export GITHUB_TOKEN="your_github_token_here"
   ```

3. **Prepare your CSV file**:
   - Ensure `sheet_with_status.csv` is in the same directory
   - CSV should have columns: `Name`, `Chain`, `Github Link`, `Link Status`

## 🚀 Usage

### Quick Start

Run the main analyzer on your CSV file:

```bash
python repo_analyzer.py
```

This will:
- Process all projects with "USER" or "ORG" Link Status
- Analyze repositories for BNB Chain relevance
- Create `sheet_with_status_with_repos.csv` with results

### Batch Processing

For large datasets, use the batch processor:

```bash
python batch_processor.py
```

Features:
- Processes users in configurable batches
- Progress tracking and resume functionality
- Saves intermediate results
- Merges all results at the end

### Testing

Run the test suite to verify functionality:

```bash
python test_analyzer.py
```

## ⚙️ Configuration

### Scoring System

The analyzer uses a configurable scoring system based on:

- **Repository Name & Description**: Keyword matching
- **Programming Language**: Solidity (25 points), other web3 languages (10 points)
- **Repository Activity**: Stars, forks, size
- **README Content**: BNB Chain indicators
- **Repository Status**: Penalties for forks/archived repos

### Customization

Edit `config.py` to modify:

- Relevance thresholds
- Scoring weights
- BNB Chain keywords
- GitHub API settings
- Output formatting

### Default Settings

- **Minimum Relevance Score**: 30/100
- **Batch Size**: 5 users per batch
- **Rate Limiting**: 0.1s between requests
- **Output Format**: CSV with additional metadata

## 📊 Output Format

The analyzer creates a comprehensive CSV with:

| Column | Description |
|--------|-------------|
| Name | Repository name |
| Chain | Always "bnb-chain" |
| Github Link | Repository URL |
| Link Status | Always "REPO" |
| Original Project | Source project name |
| Confidence Score | Relevance score (0-100) |
| Language | Primary programming language |
| Stars | GitHub star count |
| Forks | GitHub fork count |
| Size | Repository size in KB |
| Description | Truncated description |

## 🔍 How It Works

### 1. Repository Discovery
- Scans CSV for USER/ORG Link Status projects
- Extracts GitHub usernames from URLs
- Fetches all repositories via GitHub API

### 2. Relevance Analysis
- **Name/Description Scoring**: Matches against BNB Chain keywords
- **Language Analysis**: Prioritizes Solidity and web3 languages
- **Activity Metrics**: Considers stars, forks, and repository size
- **Content Analysis**: Analyzes README files for indicators
- **Quality Checks**: Penalizes forks and archived repositories

### 3. Smart Filtering
- Uses configurable scoring thresholds
- Combines multiple relevance factors
- Provides confidence scores for transparency
- Filters out irrelevant repositories

## 📈 Performance

### Rate Limits
- **Without token**: 60 requests/hour
- **With token**: 5,000 requests/hour
- **Automatic handling**: Waits when limits are reached

### Processing Speed
- **Small datasets** (< 50 users): ~5-10 minutes
- **Medium datasets** (50-200 users): ~30-60 minutes
- **Large datasets** (> 200 users): Use batch processor

### Memory Usage
- **Minimal**: Processes one user at a time
- **Scalable**: Handles unlimited repository counts
- **Efficient**: Streams data without loading everything into memory

## 🎯 Use Cases

### Primary Use Case
- **BNB Chain Ecosystem Mapping**: Discover all repositories from known projects
- **Developer Discovery**: Find active developers in the BNB Chain space
- **Project Analysis**: Understand the scope and activity of BNB Chain projects

### Secondary Use Cases
- **Research**: Academic or market research on BNB Chain ecosystem
- **Investment Due Diligence**: Analyze project activity and development
- **Partnership Discovery**: Find potential collaborators or integration partners

## 🔧 Troubleshooting

### Common Issues

1. **Rate Limit Errors**
   - Set a GitHub token
   - Wait for rate limit to reset
   - Use batch processor for large datasets

2. **Permission Errors**
   - Check file read/write permissions
   - Ensure CSV is not open in another application

3. **Network Errors**
   - Verify internet connection
   - Check GitHub API availability
   - Retry with exponential backoff

### Debug Mode

Enable verbose logging in `config.py`:

```python
LOGGING_CONFIG = {
    'VERBOSE': True,
    'SHOW_PROGRESS': True,
    'SHOW_SCORES': True,
    'SHOW_REJECTED': True,
}
```

## 📚 Examples

### Sample Output

```csv
Name,Chain,Github Link,Link Status,Original Project,Confidence Score,Language,Stars,Forks,Size,Description
fstswap-core,bnb-chain,https://github.com/fstswap/fstswap-core,REPO,FstSwap,85.0,Solidity,45,12,2048,Core smart contracts for FstSwap DEX...
fstswap-interface,bnb-chain,https://github.com/fstswap/fstswap-interface,REPO,FstSwap,72.0,TypeScript,23,8,1536,Frontend interface for FstSwap...
```

### Configuration Example

```python
# config.py
SCORING_CONFIG = {
    'MINIMUM_RELEVANCE_SCORE': 25,  # Lower threshold for more results
    'SCORES': {
        'SOLIDITY_LANGUAGE': 30,     # Higher weight for Solidity
        'KEYWORD_IN_NAME': 20,       # Higher weight for name matches
    }
}
```

## 🤝 Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Testing

Run the test suite:

```bash
python test_analyzer.py
```

### Code Style

- Follow PEP 8 guidelines
- Add type hints where possible
- Include docstrings for functions
- Use meaningful variable names

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- GitHub API for repository access
- BNB Chain community for ecosystem data
- Open source contributors and maintainers

## 📞 Support

For questions or issues:

1. Check the troubleshooting section
2. Review the configuration options
3. Run the test suite
4. Open an issue on GitHub

---

**Happy analyzing! 🚀**
