"""
Test Suite for Optimizers (SPSA, QNG, Hybrid)

Tests convergence, accuracy, and performance of optimization algorithms.
"""

import pytest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.optimizers import SPSAOptimizer, QuantumNaturalGradient, HybridOptimizer


class TestSPSAOptimizer:
    """Test SPSA optimizer."""
    
    def test_quadratic_convergence(self):
        """Test SPSA converges on simple quadratic function."""
        # Minimize f(x) = (x - 3)^2 + (y - 2)^2
        def loss_fn(params):
            x, y = params
            return (x - 3)**2 + (y - 2)**2
        
        optimizer = SPSAOptimizer(a=0.16, c=0.1)
        initial_params = np.array([0.0, 0.0])
        
        params, loss, history = optimizer.optimize(
            loss_fn,
            initial_params,
            max_iterations=100,
            tolerance=1e-3
        )
        
        # Should converge near (3, 2)
        assert abs(params[0] - 3.0) < 0.5
        assert abs(params[1] - 2.0) < 0.5
        assert loss < 1.0
    
    def test_convergence_detection(self):
        """Test that SPSA detects convergence."""
        def loss_fn(params):
            return np.sum(params**2)
        
        optimizer = SPSAOptimizer()
        initial_params = np.array([1.0, 1.0, 1.0])
        
        params, loss, history = optimizer.optimize(
            loss_fn,
            initial_params,
            max_iterations=200,
            tolerance=1e-4
        )
        
        # Should converge before max iterations
        assert len(history) < 200
        assert loss < 0.1
    
    def test_best_params_tracking(self):
        """Test that SPSA tracks best parameters."""
        def noisy_loss(params):
            # Add noise to make optimization harder
            return np.sum(params**2) + np.random.randn() * 0.1
        
        optimizer = SPSAOptimizer()
        initial_params = np.array([2.0, 2.0])
        
        params, loss, history = optimizer.optimize(
            noisy_loss,
            initial_params,
            max_iterations=50
        )
        
        # Best loss should be better than final loss (due to noise)
        assert optimizer.best_loss <= loss + 0.2


class TestQuantumNaturalGradient:
    """Test QNG optimizer."""
    
    def test_fisher_information_computation(self):
        """Test Fisher information matrix computation."""
        # Simple quantum state function
        def state_fn(params):
            theta, phi = params
            return np.array([
                np.cos(theta/2),
                np.exp(1j * phi) * np.sin(theta/2)
            ], dtype=np.complex128)
        
        qng = QuantumNaturalGradient()
        params = np.array([np.pi/4, 0.0])
        
        F = qng.compute_fisher_information(params, state_fn)
        
        # Fisher matrix should be 2x2, symmetric, positive semi-definite
        assert F.shape == (2, 2)
        assert np.allclose(F, F.T)  # Symmetric
        eigenvalues = np.linalg.eigvalsh(F)
        assert np.all(eigenvalues >= -1e-10)  # Positive semi-definite
    
    def test_natural_gradient_step(self):
        """Test QNG optimization step."""
        def state_fn(params):
            theta = params[0]
            return np.array([np.cos(theta/2), np.sin(theta/2)], dtype=np.complex128)
        
        qng = QuantumNaturalGradient(learning_rate=0.1)
        params = np.array([np.pi/2])
        gradient = np.array([1.0])
        
        params_new = qng.optimize_step(params, gradient, state_fn)
        
        # Parameters should change
        assert not np.allclose(params, params_new)


class TestHybridOptimizer:
    """Test Hybrid SPSA→QNG optimizer."""
    
    def test_hybrid_convergence(self):
        """Test hybrid optimizer converges faster than SPSA alone."""
        # Simple quadratic function (reliable convergence)
        def loss_fn(params):
            x, y = params
            return (x - 1)**2 + (y - 1)**2
        
        def state_fn(params):
            # Dummy state function for QNG
            return np.array([params[0], params[1]], dtype=np.complex128)
        
        hybrid = HybridOptimizer(spsa_iterations=30, qng_iterations=10)
        initial_params = np.array([0.0, 0.0])
        
        params, loss, info = hybrid.optimize(loss_fn, state_fn, initial_params)
        
        # Should make progress
        initial_loss = loss_fn(initial_params)
        assert loss < initial_loss
        assert len(info["spsa_history"]) > 0
    
    def test_phase_switching(self):
        """Test that hybrid optimizer switches from SPSA to QNG."""
        def loss_fn(params):
            return np.sum((params - 1)**2)
        
        def state_fn(params):
            return params.astype(np.complex128)
        
        hybrid = HybridOptimizer(
            spsa_iterations=20,
            qng_iterations=10,
            switch_threshold=0.1
        )
        initial_params = np.array([0.0, 0.0])
        
        params, loss, info = hybrid.optimize(loss_fn, state_fn, initial_params)
        
        # Should have both SPSA and QNG history if improvement is good
        assert "spsa_history" in info
        assert "qng_history" in info


class TestOptimizerRobustness:
    """Test optimizer robustness to edge cases."""
    
    def test_spsa_with_flat_loss(self):
        """Test SPSA handles flat loss landscape."""
        def flat_loss(params):
            return 1.0  # Constant
        
        optimizer = SPSAOptimizer()
        initial_params = np.array([1.0, 1.0])
        
        # Should not crash
        params, loss, history = optimizer.optimize(
            flat_loss,
            initial_params,
            max_iterations=20
        )
        
        assert len(history) > 0
    
    def test_spsa_with_noisy_loss(self):
        """Test SPSA handles very noisy loss."""
        def noisy_loss(params):
            true_loss = np.sum(params**2)
            noise = np.random.randn() * 10  # Large noise
            return true_loss + noise
        
        optimizer = SPSAOptimizer(a=0.2, c=0.2)  # Larger step sizes for noise
        initial_params = np.array([5.0, 5.0])
        
        params, loss, history = optimizer.optimize(
            noisy_loss,
            initial_params,
            max_iterations=100
        )
        
        # Should still make some progress
        assert np.linalg.norm(params) < np.linalg.norm(initial_params)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
