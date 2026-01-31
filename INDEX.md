# Smurfing Hunter - Project Index

Complete money laundering detection system for blockchain transactions.

## 📁 Project Files Overview

### 🚀 Quick Start Files

| File | Purpose | When to Use |
|------|---------|-------------|
| [GETTING_STARTED.md](GETTING_STARTED.md) | Installation & setup guide | **START HERE** if you're new |
| [test_quick.py](test_quick.py) | Quick 30-second demo | First thing to run |
| [README.md](README.md) | Project overview | High-level understanding |

### 💻 Core Python Modules

| File | Lines | Purpose |
|------|-------|---------|
| [graph_builder.py](graph_builder.py) | 350 | Load transactions, build graph, extract features |
| [pattern_detector.py](pattern_detector.py) | 380 | Detect laundering patterns (fan-out/fan-in, cyclic, layered) |
| [suspicion_scorer.py](suspicion_scorer.py) | 450 | Calculate suspicion scores, risk assessment |
| [visualizer.py](visualizer.py) | 400 | Create interactive and static visualizations |
| [generate_sample_data.py](generate_sample_data.py) | 330 | Generate synthetic blockchain data with patterns |
| [smurfing_hunter.py](smurfing_hunter.py) | 400 | Main orchestrator, CLI interface |

**Total Core Code: ~2,310 lines**

### 📚 Documentation Files

| File | Lines | Purpose |
|------|-------|---------|
| [USAGE.md](USAGE.md) | 200 | Detailed API usage, examples, data formats |
| [ARCHITECTURE.md](ARCHITECTURE.md) | 300 | Technical deep-dive, algorithms, complexity |
| [SYSTEM_FLOW.md](SYSTEM_FLOW.md) | 250 | Visual system flow diagram |
| [PROJECT_SUMMARY.py](PROJECT_SUMMARY.py) | 280 | Complete project summary |

**Total Documentation: ~1,030 lines**

### 🛠️ Configuration Files

| File | Purpose |
|------|---------|
| [requirements.txt](requirements.txt) | Python dependencies |
| [.gitignore](.gitignore) | Git ignore rules |

## 🎯 File Navigation Guide

### For Different Users

#### 🆕 First-Time Users
1. Read: [GETTING_STARTED.md](GETTING_STARTED.md)
2. Run: `python test_quick.py`
3. Explore: Generated output files
4. Read: [README.md](README.md)

#### 👨‍💻 Developers
1. Read: [ARCHITECTURE.md](ARCHITECTURE.md)
2. Study: [graph_builder.py](graph_builder.py) → [pattern_detector.py](pattern_detector.py) → [suspicion_scorer.py](suspicion_scorer.py)
3. Reference: [USAGE.md](USAGE.md) for API
4. Extend: Add custom patterns or scoring

#### 🔬 Data Scientists
1. Read: [ARCHITECTURE.md](ARCHITECTURE.md) - Algorithm section
2. Study: [suspicion_scorer.py](suspicion_scorer.py) - Scoring formulas
3. Use: [generate_sample_data.py](generate_sample_data.py) for experiments
4. Reference: [USAGE.md](USAGE.md) for API integration

#### 🏢 Compliance Officers
1. Read: [GETTING_STARTED.md](GETTING_STARTED.md) - Understanding the Results
2. Run: `python smurfing_hunter.py --generate-data`
3. Review: `output/risk_report.txt`
4. Interpret: Risk levels and pattern types

#### 📊 Analysts
1. Run: Full analysis with your data
2. Open: `output/visualizations/full_graph.html`
3. Review: Pattern visualizations in `patterns/`
4. Export: Wallet scores for further analysis

## 📖 Documentation Map

```
Documentation Structure:

GETTING_STARTED.md (Entry Point)
├── Installation
├── Quick Start
├── Understanding Results
└── Troubleshooting

README.md (Overview)
├── Features
├── Installation
└── Basic Usage

USAGE.md (API Reference)
├── Command-Line Examples
├── Python API Examples
├── Data Format Specs
├── Advanced Features
└── Performance Tips

ARCHITECTURE.md (Technical Deep-Dive)
├── System Components
├── Algorithms & Complexity
├── Performance Analysis
├── Scalability
└── Extension Points

SYSTEM_FLOW.md (Visual Guide)
├── Data Flow Diagram
├── Phase-by-Phase Breakdown
├── Component Interaction
└── Input/Output Formats

PROJECT_SUMMARY.py (Complete Overview)
├── Problem Statement
├── Solution Overview
├── Key Features
├── Technical Stack
└── Deliverables
```

## 🔍 Code Organization

### Module Dependencies

```
graph_builder.py (Base)
    ↓
pattern_detector.py (Uses BlockchainGraph)
    ↓
suspicion_scorer.py (Uses BlockchainGraph + PatternDetector)
    ↓
visualizer.py (Uses all three above)
    ↓
smurfing_hunter.py (Orchestrates all)

generate_sample_data.py (Independent - generates test data)
test_quick.py (Uses all modules for demonstration)
```

### Class Hierarchy

