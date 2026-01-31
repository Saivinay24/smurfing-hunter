# Smurfing Hunter: Money Laundering Detection in Blockchain

A Graph Neural Network-based system to detect money laundering patterns (Smurfing/Layering) in blockchain transaction networks.

## Overview

This tool identifies "Fan-out / Fan-in" structures where dirty money is:
1. Split into many small transactions (Fan-out)
2. Passed through intermediate wallets (Layering)
3. Re-aggregated in clean wallets (Fan-in)

## Features

- **Topology Detection**: Identifies gather-scatter and cyclic patterns
- **Obfuscation Handling**: Accounts for peeling chains and time delays
- **Suspicion Scoring**: Calculates risk scores based on graph centrality and illicit connections
- **Visualization**: Interactive and static graph visualizations with highlighted patterns

## Quick Start (One Command!)

```bash
# Run the complete demonstration
python run_demo.py
```

This single script will:
- Generate sample blockchain data
- Detect laundering patterns
- Calculate suspicion scores
- Create visualizations
- Generate risk reports

**Demo runs in ~5 seconds and shows all results!**

## Installation

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Option 1: Run Complete Demo (Recommended)
```bash
python run_demo.py
```

### Option 2: Full Analysis with Custom Data
```bash
python smurfing_hunter.py --transactions data.csv --illicit illicit.csv --output results
```

### Option 3: Generate Sample Data Only
```bash
python generate_sample_data.py
```

## Data Format

### transactions.csv
- Source_Wallet_ID: Origin wallet address
- Dest_Wallet_ID: Destination wallet address
- Timestamp: Transaction timestamp
- Amount: Transaction amount
- Token_Type: Cryptocurrency type

### illicit_wallets.csv
- Wallet_ID: Known illicit wallet address
- Reason: Why it's flagged as illicit

## Output

- Laundering graph visualization (HTML and PNG)
- Suspicion scores for all wallets
- Detected pattern statistics
- Risk assessment report
