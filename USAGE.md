# Smurfing Hunter - Usage Examples

This document provides detailed examples of using the Smurfing Hunter system.

## Quick Start

### 1. Generate Sample Data and Run Analysis

```bash
# Generate sample data and run complete analysis
python smurfing_hunter.py --generate-data --output results

# This will:
# - Generate synthetic blockchain transactions
# - Create known illicit wallet list
# - Detect laundering patterns
# - Calculate suspicion scores
# - Create visualizations
# - Generate risk report
```

### 2. Analyze Existing Data

```bash
# Analyze your own transaction data
python smurfing_hunter.py --transactions my_transactions.csv --illicit my_illicit_wallets.csv --output my_results
```

### 3. Investigate a Specific Wallet

```bash
# Deep dive into a suspicious wallet
python smurfing_hunter.py --transactions transactions.csv --illicit illicit_wallets.csv --investigate 0xabc123...
```

## Python API Usage

### Basic Analysis

```python
from graph_builder import BlockchainGraph
from pattern_detector import PatternDetector
from suspicion_scorer import SuspicionScorer

# Load data
blockchain = BlockchainGraph()
blockchain.load_transactions('transactions.csv')
blockchain.load_illicit_wallets('illicit_wallets.csv')

# Detect patterns
detector = PatternDetector(blockchain)
patterns = detector.detect_all_patterns_from_illicit()

# Calculate scores
scorer = SuspicionScorer(blockchain, detector)
scores = scorer.calculate_all_scores()

# Get top suspicious wallets
top_wallets = scorer.get_top_suspicious_wallets(10)
for wallet, score in top_wallets:
    print(f"{wallet}: {score:.2f}")
```

### Detecting Specific Patterns

```python
# Detect fan-out/fan-in patterns
fanout_patterns = detector.detect_fanout_fanin_patterns(
    min_fanout=5,    # Minimum split factor
    min_fanin=5,     # Minimum convergence factor
    max_hops=3       # Maximum path length
)

# Detect cyclic patterns
cyclic_patterns = detector.detect_cyclic_patterns(
    min_cycle_length=3,
    max_cycle_length=10
)

# Detect layered patterns from a specific wallet
layered = detector.detect_layered_patterns(
    source_wallet='0xabc123...',
    max_layers=5,
    min_split=3
)
```

### Wallet Risk Assessment

```python
# Get detailed risk assessment for a wallet
assessment = scorer.get_wallet_risk_assessment('0xabc123...')

print(f"Overall Score: {assessment['overall_suspicion_score']}")
print(f"Risk Level: {assessment['risk_level']}")
print(f"Patterns Involved: {assessment['patterns_involved']}")
print(f"Distance to Illicit: {assessment['illicit_connection']['distance_to_illicit']}")
```

### Creating Visualizations

```python
from visualizer import GraphVisualizer

visualizer = GraphVisualizer(blockchain, detector, scorer)

# Create interactive graph
visualizer.visualize_full_graph('graph.html', max_nodes=500)

# Visualize a specific pattern
for pattern in patterns['fanout_fanin'][:5]:
    visualizer.visualize_pattern(pattern, f'pattern_{pattern.pattern_type}.png')

# Create complete dashboard
visualizer.create_dashboard('dashboard')
```

## Understanding the Output

### Risk Levels

- **CRITICAL (80-100)**: Highly suspicious, likely involved in laundering
- **HIGH (60-79)**: Strong indicators of suspicious activity
- **MEDIUM (40-59)**: Some concerning patterns detected
- **LOW (20-39)**: Minor red flags
- **MINIMAL (0-19)**: Normal behavior

### Suspicion Score Components

1. **Centrality Score (20%)**: Based on network position and importance
   - High PageRank, betweenness, or closeness centrality
   - Indicates wallet is a hub in the network

2. **Illicit Proximity Score (35%)**: Distance to known illicit wallets
   - Direct connections to illicit wallets
   - Shortest path length to illicit nodes

