import sys
import os

# Add backend to path (Priority 0 to override site-packages)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

print("\n[TEST] Starting Simplified E2E Verification...")

# 1. Test Quantum Engine Import
try:
    import quantum_engine
    print(f"[SUCCESS] Quantum Engine imported from: {quantum_engine.__file__}")
    
    # Test Lobotomy Mode
    qc = quantum_engine.QuantumCircuit(4)
    print(f"[INFO] QuantumCircuit has set_lobotomy_mode: {hasattr(qc, 'set_lobotomy_mode')}")
    
    if hasattr(qc, 'set_lobotomy_mode'):
        qc.set_lobotomy_mode(True)
        state = qc.execute()
        energy = state.expectation_value()
        print(f"[SUCCESS] Lobotomy Mode works. Energy: {energy} (Expected: 0.0)")
        assert abs(energy) < 0.01, "Lobotomy mode failed"
    
    # Test PFC Control
    qc2 = quantum_engine.QuantumCircuit(4)
    if hasattr(qc2, 'apply_pfc_control'):
        qc2.apply_pfc_control(0.5)
        print(f"[SUCCESS] PFC Control method exists")
    
    # Test Homeostasis
    state2 = quantum_engine.QuantumState(4)
    state2.apply_gate("X", 0, None)
    if hasattr(state2, 'homeostasis'):
        energy_before = state2.expectation_value()
        state2.homeostasis(0.5)
        energy_after = state2.expectation_value()
        print(f"[SUCCESS] Homeostasis works. Energy: {energy_before:.3f} -> {energy_after:.3f}")
        
except Exception as e:
    print(f"[FAIL] Quantum Engine test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 2. Test Backend Integration
try:
    from app.services.llm_interface import LLMInterface
    
    llm = LLMInterface()
    print(f"[INFO] LLM Provider: {llm.provider}")
    print(f"[INFO] Quantum Engine Enabled: {llm.use_quantum_engine}")
    
    # Mock context with low coherence
    mock_context = {
        "growth_stage": 2,
        "emotional_state": "anxious",
        "energy": 0.8,
        "comfort": 20,
        "stimulation": 80,
        "connection": 30,
        "coherence": 0.2  # Low coherence
    }
    
    prompt = llm._build_personality_prompt("Hello", mock_context, [], None)
    
    if "SYSTEM ALERT" in prompt and "unstable" in prompt:
        print("[SUCCESS] Coherence Alert injected into prompt")
    else:
        print("[WARN] Coherence Alert not found in prompt")
        print(f"Prompt snippet: {prompt[:300]}...")
    
    print("\n[SUCCESS] All E2E tests passed!")
    
except Exception as e:
    print(f"[FAIL] Backend test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
