"""
Pattern Detector Module
Detects money laundering patterns including fan-out/fan-in and cyclic structures
"""

import networkx as nx
from typing import List, Dict, Set, Tuple
from collections import defaultdict, deque
import numpy as np


class SmurfingPattern:
    """
    Represents a detected smurfing pattern
    """
    def __init__(self, source_wallets: Set[str], intermediate_wallets: Set[str], 
                 destination_wallets: Set[str], pattern_type: str):
        self.source_wallets = source_wallets
        self.intermediate_wallets = intermediate_wallets
        self.destination_wallets = destination_wallets
        self.pattern_type = pattern_type  # 'fanout_fanin', 'cyclic', 'layered'
        self.suspicion_score = 0.0
        self.total_amount = 0.0
        self.time_span = None
        
    def __repr__(self):
        return (f"SmurfingPattern(type={self.pattern_type}, "
                f"sources={len(self.source_wallets)}, "
                f"intermediates={len(self.intermediate_wallets)}, "
                f"destinations={len(self.destination_wallets)}, "
                f"score={self.suspicion_score:.3f})")


class PatternDetector:
    """
    Detects various money laundering patterns in blockchain graphs
    """
    
    def __init__(self, blockchain_graph):
        self.graph = blockchain_graph.graph
        self.blockchain = blockchain_graph
        self.detected_patterns = []
        
    def detect_fanout_fanin_patterns(self, min_fanout: int = 3, min_fanin: int = 3,
                                     max_hops: int = 4) -> List[SmurfingPattern]:
        """
        Detect fan-out/fan-in patterns:
        Source(s) -> Multiple Intermediates -> Destination(s)
        
        Args:
            min_fanout: Minimum number of wallets in fan-out
            min_fanin: Minimum number of wallets in fan-in
            max_hops: Maximum path length to consider
        """
        patterns = []
        
        # Iterate through all nodes as potential sources
        for source in self.graph.nodes():
            successors = list(self.graph.successors(source))
            
            # Check if this node fans out
            if len(successors) < min_fanout:
                continue
            
            # For each intermediate layer, check if they fan-in
            intermediate_wallets = set(successors)
            
            # Get all potential destinations (nodes that receive from multiple intermediates)
            destination_candidates = defaultdict(set)
            
            for intermediate in intermediate_wallets:
                for dest in self.graph.successors(intermediate):
                    destination_candidates[dest].add(intermediate)
            
            # Find destinations that receive from multiple intermediates (fan-in)
            for dest, sources in destination_candidates.items():
                if len(sources) >= min_fanin:
                    # Calculate pattern metrics
                    total_amount = 0
                    for intermediate in sources:
                        if self.graph.has_edge(intermediate, dest):
                            total_amount += self.graph[intermediate][dest]['amount']
                    
                    pattern = SmurfingPattern(
                        source_wallets={source},
                        intermediate_wallets=sources,
                        destination_wallets={dest},
                        pattern_type='fanout_fanin'
                    )
                    pattern.total_amount = total_amount
                    pattern.suspicion_score = self._calculate_pattern_suspicion(pattern)
                    
                    patterns.append(pattern)
        
        self.detected_patterns.extend(patterns)
        return patterns
    
    def detect_cyclic_patterns(self, min_cycle_length: int = 3, 
                              max_cycle_length: int = 10) -> List[SmurfingPattern]:
        """
        Detect cyclic patterns where money flows in a loop
        """
        patterns = []
        
        # Find all simple cycles
        try:
            # Limit search to avoid performance issues
            cycles = []
            cycle_count = 0
            for cycle in nx.simple_cycles(self.graph):
                cycle_count += 1
                if min_cycle_length <= len(cycle) <= max_cycle_length:
                    cycles.append(cycle)
                if len(cycles) >= 100:  # Reduced limit for faster execution
                    break
                if cycle_count >= 5000:  # Stop after checking enough cycles
                    break
            
            for cycle in cycles:
                # Calculate cycle metrics
                total_amount = sum(
                    self.graph[cycle[i]][cycle[(i+1) % len(cycle)]]['amount']
                    for i in range(len(cycle))
                )
                
                pattern = SmurfingPattern(
                    source_wallets={cycle[0]},
                    intermediate_wallets=set(cycle[1:-1]) if len(cycle) > 2 else set(),
                    destination_wallets={cycle[-1]},
                    pattern_type='cyclic'
                )
                pattern.total_amount = total_amount
                pattern.suspicion_score = self._calculate_pattern_suspicion(pattern)
                
                patterns.append(pattern)
        
        except (nx.NetworkXNoCycle, StopIteration):
            pass
        
        self.detected_patterns.extend(patterns)
        return patterns
    
    def detect_layered_patterns(self, source_wallet: str, max_layers: int = 5,
                               min_split: int = 2) -> List[SmurfingPattern]:
        """
        Detect layered money laundering starting from a source wallet
        Uses BFS to find multiple layers of splitting and recombining
        
        Args:
            source_wallet: Starting wallet (typically an illicit one)
            max_layers: Maximum number of layers to explore
            min_split: Minimum split factor at each layer
        """
        patterns = []
        
        if not self.graph.has_node(source_wallet):
            return patterns
        
        # BFS layer by layer
        current_layer = {source_wallet}
        all_intermediates = set()
        
        for layer in range(max_layers):
            next_layer = set()
            
            for wallet in current_layer:
                successors = set(self.graph.successors(wallet))
                
                # If this wallet splits to multiple (layering behavior)
                if len(successors) >= min_split:
                    next_layer.update(successors)
                    all_intermediates.update(successors)
            
            if not next_layer:
                break
            
            current_layer = next_layer
        
        # Check if final layer converges (fan-in)
        final_destinations = defaultdict(int)
        for intermediate in all_intermediates:
            for dest in self.graph.successors(intermediate):
                if dest not in all_intermediates and dest != source_wallet:
                    final_destinations[dest] += 1
        
        # Find convergence points
        convergence_wallets = {w for w, count in final_destinations.items() if count >= min_split}
        
        if convergence_wallets:
            pattern = SmurfingPattern(
                source_wallets={source_wallet},
                intermediate_wallets=all_intermediates,
                destination_wallets=convergence_wallets,
                pattern_type='layered'
            )
            
            # Calculate total amount
            total_amount = 0
            for dest in convergence_wallets:
                for intermediate in all_intermediates:
                    if self.graph.has_edge(intermediate, dest):
                        total_amount += self.graph[intermediate][dest]['amount']
            
            pattern.total_amount = total_amount
            pattern.suspicion_score = self._calculate_pattern_suspicion(pattern)
            patterns.append(pattern)
        
        self.detected_patterns.extend(patterns)
        return patterns
    
    def detect_all_patterns_from_illicit(self) -> Dict[str, List[SmurfingPattern]]:
        """
        Run all pattern detection algorithms starting from known illicit wallets
        """
        all_patterns = {
            'fanout_fanin': [],
            'cyclic': [],
            'layered': []
        }
        
        # Detect general patterns
        print("Detecting fan-out/fan-in patterns...")
        fanout_patterns = self.detect_fanout_fanin_patterns()
        all_patterns['fanout_fanin'] = fanout_patterns
        print(f"Found {len(fanout_patterns)} fan-out/fan-in patterns")
        
        print("Detecting cyclic patterns...")
        cyclic_patterns = self.detect_cyclic_patterns()
        all_patterns['cyclic'] = cyclic_patterns
        print(f"Found {len(cyclic_patterns)} cyclic patterns")
        
        # Detect layered patterns from each illicit wallet
        print("Detecting layered patterns from illicit wallets...")
        for illicit_wallet in self.blockchain.illicit_wallets:
            if self.graph.has_node(illicit_wallet):
                layered = self.detect_layered_patterns(illicit_wallet)
                all_patterns['layered'].extend(layered)
        
        print(f"Found {len(all_patterns['layered'])} layered patterns")
        
        return all_patterns
    
    def _calculate_pattern_suspicion(self, pattern: SmurfingPattern) -> float:
        """
        Calculate suspicion score for a pattern based on multiple factors
        """
        score = 0.0
        
        # Factor 1: Number of intermediaries (more = more suspicious)
        intermediary_score = min(len(pattern.intermediate_wallets) / 10.0, 1.0) * 30
        score += intermediary_score
        
        # Factor 2: Connection to illicit wallets
        illicit_count = 0
        all_wallets = (pattern.source_wallets | pattern.intermediate_wallets | 
                      pattern.destination_wallets)
        
        for wallet in all_wallets:
            if wallet in self.blockchain.illicit_wallets:
                illicit_count += 1
        
        illicit_score = min(illicit_count / len(all_wallets), 1.0) * 40 if all_wallets else 0
        score += illicit_score
        
        # Factor 3: Amount (larger amounts more suspicious)
        # Normalize by median transaction amount
        if pattern.total_amount > 0:
            amounts = [data['amount'] for _, _, data in self.graph.edges(data=True)]
            median_amount = np.median(amounts) if amounts else 1
            amount_score = min(pattern.total_amount / (median_amount * 10), 1.0) * 30
            score += amount_score
        
        return min(score, 100.0)
    
    def find_shortest_path_to_illicit(self, wallet: str) -> Tuple[List[str], float]:
        """
        Find shortest path from wallet to any illicit wallet
        Returns (path, distance) or ([], inf) if no path exists
        """
        min_distance = float('inf')
        shortest_path = []
        
        for illicit in self.blockchain.illicit_wallets:
            if illicit in self.graph:
                try:
                    path = nx.shortest_path(self.graph, wallet, illicit)
                    if len(path) < min_distance:
                        min_distance = len(path)
                        shortest_path = path
                except nx.NetworkXNoPath:
                    continue
        
        return shortest_path, min_distance if shortest_path else float('inf')
    
    def analyze_wallet_neighborhood(self, wallet: str, radius: int = 2) -> Dict:
        """
        Analyze the neighborhood of a wallet for suspicious patterns
        """
        if not self.graph.has_node(wallet):
            return {}
        
        subgraph = self.blockchain.get_subgraph_around_wallet(wallet, radius)
        
        analysis = {
            'wallet': wallet,
            'local_nodes': subgraph.number_of_nodes(),
            'local_edges': subgraph.number_of_edges(),
            'local_density': nx.density(subgraph),
            'clustering_coefficient': nx.clustering(subgraph.to_undirected(), wallet),
        }
        
        # Count illicit connections
        illicit_neighbors = sum(
            1 for n in subgraph.nodes() 
            if n in self.blockchain.illicit_wallets
        )
        analysis['illicit_neighbors'] = illicit_neighbors
        analysis['illicit_ratio'] = illicit_neighbors / subgraph.number_of_nodes()
        
        return analysis
    
    def get_pattern_statistics(self) -> Dict:
        """
        Get statistics about detected patterns
        """
        if not self.detected_patterns:
            return {}
        
        by_type = defaultdict(list)
        for pattern in self.detected_patterns:
            by_type[pattern.pattern_type].append(pattern)
        
        stats = {
            'total_patterns': len(self.detected_patterns),
            'by_type': {ptype: len(patterns) for ptype, patterns in by_type.items()},
            'avg_suspicion_score': np.mean([p.suspicion_score for p in self.detected_patterns]),
            'max_suspicion_score': max([p.suspicion_score for p in self.detected_patterns]),
            'total_amount_flagged': sum([p.total_amount for p in self.detected_patterns]),
        }
        
        return stats
