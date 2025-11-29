"""
Test Suite for Entanglement Metrics

Tests mutual information, concurrence, tangle, negativity, and entanglement spectrum.
"""

import pytest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.entanglement_metrics import EntanglementMetrics


class TestMutualInformation:
    """Test mutual information calculation."""
    
    def test_separable_state_zero_mi(self):
        """Test that separable states have zero mutual information."""
        # Product state |00>
        state = np.array([1, 0, 0, 0], dtype=np.complex128)
        
        mi = EntanglementMetrics.mutual_information(state, 0, 1, 2)
        
        assert abs(mi) < 1e-6
    
    def test_bell_state_high_mi(self):
        """Test that Bell states have high mutual information."""
        # Bell state (|00> + |11>)/√2
        state = np.array([1/np.sqrt(2), 0, 0, 1/np.sqrt(2)], dtype=np.complex128)
        
        mi = EntanglementMetrics.mutual_information(state, 0, 1, 2)
        
        # Bell state should have MI ≈ 2 (maximum for 2 qubits)
        assert mi > 1.5


class TestConcurrence:
    """Test concurrence calculation."""
    
    def test_separable_state_zero_concurrence(self):
        """Test that separable states have zero concurrence."""
        # Product state |01>
        state = np.array([0, 1, 0, 0], dtype=np.complex128)
        
        C = EntanglementMetrics.concurrence(state, 0, 1, 2)
        
        assert abs(C) < 1e-6
    
    def test_bell_state_max_concurrence(self):
        """Test that Bell states have maximum concurrence."""
        # Bell state (|00> + |11>)/√2
        state = np.array([1/np.sqrt(2), 0, 0, 1/np.sqrt(2)], dtype=np.complex128)
        
        C = EntanglementMetrics.concurrence(state, 0, 1, 2)
        
        # Bell state should have C = 1
        assert abs(C - 1.0) < 0.1
    
    def test_partial_entanglement(self):
        """Test partially entangled state."""
        # Partially entangled: 0.8|00> + 0.6|11>
        state = np.array([0.8, 0, 0, 0.6], dtype=np.complex128)
        state = state / np.linalg.norm(state)
        
        C = EntanglementMetrics.concurrence(state, 0, 1, 2)
        
        # Should have 0 < C < 1
        assert 0.5 < C < 1.0


class TestTangle:
    """Test tangle calculation."""
    
    def test_tangle_is_squared_concurrence(self):
        """Test that tangle = concurrence²."""
        # Bell state
        state = np.array([1/np.sqrt(2), 0, 0, 1/np.sqrt(2)], dtype=np.complex128)
        
        C = EntanglementMetrics.concurrence(state, 0, 1, 2)
        tau = EntanglementMetrics.tangle(state, 0, 1, 2)
        
        assert abs(tau - C**2) < 1e-6


class TestNegativity:
    """Test negativity calculation."""
    
    def test_separable_state_zero_negativity(self):
        """Test that separable states have zero negativity."""
        # Product state
        state = np.array([1, 0, 0, 0], dtype=np.complex128)
        
        N = EntanglementMetrics.negativity(state, 0, 1, 2)
        
        assert abs(N) < 1e-6
    
    def test_bell_state_positive_negativity(self):
        """Test that entangled states have positive negativity."""
        # Bell state
        state = np.array([1/np.sqrt(2), 0, 0, 1/np.sqrt(2)], dtype=np.complex128)
        
        N = EntanglementMetrics.negativity(state, 0, 1, 2)
        
        assert N > 0.4  # Bell state should have high negativity


class TestEntanglementSpectrum:
    """Test entanglement spectrum calculation."""
    
    def test_spectrum_normalization(self):
        """Test that spectrum eigenvalues sum to 1."""
        # Random state
        state = np.random.randn(16) + 1j * np.random.randn(16)
        state = state / np.linalg.norm(state)
        
        spectrum = EntanglementMetrics.entanglement_spectrum(state, 4)
        
        # Each qubit's reduced density matrix eigenvalues should sum to 1
        for eigenvalues in spectrum:
            assert abs(np.sum(eigenvalues) - 1.0) < 1e-6
    
    def test_spectrum_positive_eigenvalues(self):
        """Test that all eigenvalues are non-negative."""
        state = np.random.randn(8) + 1j * np.random.randn(8)
        state = state / np.linalg.norm(state)
        
        spectrum = EntanglementMetrics.entanglement_spectrum(state, 3)
        
        for eigenvalues in spectrum:
            assert np.all(eigenvalues >= -1e-10)


class TestComputeAllMetrics:
    """Test compute_all_metrics function."""
    
    def test_all_metrics_returned(self):
        """Test that all metrics are computed."""
        # Bell state on 4 qubits
        state = np.zeros(16, dtype=np.complex128)
        state[0] = 1/np.sqrt(2)
        state[15] = 1/np.sqrt(2)
        
        metrics = EntanglementMetrics.compute_all_metrics(state, 4)
        
        # Check all keys present
        assert "mutual_information" in metrics
        assert "concurrence" in metrics
        assert "tangle" in metrics
        assert "negativity" in metrics
        assert "three_tangle" in metrics
        assert "spectrum" in metrics
    
    def test_pairwise_metrics_computed(self):
        """Test that pairwise metrics are computed for all pairs."""
        state = np.zeros(16, dtype=np.complex128)
        state[0] = 1.0
        
        metrics = EntanglementMetrics.compute_all_metrics(state, 4)
        
        # Should have metrics for all pairs: (0,1), (0,2), (0,3), (1,2), (1,3), (2,3)
        expected_pairs = 6  # C(4,2) = 6
        assert len(metrics["mutual_information"]) == expected_pairs
        assert len(metrics["concurrence"]) == expected_pairs


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