3. **Pattern Involvement Score (30%)**: Participation in detected patterns
   - Number of patterns the wallet is involved in
   - Role in patterns (source, intermediate, destination)

4. **Structural Anomaly Score (15%)**: Unusual transaction patterns
   - Extreme fan-out or fan-in ratios
   - Rapid transaction sequences
   - Statistical outliers in behavior

### Detected Patterns

#### Fan-out/Fan-in Pattern
```
Source → [Multiple Intermediates] → Destination

Example:
Illicit_Wallet → [Wallet1, Wallet2, ..., Wallet10] → Clean_Wallet
```

#### Layered Pattern
```
Source → Layer1 → Layer2 → Layer3 → Destination

Example:
Dirty_Money → [5 wallets] → [10 wallets] → [5 wallets] → Clean_Money
```

#### Cyclic Pattern
```
Wallet_A → Wallet_B → Wallet_C → ... → Wallet_A

Example: Money moves in a circle to obscure origin
```

## Data Format Requirements

### transactions.csv

Required columns:
- `Source_Wallet_ID`: Wallet sending funds (string)
- `Dest_Wallet_ID`: Wallet receiving funds (string)
- `Timestamp`: Transaction time (datetime, format: YYYY-MM-DD HH:MM:SS)
- `Amount`: Transaction amount (float)
- `Token_Type`: Cryptocurrency type (string, e.g., BTC, ETH, USDT)

Example:
```csv
Source_Wallet_ID,Dest_Wallet_ID,Timestamp,Amount,Token_Type
0xabc123...,0xdef456...,2024-01-15 10:30:00,1000.50,ETH
0xdef456...,0xghi789...,2024-01-15 11:00:00,995.25,ETH
```

### illicit_wallets.csv

Required columns:
- `Wallet_ID`: Known illicit wallet address (string)
- `Reason`: Why it's flagged (string, optional)

Example:
```csv
Wallet_ID,Reason
0xabc123...,Known hacker
0xdef456...,Ransomware wallet
0xghi789...,Dark web marketplace
```

## Advanced Features

### Custom Pattern Detection

```python
# Analyze wallet neighborhood
neighborhood = detector.analyze_wallet_neighborhood(
    wallet='0xabc123...',
    radius=2  # Number of hops
)

print(f"Local density: {neighborhood['local_density']}")
print(f"Illicit neighbors: {neighborhood['illicit_neighbors']}")
```

### Peeling Chain Detection

```python
# Detect peeling chains (small amounts taken at each hop)
chain = blockchain.detect_peeling_chain(
    wallet='0xabc123...',
    threshold=0.1  # 10% maximum peel
)

if chain:
    print(f"Peeling chain detected: {len(chain)} hops")
```

### Subgraph Analysis

```python
# Extract subgraph around a wallet
subgraph = blockchain.get_subgraph_around_wallet(
    wallet='0xabc123...',
    hops=3
)

print(f"Subgraph has {subgraph.number_of_nodes()} nodes")
```

## Performance Tips

1. **Large Graphs**: For graphs with >10,000 nodes, increase max_nodes limit in visualization
2. **Pattern Detection**: Adjust min_fanout, min_fanin parameters to reduce false positives
3. **Computation Time**: Cyclic pattern detection can be slow on large graphs
4. **Memory Usage**: Consider sampling large datasets for initial exploration

## Troubleshooting

### Common Issues

**Problem**: "CSV must contain columns: ..."
- **Solution**: Ensure your CSV has all required columns with exact names

**Problem**: Visualizations not showing
- **Solution**: Install required packages: `pip install -r requirements.txt`

**Problem**: Too many patterns detected
- **Solution**: Increase threshold parameters (min_fanout, min_fanin, etc.)

**Problem**: No patterns detected
- **Solution**: Lower threshold parameters or ensure illicit wallets are in the graph

## Citation

If you use this tool in your research, please cite:

```bibtex
@software{smurfing_hunter,
  title={Smurfing Hunter: Money Laundering Detection in Blockchain},
  author={Your Name},
  year={2024},
  url={https://github.com/yourusername/smurfing-hunter}
}
```
