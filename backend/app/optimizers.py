"""
SPSA (Simultaneous Perturbation Stochastic Approximation) Optimizer
for Quantum Emotional Engine

Implements gradient-free optimization for quantum state evolution.
"""

import numpy as np
from typing import Callable, Tuple, List

class SPSAOptimizer:
    """
    SPSA optimizer for quantum parameter optimization.
    
    Reference: Spall, J. C. (1998). "Implementation of the simultaneous 
    perturbation algorithm for stochastic optimization."
    """
    
    def __init__(
        self,
        a: float = 0.16,
        c: float = 0.1,
        alpha: float = 0.602,
        gamma: float = 0.101,
        A: float = 0.0
    ):
        """
        Initialize SPSA optimizer.
        
        Args:
            a: Step size scaling
            c: Perturbation size scaling
            alpha: Step size decay exponent
            gamma: Perturbation decay exponent
            A: Stability constant (typically 10% of max iterations)
        """
        self.a = a
        self.c = c
        self.alpha = alpha
        self.gamma = gamma
        self.A = A
        
        self.iteration = 0
        self.best_params = None
        self.best_loss = float('inf')
        self.loss_history = []
    
    def step_size(self, k: int) -> float:
        """Calculate step size for iteration k."""
        return self.a / ((k + 1 + self.A) ** self.alpha)
    
    def perturbation_size(self, k: int) -> float:
        """Calculate perturbation size for iteration k."""
        return self.c / ((k + 1) ** self.gamma)
    
    def optimize(
        self,
        loss_fn: Callable[[np.ndarray], float],
        initial_params: np.ndarray,
        max_iterations: int = 100,
        tolerance: float = 1e-6
    ) -> Tuple[np.ndarray, float, List[float]]:
        """
        Optimize parameters using SPSA.
        
        Args:
            loss_fn: Function that takes parameters and returns loss
            initial_params: Starting parameter values
            max_iterations: Maximum optimization iterations
            tolerance: Convergence tolerance
            
        Returns:
            (optimized_params, final_loss, loss_history)
        """
        params = initial_params.copy()
        n_params = len(params)
        
        self.loss_history = []
        self.best_params = params.copy()
        self.best_loss = loss_fn(params)
        
        for k in range(max_iterations):
            # Calculate step sizes
            ak = self.step_size(k)
            ck = self.perturbation_size(k)
            
            # Generate random perturbation direction (Bernoulli ±1)
            delta = 2 * np.random.randint(0, 2, size=n_params) - 1
            
            # Evaluate loss at perturbed points
            loss_plus = loss_fn(params + ck * delta)
            loss_minus = loss_fn(params - ck * delta)
            
            # Estimate gradient
            gradient_estimate = (loss_plus - loss_minus) / (2 * ck * delta)
            
            # Update parameters
            params = params - ak * gradient_estimate
            
            # Evaluate current loss
            current_loss = loss_fn(params)
            self.loss_history.append(current_loss)
            
            # Track best
            if current_loss < self.best_loss:
                self.best_loss = current_loss
                self.best_params = params.copy()
            
            # Check convergence
            if k > 10 and abs(self.loss_history[-1] - self.loss_history[-10]) < tolerance:
                print(f"SPSA converged at iteration {k}")
                break
        
        return self.best_params, self.best_loss, self.loss_history


