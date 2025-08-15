## 🎯 **Scoring System Overview**

The system assigns a **confidence score from 0-100** to each repository, with **30+ being considered relevant**. The score is calculated by combining multiple factors that indicate BNB Chain relevance.

## 📊 **Scoring Components**

### 1. **Repository Name & Description Analysis** (25 points max)
```python
# Repository name contains BNB keyword: +15 points
# Repository description contains BNB keyword: +10 points
```

**Example:**
- Repository named `"bnb-swap-contracts"` → +15 points
- Description mentions `"DeFi protocol on BSC"` → +10 points
- **Total: 25 points**

### 2. **Programming Language Scoring** (25 points max)
```python
# Solidity (smart contracts): +25 points
# Other web3 languages: +10 points
```

**Why this matters:**
- **Solidity** is the primary language for Ethereum/BNB Chain smart contracts
- **JavaScript/TypeScript** are common for DApp frontends
- **Python/Go/Rust** are used for blockchain tools and APIs

### 3. **Repository Activity Metrics** (15 points max)
```python
# Large repository (>1000 KB): +5 points
# Many stars (>10): +5 points  
# Many forks (>5): +5 points
```

**Activity indicators:**
- **Size**: Larger repos usually contain more substantial code
- **Stars**: Community approval and interest
- **Forks**: Other developers building on the project

### 4. **README Content Analysis** (40 points max)
```python
# Each BNB Chain indicator found: +8 points
# Maximum README score: 40 points
```

**README indicators include:**
- Blockchain terms: `"bnb chain"`, `"binance smart chain"`, `"bsc"`
- DeFi concepts: `"defi"`, `"dex"`, `"yield farming"`
- Technical stack: `"solidity"`, `"web3"`, `"hardhat"`

### 5. **Quality Penalties** (Negative points)
```python
# Repository is a fork: -10 points
# Repository is archived: -20 points
```

**Why penalize these:**
- **Forks**: Often less relevant than original projects
- **Archived**: Indicates abandoned or inactive projects

## 🔍 **Scoring Algorithm in Action**

Let me show you how a repository gets scored:

### **Example Repository: "fstswap-core"**
```python
# Repository data
name = "fstswap-core"
description = "Core smart contracts for FstSwap DEX on BSC"
language = "Solidity"
size = 2048  # KB
stars = 45
forks = 12
fork = False
archived = False
```

**Scoring breakdown:**
1. **Name analysis**: `"fstswap-core"` contains `"swap"` → +15 points
2. **Description analysis**: Contains `"dex"`, `"bsc"` → +20 points (2 keywords × 10)
3. **Language**: Solidity → +25 points
4. **Activity**: Large size, many stars, many forks → +15 points
5. **README analysis**: Let's say it contains 3 indicators → +24 points
6. **Quality**: No penalties → 0 points

**Total Score: 99/100** ✅ **Highly Relevant!**

### **Example Repository: "random-webapp"**
```python
# Repository data
name = "random-webapp"
description = "A simple web application"
language = "JavaScript"
size = 500  # KB
stars = 2
forks = 1
fork = True
archived = False
```

**Scoring breakdown:**
1. **Name analysis**: No BNB keywords → 0 points
2. **Description analysis**: No BNB keywords → 0 points
3. **Language**: JavaScript → +10 points
4. **Activity**: Small size, few stars/forks → 0 points
5. **README analysis**: No BNB indicators → 0 points
6. **Quality**: Fork penalty → -10 points

**Total Score: 0/100** ❌ **Not Relevant**

## ⚙️ **Configurable Scoring**

You can customize the scoring system in `config.py`:

```python
SCORING_CONFIG = {
    'MINIMUM_RELEVANCE_SCORE': 30,  # Lower = more results
    'SCORES': {
        'KEYWORD_IN_NAME': 15,        # Increase for name importance
        'KEYWORD_IN_DESCRIPTION': 10, # Increase for description importance
        'SOLIDITY_LANGUAGE': 25,      # Increase for Solidity importance
        'WEB3_LANGUAGE': 10,          # Adjust for other languages
        'README_INDICATOR': 8,        # Adjust for README importance
        'FORK_PENALTY': -10,          # Adjust fork penalty
        'ARCHIVED_PENALTY': -20,      # Adjust archive penalty
    }
}
```

## 🎯 **Scoring Thresholds**

- **0-29**: Not relevant (filtered out)
- **30-49**: Somewhat relevant (basic BNB Chain connection)
- **50-69**: Moderately relevant (clear BNB Chain usage)
- **70-89**: Highly relevant (strong BNB Chain focus)
- **90-100**: Extremely relevant (core BNB Chain project)

## 🔧 **Why This System Works**

1. **Multi-factor analysis**: Considers multiple aspects, not just keywords
2. **Weighted scoring**: More important factors get higher scores
3. **Quality filtering**: Penalizes low-quality indicators
4. **Configurable**: Can adjust based on your specific needs
5. **Transparent**: Each repository shows its score and reasoning

## �� **Pro Tips**

- **Lower the threshold** (e.g., to 25) for more inclusive results
- **Increase Solidity weight** if you want more smart contract focus
- **Adjust README weight** based on how much you trust documentation
- **Monitor false positives** and adjust penalties accordingly

This scoring system gives you a systematic way to identify truly relevant BNB Chain repositories while filtering out noise! 🚀