```
BlockchainGraph
├── graph: nx.DiGraph
├── transactions: List[Dict]
├── illicit_wallets: Set[str]
└── Methods: load_*, get_*, detect_*

PatternDetector
├── blockchain: BlockchainGraph
├── detected_patterns: List[SmurfingPattern]
└── Methods: detect_*_patterns(), analyze_*

SuspicionScorer
├── blockchain: BlockchainGraph
├── pattern_detector: PatternDetector
├── wallet_scores: Dict[str, float]
└── Methods: calculate_*, get_*

GraphVisualizer
├── blockchain: BlockchainGraph
├── pattern_detector: PatternDetector
├── suspicion_scorer: SuspicionScorer
└── Methods: visualize_*, create_*, plot_*

SmurfingHunter (Main)
├── blockchain: BlockchainGraph
├── pattern_detector: PatternDetector
├── suspicion_scorer: SuspicionScorer
├── visualizer: GraphVisualizer
└── Methods: run_analysis(), investigate_wallet()
```

## 🎓 Learning Path

### Beginner Path (2 hours)
1. ⏱️ 10 min: Read [GETTING_STARTED.md](GETTING_STARTED.md)
2. ⏱️ 5 min: Run `python test_quick.py`
3. ⏱️ 15 min: Explore generated files
4. ⏱️ 20 min: Read [README.md](README.md) + [SYSTEM_FLOW.md](SYSTEM_FLOW.md)
5. ⏱️ 30 min: Run full analysis with `--generate-data`
6. ⏱️ 40 min: Experiment with [USAGE.md](USAGE.md) examples

### Intermediate Path (4 hours)
1. Complete Beginner Path
2. ⏱️ 1 hour: Study [ARCHITECTURE.md](ARCHITECTURE.md)
3. ⏱️ 1 hour: Read core module code
4. ⏱️ 1 hour: Try Python API examples
5. ⏱️ 1 hour: Analyze your own data

### Advanced Path (8+ hours)
1. Complete Intermediate Path
2. ⏱️ 2 hours: Deep dive into algorithms
3. ⏱️ 2 hours: Modify scoring weights
4. ⏱️ 2 hours: Add custom pattern detector
5. ⏱️ 2+ hours: Integrate with your pipeline

## 🔧 Modification Guide

### Want to... → Edit this file

| Goal | Primary File | Also See |
|------|-------------|----------|
| Add new pattern type | pattern_detector.py | ARCHITECTURE.md (Algorithms) |
| Change scoring weights | suspicion_scorer.py | ARCHITECTURE.md (Scoring) |
| Customize visualization | visualizer.py | USAGE.md (Visualization) |
| Add new data source | graph_builder.py | USAGE.md (Data Format) |
| Modify CLI | smurfing_hunter.py | - |
| Generate different test data | generate_sample_data.py | - |

## 📊 Output Files Reference

### After Running `test_quick.py`

| File | Type | Description |
|------|------|-------------|
| transactions.csv | Data | Sample blockchain transactions |
| illicit_wallets.csv | Data | Known illicit wallet list |
| test_risk_report.txt | Report | Risk assessment text report |
| test_score_distribution.png | Chart | Histogram of scores |
| test_network_stats.png | Chart | Network statistics |

### After Running `smurfing_hunter.py --generate-data`

| Path | Type | Description |
|------|------|-------------|
| output/risk_report.txt | Report | Comprehensive risk report |
| output/visualizations/full_graph.html | Interactive | Full network graph |
| output/visualizations/score_distribution.png | Chart | Score histogram |
| output/visualizations/network_stats.png | Chart | 4-panel statistics |
| output/visualizations/patterns/*.png | Charts | Individual pattern views |
| output/visualizations/illicit_wallets/*.png | Charts | Subgraph analyses |

## 🚀 Common Tasks Quick Reference

```bash
# First time setup
pip install -r requirements.txt

# Quick test (30 seconds)
python test_quick.py

# Full demo with sample data
python smurfing_hunter.py --generate-data --output results

# Analyze your data
python smurfing_hunter.py --transactions data.csv --illicit illicit.csv

# Investigate specific wallet
python smurfing_hunter.py --investigate 0xabc123... --transactions data.csv

# Generate only data (no analysis)
python generate_sample_data.py

# View project summary
python PROJECT_SUMMARY.py
```

## 📞 Support Reference

| Issue Type | Where to Look |
|------------|---------------|
| Installation problems | [GETTING_STARTED.md](GETTING_STARTED.md) - Installation section |
| Usage questions | [USAGE.md](USAGE.md) |
| Understanding results | [GETTING_STARTED.md](GETTING_STARTED.md) - Understanding Results |
| Algorithm details | [ARCHITECTURE.md](ARCHITECTURE.md) |
| Performance issues | [ARCHITECTURE.md](ARCHITECTURE.md) - Performance section |
| API reference | [USAGE.md](USAGE.md) - Python API |
| Data format | [USAGE.md](USAGE.md) - Data Format Requirements |

## 🏆 Project Statistics

- **Total Files**: 14
- **Total Lines of Code**: ~3,140
- **Total Documentation**: ~1,030 lines
- **Python Modules**: 6 core + 1 test
- **Documentation Files**: 5
- **Configuration Files**: 2
- **Algorithms Implemented**: 7+
- **Visualization Types**: 5
- **Pattern Types Detected**: 3

---

**Quick Command Reference Card**

```bash
# Essential Commands
pip install -r requirements.txt          # Install
python test_quick.py                     # Test
python smurfing_hunter.py --generate-data # Demo
python PROJECT_SUMMARY.py                # Info
```

**Essential Reading Order:**
1. GETTING_STARTED.md
2. README.md  
3. USAGE.md
4. ARCHITECTURE.md

---

*Last Updated: January 2026*
*Project Status: Production Ready*
