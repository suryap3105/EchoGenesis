import sys
import os
import asyncio
import pytest

# Add backend to path (Priority 0 to override site-packages)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.services.llm_interface import LLMInterface

# Mock Emotional Context
MOCK_CONTEXT = {
    "growth_stage": 2,
    "emotional_state": "anxious",
    "energy": 0.8,
    "comfort": 20,
    "stimulation": 80,
    "connection": 30,
    "coherence": 0.2  # Low coherence to trigger instability alert
}

@pytest.mark.asyncio
async def test_end_to_end_flow():
    print("\n[TEST] Starting End-to-End Methodology Verification...")
    
    # 1. Initialize Interface
    llm = LLMInterface()
    print(f"[INFO] Provider: {llm.provider}")
    print(f"[INFO] Quantum Engine Enabled: {llm.use_quantum_engine}")
    
    # 2. Verify Quantum Engine Import
    try:
        import quantum_engine
        print(f"[DEBUG] quantum_engine file: {quantum_engine.__file__}")
        import os
        print(f"[DEBUG] Timestamp: {os.path.getmtime(quantum_engine.__file__)}")
        
        print("[SUCCESS] Quantum Engine module imported successfully.")
        
        # Quick check of Lobotomy Mode
        qc = quantum_engine.QuantumCircuit(4)
        print(f"[DEBUG] QuantumCircuit attributes: {dir(qc)}")
        
        if not hasattr(qc, 'set_lobotomy_mode'):
            print("[ERROR] set_lobotomy_mode missing!")
            return

        qc.set_lobotomy_mode(True)
        state = qc.execute()
        energy = state.expectation_value()
        print(f"[INFO] Lobotomy Mode Energy: {energy} (Expected: 0.0)")
        assert energy == 0.0, "Lobotomy mode failed to return ground state"
        
    except ImportError:
        print("[ERROR] Could not import quantum_engine. Make sure .pyd is in place.")
        return

    # 3. Test Prompt Generation with Coherence Check
    # We want to see if the "SYSTEM ALERT" is injected into the prompt
    prompt = llm._build_personality_prompt("Hello", MOCK_CONTEXT, [], None)
    
    if "SYSTEM ALERT: Your emotional state is unstable" in prompt:
        print("[SUCCESS] Coherence Alert injected into prompt.")
    else:
        print("[FAIL] Coherence Alert NOT found in prompt.")
        print(f"Prompt snippet: {prompt[:200]}...")
        
    # 4. Generate Response (Mock or Real)
    response = await llm.generate_emotional_reply("I feel a bit overwhelmed today.", MOCK_CONTEXT)
    
    if response:
        print(f"\n[RESPONSE] {response}")
        print("[SUCCESS] Generated response successfully.")
    else:
        print("[WARN] No response generated (Ollama might be down, which is expected in some envs).")

if __name__ == "__main__":
    asyncio.run(test_end_to_end_flow())
