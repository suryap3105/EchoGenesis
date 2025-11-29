import asyncio
import os
import sys
import io

# Force UTF-8 for stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from app.quantum_bridge import QuantumBridge
from app.state_manager import StateManager
from app.services.llm_interface import LLMInterface

async def main():
    print("\n=== EchoGenesis System Verification ===\n")
    
    # 1. Initialize Quantum Engine
    print("[1/4] Initializing Rust Quantum Engine...")
    try:
        qb = QuantumBridge()
        print(f"   - Ground State Energy: {qb.ground_state_energy:.4f}")
        print(f"   - Entanglement Entropy: {qb.entanglement_entropy:.4f}")
        print("   [OK] Quantum Engine Online")
    except Exception as e:
        print(f"   [FAIL] Quantum Engine Error: {e}")
        return

    # 2. Initialize State Manager
    print("\n[2/4] Initializing State Manager...")
    try:
        # Use a temporary persistence directory for verification
        sm = StateManager(qb, persistence_dir="verification_data")
        print("   [OK] State Manager Online")
    except Exception as e:
        print(f"   [FAIL] State Manager Error: {e}")
        return

    # 3. Verify LLM Connection
    print("\n[3/4] Verifying Ollama Connection...")
    try:
        # Force provider to ollama for this test
        sm.llm_interface.provider = "ollama"
        stats = sm.llm_interface.get_conversation_stats()
        print(f"   - Provider: {stats['provider']}")
        print(f"   - Model: {stats['model']}")
        
        # Simple connectivity check
        print("   - Sending test ping to LLM...")
        response = await sm.llm_interface.generate_response("Say 'Online' if you can hear me.")
        if response:
            print(f"   - Response: {response.strip()}")
            print("   [OK] LLM Connection Verified")
        else:
            print("   [WARN] No response from LLM (Is Ollama running and model pulled?)")
    except Exception as e:
        print(f"   [FAIL] LLM Error: {e}")

    # 4. Full Interaction Loop
    print("\n[4/4] Testing Full Interaction Loop...")
    user_input = "I'm feeling a bit anxious about the future."
    print(f"   User: {user_input}")
    
    try:
        result = await sm.process_interaction(user_input)
        
        print(f"\n   Echo: {result['reply']}")
        print(f"   [State Update]")
        print(f"   - Emotional State: {result['emotional_state']}")
        print(f"   - Quantum Energy: {result['quantum_metrics']['ground_state_energy']:.4f}")
        print(f"   - Needs: {sm.state['needs']}")
        
        print("\n=== Verification Complete: SYSTEM OPERATIONAL ===")
        
    except Exception as e:
        print(f"   [FAIL] Interaction Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