class QuantumNaturalGradient:
    """
    Quantum Natural Gradient optimizer.
    
    Uses the quantum Fisher information metric for more efficient
    optimization in quantum parameter space.
    """
    
    def __init__(self, learning_rate: float = 0.01, epsilon: float = 1e-8):
        """
        Initialize QNG optimizer.
        
        Args:
            learning_rate: Learning rate for parameter updates
            epsilon: Small constant for numerical stability
        """
        self.learning_rate = learning_rate
        self.epsilon = epsilon
        self.iteration = 0
    
    def compute_fisher_information(
        self,
        params: np.ndarray,
        state_fn: Callable[[np.ndarray], np.ndarray],
        delta: float = 1e-4
    ) -> np.ndarray:
        """
        Compute quantum Fisher information matrix.
        
        Args:
            params: Current parameters
            state_fn: Function that returns quantum state for given params
            delta: Finite difference step size
            
        Returns:
            Fisher information matrix
        """
        n = len(params)
        F = np.zeros((n, n))
        
        # Get current state
        psi = state_fn(params)
        
        for i in range(n):
            # Perturb parameter i
            params_plus = params.copy()
            params_plus[i] += delta
            psi_plus = state_fn(params_plus)
            
            # Compute derivative
            dpsi_i = (psi_plus - psi) / delta
            
            for j in range(i, n):
                # Perturb parameter j
                params_plus_j = params.copy()
                params_plus_j[j] += delta
                psi_plus_j = state_fn(params_plus_j)
                
                # Compute derivative
                dpsi_j = (psi_plus_j - psi) / delta
                
                # Fisher information element
                F[i, j] = 4 * np.real(np.vdot(dpsi_i, dpsi_j) - np.vdot(dpsi_i, psi) * np.vdot(psi, dpsi_j))
                F[j, i] = F[i, j]  # Symmetric
        
        return F
    
    def optimize_step(
        self,
        params: np.ndarray,
        gradient: np.ndarray,
        state_fn: Callable[[np.ndarray], np.ndarray]
    ) -> np.ndarray:
        """
        Perform one QNG optimization step.
        
        Args:
            params: Current parameters
            gradient: Gradient of loss function
            state_fn: Function that returns quantum state
            
        Returns:
            Updated parameters
        """
        # Compute Fisher information
        F = self.compute_fisher_information(params, state_fn)
        
        # Add regularization for numerical stability
        F_reg = F + self.epsilon * np.eye(len(params))
        
        # Compute natural gradient
        try:
            F_inv = np.linalg.inv(F_reg)
            natural_gradient = F_inv @ gradient
        except np.linalg.LinAlgError:
            # Fallback to regular gradient if inversion fails
            natural_gradient = gradient
        
        # Update parameters
        params_new = params - self.learning_rate * natural_gradient
        
        self.iteration += 1
        return params_new


class HybridOptimizer:
    """
    Hybrid SPSA + QNG optimizer.
    
    Uses SPSA for initial exploration, then refines with QNG.
    """
    
    def __init__(
        self,
        spsa_iterations: int = 50,
        qng_iterations: int = 20,
        switch_threshold: float = 0.1
    ):
        """
        Initialize hybrid optimizer.
        
        Args:
            spsa_iterations: Number of SPSA iterations
            qng_iterations: Number of QNG refinement iterations
            switch_threshold: Loss improvement threshold to switch to QNG
        """
        self.spsa = SPSAOptimizer()
        self.qng = QuantumNaturalGradient()
        self.spsa_iterations = spsa_iterations
        self.qng_iterations = qng_iterations
        self.switch_threshold = switch_threshold
    
    def optimize(
        self,
        loss_fn: Callable[[np.ndarray], float],
        state_fn: Callable[[np.ndarray], np.ndarray],
        initial_params: np.ndarray
    ) -> Tuple[np.ndarray, float, dict]:
        """
        Optimize using hybrid SPSA → QNG approach.
        
        Args:
            loss_fn: Loss function
            state_fn: Quantum state function
            initial_params: Initial parameters
            
        Returns:
            (optimized_params, final_loss, info_dict)
        """
        # Phase 1: SPSA exploration
        print("[Hybrid] Phase 1: SPSA exploration")
        params, loss, spsa_history = self.spsa.optimize(
            loss_fn,
            initial_params,
            max_iterations=self.spsa_iterations
        )
        
        # Phase 2: QNG refinement (if improvement is good)
        qng_history = []
        if len(spsa_history) > 10:
            improvement = spsa_history[0] - spsa_history[-1]
            
            if improvement > self.switch_threshold:
                print("[Hybrid] Phase 2: QNG refinement")
                
                for _ in range(self.qng_iterations):
                    # Estimate gradient using finite differences
                    gradient = self._estimate_gradient(loss_fn, params)
                    
                    # QNG step
                    params = self.qng.optimize_step(params, gradient, state_fn)
                    
                    # Track loss
                    current_loss = loss_fn(params)
                    qng_history.append(current_loss)
                    
                    if current_loss < loss:
                        loss = current_loss
        
        info = {
            "spsa_history": spsa_history,
            "qng_history": qng_history,
            "total_iterations": len(spsa_history) + len(qng_history)
        }
        
        return params, loss, info
    
    def _estimate_gradient(
        self,
        loss_fn: Callable[[np.ndarray], float],
        params: np.ndarray,
        delta: float = 1e-4
    ) -> np.ndarray:
        """Estimate gradient using finite differences."""
        gradient = np.zeros_like(params)
        
        for i in range(len(params)):
            params_plus = params.copy()
            params_plus[i] += delta
            
            params_minus = params.copy()
            params_minus[i] -= delta
            
            gradient[i] = (loss_fn(params_plus) - loss_fn(params_minus)) / (2 * delta)
        
        return gradient
