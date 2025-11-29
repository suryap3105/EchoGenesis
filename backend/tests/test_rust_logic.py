import pytest
import numpy as np
from app.quantum_bridge import QuantumBridge

def test_quantum_state_initialization():
    """Verify that the quantum state initializes to |0...0>."""
    bridge = QuantumBridge()
    assert bridge.qubits == 4
    # Check |0000> amplitude is 1.0
    assert np.isclose(abs(bridge.state_vector[0]), 1.0)
    # Check total probability is 1.0
    assert np.isclose(np.sum(np.abs(bridge.state_vector)**2), 1.0)

def test_pauli_x_gate():
    """Verify X gate flips |0> to |1>."""
    bridge = QuantumBridge()
    # Apply X to qubit 0
    x_gate = np.array([[0, 1], [1, 0]], dtype=np.complex64)
    bridge.apply_gate(x_gate, 0)
    
    # Should be |1000> (if qubit 0 is LSB or MSB depending on convention)
    # In our kron(op, I) construction, qubit 0 is the MSB (leftmost in tensor product)
    # So |1000> corresponds to index 2^(N-1) = 8
    
    # Let's check which index has probability 1
    probs = np.abs(bridge.state_vector)**2
    idx = np.argmax(probs)
    assert np.isclose(probs[idx], 1.0)
    # With 4 qubits, if we apply to q0 (first in loop), it should be index 8 (1000)
    assert idx == 8

def test_entanglement_entropy():
    """Verify entropy calculation for an entangled state."""
    bridge = QuantumBridge()
    # Create Bell State |00> + |11> on first two qubits (indices 0 and 1)
    # H on q0
    h_gate = np.array([[1, 1], [1, -1]], dtype=np.complex64) / np.sqrt(2)
    bridge.apply_gate(h_gate, 0)
    
    # CNOT q0 -> q1
    # Our CNOT implementation in Python is currently a placeholder/mock or simplified.
    # The current QuantumBridge.cnot is a pass.
    # So we can't test CNOT directly unless we implement it fully.
    
    # However, we can test the entropy function itself by manually setting a state.
    # Set state to (|0000> + |1100>) / sqrt(2)
    bridge.state_vector = np.zeros(16, dtype=np.complex64)
    bridge.state_vector[0] = 1.0 / np.sqrt(2)
    bridge.state_vector[12] = 1.0 / np.sqrt(2) # 1100 is 12 (8+4)
    
    # Calculate metrics
    metrics = bridge.calculate_metrics()
    entropy = metrics["entanglement_entropy"]
    
    # Entropy of Bell state is 1 bit (if normalized by qubits, 1/N)
    # Our implementation: -sum(p log p) / N
    # p = 0.5, 0.5
    # - (0.5*-1 + 0.5*-1) = 1.0
    # Divided by 4 qubits = 0.25
    assert np.isclose(entropy, 0.25)

def test_hamiltonian_evolution():
    """Verify that energy changes with needs."""
    bridge = QuantumBridge()
    
    # High comfort -> Low energy (Ground state)
    metrics_calm = bridge.optimize_state({"comfort": 100, "stimulation": 0}, {}, 0.5)
    
    # Low comfort -> High energy (Excited state)
    metrics_agitated = bridge.optimize_state({"comfort": 0, "stimulation": 100}, {}, 0.5)
    
    assert metrics_agitated["ground_state_energy"] > metrics_calm["ground_state_energy"]
