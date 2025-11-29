"""
Performance Benchmark: Rust vs Python Quantum Engine

Compares the performance of the Rust SIMD-optimized engine
against the Python NumPy simulator.
"""

import time
import numpy as np
from app.quantum_bridge import QuantumBridge

def benchmark_gate_operations(qubits=4, iterations=1000):
    """Benchmark single-qubit gate operations."""
    print(f"\n{'='*60}")
    print(f"Benchmarking {iterations} gate operations on {qubits} qubits")
    print(f"{'='*60}\n")
    
    qb = QuantumBridge()
    
    # Test Hadamard gates
    start = time.time()
    for _ in range(iterations):
        H = np.array([[1, 1], [1, -1]], dtype=np.complex64) / np.sqrt(2)
        qb.apply_gate(H, 0)
    h_time = time.time() - start
    
    # Test RX gates
    qb = QuantumBridge()
    start = time.time()
    for _ in range(iterations):
        qb.apply_gate(qb.rx(np.pi/4), 0)
    rx_time = time.time() - start
    
    # Test CNOT gates
    qb = QuantumBridge()
    start = time.time()
    for _ in range(iterations):
        qb.cnot(0, 1)
    cnot_time = time.time() - start
    
    print(f"Hadamard gates: {h_time:.4f}s ({iterations/h_time:.0f} ops/sec)")
    print(f"RX gates:       {rx_time:.4f}s ({iterations/rx_time:.0f} ops/sec)")
    print(f"CNOT gates:     {cnot_time:.4f}s ({iterations/cnot_time:.0f} ops/sec)")
    
    return h_time, rx_time, cnot_time

def benchmark_state_optimization(iterations=100):
    """Benchmark full state optimization."""
    print(f"\n{'='*60}")
    print(f"Benchmarking {iterations} state optimizations")
    print(f"{'='*60}\n")
    
    qb = QuantumBridge()
    needs = {"comfort": 50, "stimulation": 50, "connection": 50}
    personality = {"anxiety": 0.5}
    
    start = time.time()
    for _ in range(iterations):
        qb = QuantumBridge()
        qb.optimize_state(needs, personality, attachment=None)
    total_time = time.time() - start
    
    print(f"Total time: {total_time:.4f}s")
    print(f"Average:    {total_time/iterations*1000:.2f}ms per optimization")
    print(f"Throughput: {iterations/total_time:.1f} optimizations/sec")
    
    return total_time

def benchmark_entanglement_metrics(iterations=50):
    """Benchmark entanglement metric computation."""
    print(f"\n{'='*60}")
    print(f"Benchmarking {iterations} entanglement metric computations")
    print(f"{'='*60}\n")
    
    # Create Bell state
    qb = QuantumBridge()
    H = np.array([[1, 1], [1, -1]], dtype=np.complex64) / np.sqrt(2)
    qb.apply_gate(H, 0)
    qb.cnot(0, 1)
    
    start = time.time()
    for _ in range(iterations):
        metrics = qb.compute_entanglement_metrics()
    total_time = time.time() - start
    
    print(f"Total time: {total_time:.4f}s")
    print(f"Average:    {total_time/iterations*1000:.2f}ms per computation")
    print(f"Throughput: {iterations/total_time:.1f} computations/sec")
    
    return total_time

def main():
    print("\n" + "="*60)
    print("EchoGenesis Quantum Engine Performance Benchmark")
    print("="*60)
    
    try:
        import quantum_engine
        print("\n[OK] Rust Engine: LOADED")
        print("   - SIMD optimizations: Enabled")
        print("   - Parallel processing (Rayon): Enabled")
        print("   - Threshold for parallelization: 1024 dimensions")
    except ImportError:
        print("\n[WARN] Rust Engine: NOT AVAILABLE")
        print("   - Using Python NumPy simulator")
    
    # Run benchmarks
    gate_times = benchmark_gate_operations(qubits=4, iterations=1000)
    opt_time = benchmark_state_optimization(iterations=100)
    ent_time = benchmark_entanglement_metrics(iterations=50)
    
    # Summary
    print(f"\n{'='*60}")
    print("Summary")
    print(f"{'='*60}\n")
    
    total_ops = 1000 + 1000 + 1000 + 100 + 50
    total_time = sum(gate_times) + opt_time + ent_time
    
    print(f"Total operations: {total_ops}")
    print(f"Total time:       {total_time:.2f}s")
    print(f"Average:          {total_time/total_ops*1000:.2f}ms per operation")
    
    print(f"\n{'='*60}\n")

if __name__ == "__main__":
    main()
