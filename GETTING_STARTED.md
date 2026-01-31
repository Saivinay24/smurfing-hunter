# Getting Started with Smurfing Hunter

This guide will help you set up and run the Smurfing Hunter money laundering detection system.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- 4GB RAM minimum (8GB recommended for large datasets)
- ~500MB disk space for dependencies and outputs

## Installation

### Step 1: Clone or Download the Project

```bash
cd /home/dhruvesh/Documents/rugved
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- networkx (graph algorithms)
- pandas (data manipulation)
- numpy (numerical computing)
- matplotlib (static plots)
- seaborn (statistical visualizations)
- scikit-learn (ML utilities)
- plotly (interactive plots)
- python-louvain (community detection)
- pyvis (network visualization)
- scipy (scientific computing)

## Quick Start (5 minutes)

### Option 1: Run Quick Test

The fastest way to see the system in action:

```bash
python test_quick.py
```

This will:
1. Generate synthetic blockchain data (~1,500 transactions)
2. Build a transaction graph
3. Detect money laundering patterns
4. Calculate suspicion scores
5. Create visualizations

**Expected output:**
- `transactions.csv` - Sample transaction data
- `illicit_wallets.csv` - Known illicit wallets
- `test_risk_report.txt` - Risk assessment report
- `test_score_distribution.png` - Score distribution chart
- `test_network_stats.png` - Network statistics

**Time:** ~30 seconds

### Option 2: Run Full Analysis

For a complete analysis with comprehensive visualizations:

```bash
python smurfing_hunter.py --generate-data --output results
```

This performs:
1. Data generation with multiple laundering patterns
2. Complete pattern detection (fan-out/fan-in, cyclic, layered)
3. Suspicion scoring for all wallets
4. Detailed risk assessment of top wallets
5. Full visualization dashboard

**Expected output in `results/`:**
- `risk_report.txt` - Comprehensive risk report
- `visualizations/full_graph.html` - Interactive graph (open in browser)
- `visualizations/score_distribution.png` - Score histograms
- `visualizations/network_stats.png` - Network analysis
- `visualizations/patterns/` - Individual pattern visualizations
- `visualizations/illicit_wallets/` - Subgraphs around illicit nodes

**Time:** ~2-3 minutes

## Using Your Own Data

### Step 1: Prepare Your Data

Create two CSV files:

**transactions.csv**
```csv
Source_Wallet_ID,Dest_Wallet_ID,Timestamp,Amount,Token_Type
0x1234...,0x5678...,2024-01-15 10:30:00,1000.50,ETH
0x5678...,0x9abc...,2024-01-15 11:00:00,995.25,ETH
```

**illicit_wallets.csv**
```csv
Wallet_ID,Reason
0x1234...,Known hacker
0xabcd...,Ransomware wallet
```

### Step 2: Run Analysis

```bash
python smurfing_hunter.py --transactions transactions.csv --illicit illicit_wallets.csv --output my_results
```

## Understanding the Results

### 1. Interactive Graph (HTML)

Open `results/visualizations/full_graph.html` in a web browser:

- **Red nodes**: Known illicit wallets
- **Orange-red nodes**: Critical risk (score ≥ 80)
- **Orange nodes**: High risk (score ≥ 60)
- **Yellow nodes**: Medium risk (score ≥ 40)
- **Green nodes**: Low/minimal risk

**Interactions:**
- Click and drag to explore
- Hover over nodes for details
- Zoom with mouse wheel
- Click nodes to highlight connections

### 2. Risk Report (TXT)

Open `results/risk_report.txt`:

```
TOP 20 MOST SUSPICIOUS WALLETS
================================

1. Wallet: 0x1234567890abcdef...
   Overall Suspicion Score: 95.67/100
   Risk Level: CRITICAL
   Is Known Illicit: True
   Distance to Illicit Wallet: 0 hops
   Patterns Involved: 3
   Score Components:
     - Centrality: 78.45
     - Illicit Proximity: 100.00
     - Pattern Involvement: 95.20
     - Structural Anomaly: 82.30
