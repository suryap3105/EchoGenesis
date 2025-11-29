# Quick Test Script for EchoGenesis Components

import sys
import os

print("="*60)
print("EchoGenesis Component Test")
print("="*60)

# Test 1: LLM Interface
print("\n[TEST 1] LLM Interface")
try:
    from app.services.llm_interface import LLMInterface
    llm = LLMInterface()
    stats = llm.get_conversation_stats()
    print(f"[OK] LLM Interface initialized")
    print(f"  Provider: {stats['provider']}")
    print(f"  Model: {stats.get('model', 'N/A')}")
    print(f"  Exchanges: {stats['total_exchanges']}")
except Exception as e:
    print(f"[FAIL] LLM Interface: {e}")

# Test 2: Memory Engine (without FAISS for now)
print("\n[TEST 2] Memory Engine")
try:
    # Test if we can at least import
    import importlib.util
    spec = importlib.util.find_spec("faiss")
    if spec is None:
        print("[WARN] FAISS not available - memory engine will fail")
    else:
        print("[OK] FAISS module found")
        
    from app.services.memory_engine import MemoryEngine
    me = MemoryEngine()
    stats = me.get_cluster_stats()
    print(f"[OK] Memory Engine initialized")
    print(f"  Memories: {stats['total_memories']}")
    print(f"  Clusters: {stats['num_clusters']}")
    print(f"  METIS: {stats['metis_available']}")
    print(f"  ColBERT: {stats['colbert_available']}")
except Exception as e:
    print(f"[FAIL] Memory Engine: {e}")

# Test 3: Quantum Bridge
print("\n[TEST 3] Quantum Bridge")
try:
    from app.quantum_bridge import QuantumBridge
    qb = QuantumBridge()
    print(f"[OK] Quantum Bridge initialized")
    print(f"  Qubits: {qb.qubits}")
    print(f"  State vector size: {len(qb.state_vector)}")
except Exception as e:
    print(f"[FAIL] Quantum Bridge: {e}")

# Test 4: Developmental Engine
print("\n[TEST 4] Developmental Engine")
try:
    from app.services.developmental_engine import DevelopmentalEngine
    de = DevelopmentalEngine()
    print(f"[OK] Developmental Engine initialized")
    print(f"  Stages: {list(de.stages.values())}")
except Exception as e:
    print(f"[FAIL] Developmental Engine: {e}")

# Test 5: State Manager
print("\n[TEST 5] State Manager")
try:
    from app.state_manager import StateManager
    from app.quantum_bridge import QuantumBridge
    qb = QuantumBridge()
    sm = StateManager(qb)
    print(f"[OK] State Manager initialized")
    print(f"  Growth stage: {sm.state['growth_stage']}")
    print(f"  Emotional state: {sm.state['emotional_state']}")
except Exception as e:
    print(f"[FAIL] State Manager: {e}")

print("\n" + "="*60)
print("Test Complete")
print("="*60)
