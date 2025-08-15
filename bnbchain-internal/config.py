"""
Configuration file for the BNB Chain Repository Analyzer
Modify these settings to customize the analyzer behavior.
"""

# Relevance scoring configuration
SCORING_CONFIG = {
    # Minimum score to consider a repository as BNB Chain related
    'MINIMUM_RELEVANCE_SCORE': 30,
    
    # Maximum possible score
    'MAX_SCORE': 100,
    
    # Score adjustments for different factors
    'SCORES': {
        'KEYWORD_IN_NAME': 15,        # Repository name contains BNB keyword
        'KEYWORD_IN_DESCRIPTION': 10, # Description contains BNB keyword
        'SOLIDITY_LANGUAGE': 25,      # Repository uses Solidity
        'WEB3_LANGUAGE': 10,          # Repository uses web3 languages
        'LARGE_SIZE': 5,              # Repository size > 1000 KB
        'MANY_STARS': 5,              # Repository has > 10 stars
        'MANY_FORKS': 5,              # Repository has > 5 forks
        'README_INDICATOR': 8,        # README contains BNB indicator
        'FORK_PENALTY': -10,          # Repository is a fork
        'ARCHIVED_PENALTY': -20,      # Repository is archived
    },
    
    # Thresholds for scoring
    'THRESHOLDS': {
        'LARGE_SIZE_KB': 1000,
        'MANY_STARS_COUNT': 10,
        'MANY_FORKS_COUNT': 5,
    }
}

# BNB Chain related keywords for scoring
BNB_KEYWORDS = [
    # Blockchain specific
    'bnb', 'binance', 'bsc', 'smart chain', 'beacon chain', 'opbnb',
    
    # DeFi and trading
    'defi', 'dex', 'swap', 'yield', 'liquidity', 'staking', 'governance',
    'dao', 'farming', 'mining', 'trading', 'finance', 'lending', 'borrowing',
    
    # Web3 and blockchain
    'web3', 'blockchain', 'cryptocurrency', 'token', 'contract', 'solidity',
    'ethereum', 'polygon', 'arbitrum', 'zksync', 'optimism',
    
    # Application domains
    'nft', 'gamefi', 'metaverse', 'gaming', 'gambling', 'lottery',
    'ai', 'artificial intelligence', 'machine learning', 'ml',
    
    # Technical terms
    'smart contract', 'dapp', 'decentralized', 'protocol', 'bridge',
    'wallet', 'exchange', 'marketplace', 'oracle', 'indexer'
]

# README content indicators
README_INDICATORS = [
    # BNB Chain specific
    'bnb chain', 'binance smart chain', 'bsc', 'beacon chain', 'opbnb',
    
    # Layer 2 and scaling
    'zksync', 'polygon zkevm', 'arbitrum', 'optimism', 'base',
    
    # Blockchain platforms
    'ethereum', 'polygon', 'avalanche', 'fantom', 'cronos',
    
    # DeFi protocols
    'defi', 'dex', 'swap', 'yield farming', 'liquidity mining',
    'staking', 'governance', 'dao', 'amm', 'orderbook',
    
    # Application types
    'nft', 'gamefi', 'metaverse', 'gaming', 'ai', 'artificial intelligence',
    
    # Technical stack
    'solidity', 'vyper', 'rust', 'go', 'typescript', 'javascript',
    'web3', 'ethers', 'wagmi', 'hardhat', 'foundry'
]

# GitHub API configuration
GITHUB_CONFIG = {
    'BASE_URL': 'https://api.github.com',
    'REPOS_PER_PAGE': 100,
    'REQUEST_DELAY': 0.1,  # seconds between requests
    'RATE_LIMIT_BUFFER': 60,  # seconds to wait before rate limit resets
    'MAX_PAGES': 100,  # maximum pages to fetch per user
}

# Output configuration
OUTPUT_CONFIG = {
    'DEFAULT_OUTPUT_SUFFIX': '_with_repos',
    'MAX_DESCRIPTION_LENGTH': 100,
    'INCLUDE_ADDITIONAL_FIELDS': True,
    'ADDITIONAL_FIELDS': [
        'Original Project',
        'Confidence Score', 
        'Language',
        'Stars',
        'Forks',
        'Size',
        'Description'
    ]
}

# Logging configuration
LOGGING_CONFIG = {
    'VERBOSE': True,
    'SHOW_PROGRESS': True,
    'SHOW_SCORES': True,
    'SHOW_REJECTED': True,
}
