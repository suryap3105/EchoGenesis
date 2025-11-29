"""
Comprehensive Test Suite for Quantum Gates

Tests all single-qubit and 2-qubit gates in the quantum engine.
"""

import pytest
import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.quantum_bridge import QuantumBridge

class TestSingleQubitGates:
    """Test all single-qubit gates."""
    
    def setup_method(self):
        """Setup for each test."""
        self.qb = QuantumBridge()
        self.epsilon = 1e-6
    
    def test_hadamard_gate(self):
        """Test Hadamard gate creates superposition."""
        # Apply H to qubit 0 (should create (|0000> + |1000>)/√2)
        # In 4-qubit system: |0000> = index 0, |1000> = index 8
        H = np.array([[1, 1], [1, -1]], dtype=np.complex64) / np.sqrt(2)
        self.qb.apply_gate(H, 0)
        
        # Check probabilities
        probs = np.abs(self.qb.state_vector) ** 2
        
        # Indices 0 and 8 should have equal probability
        assert abs(probs[0] - 0.5) < self.epsilon
        assert abs(probs[8] - 0.5) < self.epsilon
        # All other indices should be zero
        for i in range(len(probs)):
            if i not in [0, 8]:
                assert probs[i] < self.epsilon
    
    def test_pauli_x_gate(self):
        """Test Pauli-X gate (bit flip)."""
        # X|0000> = |1000> (flip qubit 0)
        # |1000> = index 8 in 4-qubit system
        X = np.array([[0, 1], [1, 0]], dtype=np.complex64)
        self.qb.apply_gate(X, 0)
        
        probs = np.abs(self.qb.state_vector) ** 2
        assert abs(probs[8] - 1.0) < self.epsilon
        assert abs(probs[0]) < self.epsilon
    
    def test_pauli_y_gate(self):
        """Test Pauli-Y gate."""
        # Y|0000> = i|1000>
        # |1000> = index 8
        Y = np.array([[0, -1j], [1j, 0]], dtype=np.complex64)
        self.qb.apply_gate(Y, 0)
        
        # Should be in state i|1000> (index 8)
        assert abs(abs(self.qb.state_vector[8]) - 1.0) < self.epsilon
        assert abs(self.qb.state_vector[0]) < self.epsilon
    
    def test_pauli_z_gate(self):
        """Test Pauli-Z gate (phase flip)."""
        # First create superposition: H|0000> = (|0000> + |1000>)/√2
        H = np.array([[1, 1], [1, -1]], dtype=np.complex64) / np.sqrt(2)
        self.qb.apply_gate(H, 0)
        
        # Apply Z (should create (|0000> - |1000>)/√2)
        Z = np.array([[1, 0], [0, -1]], dtype=np.complex64)
        self.qb.apply_gate(Z, 0)
        
        # Apply H again (should return to |1000>)
        self.qb.apply_gate(H, 0)
        
        probs = np.abs(self.qb.state_vector) ** 2
        assert abs(probs[8] - 1.0) < self.epsilon
    
    def test_s_gate(self):
        """Test S gate (phase gate)."""
        # S = [[1, 0], [0, i]]
        H = np.array([[1, 1], [1, -1]], dtype=np.complex64) / np.sqrt(2)
        S = np.array([[1, 0], [0, 1j]], dtype=np.complex64)
        
        self.qb.apply_gate(H, 0)
        self.qb.apply_gate(S, 0)
        
        # State should have phase difference between |0000> and |1000>
        assert abs(abs(self.qb.state_vector[0]) - 1/np.sqrt(2)) < self.epsilon
        assert abs(abs(self.qb.state_vector[8]) - 1/np.sqrt(2)) < self.epsilon
    
    def test_rotation_gates(self):
        """Test RX, RY, RZ rotation gates."""
        theta = np.pi / 4
        
        # Test RX
        self.qb = QuantumBridge()
        self.qb.apply_gate(self.qb.rx(theta), 0)
        assert np.linalg.norm(self.qb.state_vector) - 1.0 < self.epsilon
        
        # Test RY
        self.qb = QuantumBridge()
        ry = np.array([
            [np.cos(theta/2), -np.sin(theta/2)],
            [np.sin(theta/2), np.cos(theta/2)]
        ], dtype=np.complex64)
        self.qb.apply_gate(ry, 0)
        assert np.linalg.norm(self.qb.state_vector) - 1.0 < self.epsilon
        
        # Test RZ
        self.qb = QuantumBridge()
        self.qb.apply_gate(self.qb.rz(theta), 0)
        assert np.linalg.norm(self.qb.state_vector) - 1.0 < self.epsilon


