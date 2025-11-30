import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.quantum_bridge import QuantumBridge

def test_refinements():
    print("--- Verifying Methodological Refinements ---")
    bridge = QuantumBridge()
    
    # 1. Test Classical Mode (Ablation)
    print("\n1. Testing Classical Mode (Ablation)...")
    classical_res = bridge.optimize_state(
        {"comfort": 50, "stimulation": 50, "connection": 50},
        {"anxiety": 0.5},
        use_quantum=False
    )
    if classical_res["mode"] == "classical":
        print("   ✅ Classical mode active")
    else:
        print("   ❌ Classical mode failed")
        
    # 2. Test Stability Clamping
    print("\n2. Testing Stability Clamping (Extreme Inputs)...")
    # Input values > 100 should be clamped
    extreme_res = bridge.optimize_state(
        {"comfort": 999, "stimulation": -500, "connection": 50},
        {"anxiety": 2.0}, # Should be clamped to 1.0
        use_quantum=True
    )
    
    print(f"   Input: Comfort=999, Anxiety=2.0")
    print(f"   Result Stability: {extreme_res['stability']:.3f}")
    
    if 0 <= extreme_res['stability'] <= 1.0:
        print("   ✅ Stability clamped within [0, 1]")
    else:
        print(f"   ❌ Stability out of bounds: {extreme_res['stability']}")

    print("\n--- Verification Complete ---")

if __name__ == "__main__":
    test_refinements()
