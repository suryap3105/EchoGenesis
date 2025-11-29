import sys
import os
import numpy as np

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

try:
    import quantum_engine
    print("Rust Quantum Engine Loaded")
except ImportError:
    print("Rust Quantum Engine NOT Found")
    sys.exit(1)

def test_noise_simulation():
    print("\nTesting Quantum Noise Simulation (Density Matrix)...")
    
    # 1. Create Bell State (Pure)
    circuit = quantum_engine.QuantumCircuit(2)
    circuit.h(0)
    circuit.cnot(0, 1)
    
    # Execute without noise
    dm_pure = circuit.execute_noisy((0.0, 0.0))
    entropy_pure = dm_pure.entropy()
    print(f"   Pure State Entropy: {entropy_pure:.6f} (Expected ~0.0)")
    
    if entropy_pure > 1e-5:
        print("Pure state entropy too high!")
        return False
        
    # 2. Execute with Phase Damping (Noise)
    # This should increase entropy
    dm_noisy = circuit.execute_noisy((0.0, 0.5)) # 50% phase damping
    entropy_noisy = dm_noisy.entropy()
    print(f"   Noisy State Entropy: {entropy_noisy:.6f} (Expected > 0.0)")
    
    if entropy_noisy <= entropy_pure:
        print("Noise did not increase entropy!")
        return False
        
    print("Noise Simulation Verified: Decoherence observed.")
    return True

def test_clustering_fallback():
    print("\nTesting Memory Clustering (NetworkX)...")
    from backend.app.services.memory_engine import MemoryEngine
    
    # Mock Memory Engine
    engine = MemoryEngine()
    engine.use_faiss = False # Force manual vector handling for test
    
    # Add dummy memories
    vectors = [
        [1.0, 0.0, 0.0], [0.9, 0.1, 0.0], # Cluster 1
        [0.0, 1.0, 0.0], [0.0, 0.9, 0.1], # Cluster 2
        [0.0, 0.0, 1.0]                   # Cluster 3
    ]
    
    engine.documents = [{"text": f"mem{i}", "id": i} for i in range(5)]
    engine.vectors = vectors
    
    # Run clustering
    engine._cluster_memories()
    
    if len(engine.clusters) > 1:
        print(f"Clustering Verified: Found {len(engine.clusters)} clusters.")
        return True
    else:
        print("Clustering Failed: Only 1 cluster found.")
        return False

if __name__ == "__main__":
    print("============================================================")
    print("Verifying Advanced Quantum Features (Phase 6)")
    print("============================================================")
    
    noise_ok = test_noise_simulation()
    cluster_ok = test_clustering_fallback()
    
    if noise_ok and cluster_ok:
        print("\nALL ADVANCED FEATURES VERIFIED")
        sys.exit(0)
    else:
        print("\nVERIFICATION FAILED")
        sys.exit(1)
