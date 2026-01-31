"""
Quick Test Script
Demonstrates the basic functionality of the Smurfing Hunter system
"""

from generate_sample_data import DataGenerator
from graph_builder import BlockchainGraph
from pattern_detector import PatternDetector
from suspicion_scorer import SuspicionScorer
from visualizer import GraphVisualizer

print("=" * 80)
print("SMURFING HUNTER - QUICK TEST")
print("=" * 80)
print()

# Step 1: Generate sample data
print("Step 1: Generating sample blockchain data...")
generator = DataGenerator(seed=42)
transactions_file, illicit_file = generator.generate_complete_dataset()
print()

# Step 2: Load data into graph
print("Step 2: Building blockchain graph...")
blockchain = BlockchainGraph()
blockchain.load_transactions(transactions_file)
blockchain.load_illicit_wallets(illicit_file)
print()

# Step 3: Detect patterns
print("Step 3: Detecting money laundering patterns...")
detector = PatternDetector(blockchain)
patterns = detector.detect_all_patterns_from_illicit()
print()

# Display pattern summary
print("Pattern Detection Results:")
print("-" * 40)
for pattern_type, pattern_list in patterns.items():
    print(f"  {pattern_type}: {len(pattern_list)} patterns")
print()

# Step 4: Calculate suspicion scores
print("Step 4: Calculating suspicion scores...")
scorer = SuspicionScorer(blockchain, detector)
scores = scorer.calculate_all_scores()
print()

# Display top suspicious wallets
print("Top 5 Most Suspicious Wallets:")
print("-" * 40)
top_wallets = scorer.get_top_suspicious_wallets(5)
for i, (wallet, score) in enumerate(top_wallets, 1):
    risk = scorer._get_risk_level(score)
    is_illicit = wallet in blockchain.illicit_wallets
    print(f"{i}. {wallet[:20]}... | Score: {score:.2f} | Risk: {risk} | Illicit: {is_illicit}")
print()

# Step 5: Generate report
print("Step 5: Generating risk report...")
scorer.generate_risk_report("test_risk_report.txt")
print()

# Step 6: Create basic visualization
print("Step 6: Creating visualizations...")
visualizer = GraphVisualizer(blockchain, detector, scorer)
visualizer.plot_suspicion_score_distribution("test_score_distribution.png")
visualizer.create_network_statistics_plot("test_network_stats.png")
print()

print("=" * 80)
print("TEST COMPLETE!")
print("=" * 80)
print()
print("Generated files:")
print("  - transactions.csv")
print("  - illicit_wallets.csv")
print("  - test_risk_report.txt")
print("  - test_score_distribution.png")
print("  - test_network_stats.png")
print()
print("Run the full analysis with:")
print("  python smurfing_hunter.py --transactions transactions.csv --illicit illicit_wallets.csv")
