#!/usr/bin/env python3
"""
Quick test to verify EchoGenesis is working end-to-end
"""
import sys
import os
import asyncio

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

async def test_echo():
    print("="*60)
    print("  EchoGenesis System Test")
    print("="*60)
    
    # 1. Test quantum engine import
    print("\n[1/6] Testing Rust quantum engine import...")
    try:
        import quantum_engine
        state = quantum_engine.QuantumState(3)
        print("  ✓ Quantum engine imported successfully")
        print(f"  ✓ Created QuantumState with 3 qubits")
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False
    
    # 2. Test quantum circuit
    print("\n[2/6] Testing quantum circuit...")
    try:
        circuit = quantum_engine.QuantumCircuit(3)
        circuit.h(0)
        circuit.rx(1, 1.57)
        circuit.cnot(0, 1)
        result = circuit.execute()
        print(f"  ✓ Quantum circuit executed successfully")
        print(f"  ✓ Final state energy: {result.expectation_value():.3f}")
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False
    
    # 3. Test backend components
    print("\n[3/6] Testing backend components...")
    try:
        from app.quantum_bridge import QuantumBridge
        from app.state_manager import StateManager
        
        qb = QuantumBridge()
        sm = StateManager(qb, persistence_dir=".")
        print("  ✓ QuantumBridge initialized")
        print("  ✓ StateManager initialized")
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 4. Test quantum optimization
    print("\n[4/6] Testing quantum state optimization...")
    try:
        metrics = qb.optimize_state(
            {"comfort": 75, "stimulation": 50, "connection": 60},
            {"trust": 0.5, "curiosity": 0.7, "anxiety": 0.3},
            0.5
        )
        print(f"  ✓ Quantum optimization complete")
        print(f"    - Energy: {metrics['ground_state_energy']:.3f}")
        print(f"    - Entropy: {metrics['entanglement_entropy']:.3f}")
        print(f"    - Resonance: RGB({metrics['resonance_vector'][0]:.2f}, {metrics['resonance_vector'][1]:.2f}, {metrics['resonance_vector'][2]:.2f})")
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 5. Test LLM interface
    print("\n[5/6] Testing LLM interface...")
    try:
        from app.services.llm_interface import LLMInterface
        llm = LLMInterface()
        print(f"  ✓ LLM Interface initialized (Provider: {llm.provider})")
        if llm.provider == "ollama":
            print(f"    - Using model: {llm.model}")
        else:
            print(f"    - Using fallback mode (Ollama not available)")
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False
    
    # 6. Test full interaction flow
    print("\n[6/6] Testing full interaction flow...")
    try:
        response = await sm.process_interaction("Hello AADHI!")
        print(f"  ✓ Interaction processed successfully")
        print(f"  ✓ AADHI Response: \"{response['reply']}\"")
        print(f"  ✓ Emotional State: {response['emotional_state']}")
        print(f"  ✓ Growth Stage: {sm.state['growth_stage']} (Newborn)")
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "="*60)
    print("  ALL TESTS PASSED! ✓")
    print("="*60)
    print(f"\nAADHI is ready for conversation!")
    print(f"Run: python run_aadhi.py")
    print("="*60 + "\n")
    return True

if __name__ == "__main__":
    success = asyncio.run(test_echo())
    sys.exit(0 if success else 1)