class TestTwoQubitGates:
    """Test 2-qubit gates."""
    
    def setup_method(self):
        """Setup for each test."""
        self.qb = QuantumBridge()
        self.epsilon = 1e-6
    
    def test_cnot_gate(self):
        """Test CNOT gate creates entanglement."""
        # Create superposition on qubit 0: (|0000> + |1000>)/√2
        H = np.array([[1, 1], [1, -1]], dtype=np.complex64) / np.sqrt(2)
        self.qb.apply_gate(H, 0)
        
        # Apply CNOT(0, 1) - should create Bell state
        # (|0000> + |1100>)/√2
        # |0000> = index 0, |1100> = index 12
        self.qb.cnot(0, 1)
        
        probs = np.abs(self.qb.state_vector) ** 2
        
        # Should be in state (|0000> + |1100>)/√2
        assert abs(probs[0] - 0.5) < self.epsilon  # |0000>
        assert abs(probs[12] - 0.5) < self.epsilon  # |1100>
        # All other indices should be near zero
        for i in range(len(probs)):
            if i not in [0, 12]:
                assert probs[i] < self.epsilon
    
    def test_cnot_control_target_order(self):
        """Test CNOT with different control/target."""
        # Set qubit 1 to |1>: X on qubit 1 creates |0100>
        # |0100> = index 4
        X = np.array([[0, 1], [1, 0]], dtype=np.complex64)
        self.qb.apply_gate(X, 1)
        
        # Apply CNOT(1, 0) - control=1, target=0
        # Should flip qubit 0 since qubit 1 is |1>
        # Result: |1100> (index 12)
        self.qb.cnot(1, 0)
        
        probs = np.abs(self.qb.state_vector) ** 2
        
        # Should flip qubit 0 since qubit 1 is |1>
        # Result: |1100> (index 12)
        assert abs(probs[12] - 1.0) < self.epsilon


class TestQuantumStateProperties:
    """Test quantum state properties and normalization."""
    
    def setup_method(self):
        """Setup for each test."""
        self.qb = QuantumBridge()
        self.epsilon = 1e-6
    
    def test_state_normalization(self):
        """Test that state remains normalized after gates."""
        gates = [
            ("H", self.qb.rx(np.pi/2)),
            ("RX", self.qb.rx(np.pi/4)),
            ("RY", self.qb.rx(np.pi/3)),
            ("RZ", self.qb.rz(np.pi/6))
        ]
        
        for name, gate in gates:
            self.qb = QuantumBridge()
            self.qb.apply_gate(gate, 0)
            norm = np.linalg.norm(self.qb.state_vector)
            assert abs(norm - 1.0) < self.epsilon, f"{name} gate broke normalization"
    
    def test_multiple_gate_sequence(self):
        """Test sequence of gates maintains normalization."""
        H = np.array([[1, 1], [1, -1]], dtype=np.complex64) / np.sqrt(2)
        X = np.array([[0, 1], [1, 0]], dtype=np.complex64)
        
        self.qb.apply_gate(H, 0)
        self.qb.apply_gate(X, 1)
        self.qb.cnot(0, 1)
        self.qb.apply_gate(H, 0)
        
        norm = np.linalg.norm(self.qb.state_vector)
        assert abs(norm - 1.0) < self.epsilon
    
    def test_optimize_state_normalization(self):
        """Test that optimize_state maintains normalization."""
        needs = {"comfort": 50, "stimulation": 50, "connection": 50}
        personality = {"anxiety": 0.5}
        
        result = self.qb.optimize_state(needs, personality)
        
        norm = np.linalg.norm(self.qb.state_vector)
        assert abs(norm - 1.0) < self.epsilon


class TestEntanglementCreation:
    """Test entanglement creation and measurement."""
    
    def setup_method(self):
        """Setup for each test."""
        self.qb = QuantumBridge()
        self.epsilon = 1e-6
    
    def test_bell_state_creation(self):
        """Test creation of Bell state (maximally entangled)."""
        # Create Bell state: (|00> + |11>)/√2
        H = np.array([[1, 1], [1, -1]], dtype=np.complex64) / np.sqrt(2)
        self.qb.apply_gate(H, 0)
        self.qb.cnot(0, 1)
        
        # Compute entanglement metrics
        metrics = self.qb.compute_entanglement_metrics()
        
        # Bell state should have high concurrence
        if "0-1" in metrics["concurrence"]:
            concurrence = metrics["concurrence"]["0-1"]
            assert concurrence > 0.9, f"Bell state concurrence too low: {concurrence}"
    
    def test_separable_state(self):
        """Test that product states have zero entanglement."""
        # Product state: |01> (no entanglement)
        X = np.array([[0, 1], [1, 0]], dtype=np.complex64)
        self.qb.apply_gate(X, 1)
        
        metrics = self.qb.compute_entanglement_metrics()
        
        # Should have zero concurrence
        if "0-1" in metrics["concurrence"]:
            concurrence = metrics["concurrence"]["0-1"]
            assert concurrence < 0.1, f"Product state has entanglement: {concurrence}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