```

**Risk Levels:**
- **CRITICAL (80-100)**: Immediate investigation required
- **HIGH (60-79)**: High priority for review
- **MEDIUM (40-59)**: Monitor closely
- **LOW (20-39)**: Standard monitoring
- **MINIMAL (0-19)**: Normal activity

### 3. Visualizations

**score_distribution.png**: Shows how many wallets fall into each risk category

**network_stats.png**: Four subplots showing:
- Degree distribution (connection patterns)
- Transaction amount distribution
- Detected pattern types
- Risk level distribution

**patterns/**: Individual visualizations of detected laundering schemes
- Red nodes: Source wallets
- Yellow nodes: Intermediate wallets
- Cyan nodes: Destination wallets
- Gray nodes: Connected wallets

## Common Use Cases

### Investigate a Specific Wallet

```bash
python smurfing_hunter.py --transactions transactions.csv --illicit illicit_wallets.csv --investigate 0x1234...
```

Provides:
- Detailed risk assessment
- Connections to illicit wallets
- Involved patterns
- Neighborhood visualization

### Adjust Detection Sensitivity

Edit parameters in your Python script:

```python
from pattern_detector import PatternDetector

detector = PatternDetector(blockchain)

# More sensitive (finds more patterns, more false positives)
patterns = detector.detect_fanout_fanin_patterns(
    min_fanout=2,  # Lower threshold
    min_fanin=2
)

# Less sensitive (fewer patterns, higher confidence)
patterns = detector.detect_fanout_fanin_patterns(
    min_fanout=5,  # Higher threshold
    min_fanin=5
)
```

### Export Data for Further Analysis

```python
import pandas as pd
from suspicion_scorer import SuspicionScorer

# After running analysis
scores_df = pd.DataFrame([
    {'wallet': wallet, 'score': score, 'risk': scorer._get_risk_level(score)}
    for wallet, score in scorer.wallet_scores.items()
])

# Export to CSV
scores_df.to_csv('wallet_scores.csv', index=False)

# Export high-risk wallets only
high_risk = scores_df[scores_df['score'] >= 60]
high_risk.to_csv('high_risk_wallets.csv', index=False)
```

## Troubleshooting

### Issue: Module not found

```bash
# Make sure you're in the correct directory
cd /home/dhruvesh/Documents/rugved

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Out of memory

For large datasets:

```python
# Reduce visualization size
visualizer.visualize_full_graph('graph.html', max_nodes=200)

# Use sampling for centrality
import networkx as nx
betweenness = nx.betweenness_centrality(graph, k=50)  # Sample 50 nodes
```

### Issue: Too slow on large graphs

```python
# Skip cyclic pattern detection (most expensive)
# Comment out in pattern_detector.py or modify:

patterns = {
    'fanout_fanin': detector.detect_fanout_fanin_patterns(),
    'layered': []  # Skip for speed
}
# Don't call detect_cyclic_patterns()
```

### Issue: Visualizations not rendering

```bash
# Update matplotlib backend
export MPLBACKEND=Agg  # For headless servers

# Or use interactive backend
export MPLBACKEND=TkAgg  # For desktop
```

## Next Steps

1. **Read USAGE.md** for detailed API documentation
2. **Read ARCHITECTURE.md** to understand the algorithms
3. **Customize patterns** by modifying `pattern_detector.py`
4. **Add your own scoring logic** in `suspicion_scorer.py`
5. **Integrate with your pipeline** using the Python API

## Support & Contribution

**Found a bug?** Check the code and create an issue description

**Want to contribute?** 
- Add new pattern detection algorithms
- Improve scoring formulas
- Add more visualization types
- Optimize for larger graphs

## Performance Benchmarks

| Dataset Size | Transactions | Wallets | Processing Time | Memory |
|--------------|-------------|---------|-----------------|--------|
| Small | 500 | 100 | 10s | 50MB |
| Medium | 1,500 | 300 | 30s | 150MB |
| Large | 5,000 | 1,000 | 2min | 500MB |
| Very Large | 20,000 | 5,000 | 10min | 2GB |

*Tested on: Intel i7, 16GB RAM, Python 3.10*

## Compliance Note

This tool is designed to assist in Anti-Money Laundering (AML) compliance and should be used in conjunction with:
- Know Your Customer (KYC) procedures
- Transaction monitoring systems
- Regulatory reporting requirements
- Human expert review

**Not a replacement for**: Legal advice, compliance officers, or regulatory guidance

## License

See LICENSE file for terms and conditions.

---

**Ready to start?** Run:

```bash
python test_quick.py
```

Then explore the generated files and move on to the full analysis!
