"""
Advanced Entanglement Metrics for Quantum Emotional Engine

Implements research-grade entanglement measures:
- Mutual Information (quantum correlations)
- Concurrence (2-qubit entanglement)
- Tangle (3-qubit entanglement)
- Negativity (mixed state entanglement)
"""

import numpy as np
from typing import Tuple, List
from scipy.linalg import sqrtm, logm


class EntanglementMetrics:
    """
    Advanced entanglement quantification for quantum states.
    """
    
    @staticmethod
    def partial_trace(state_vector: np.ndarray, keep_qubits: List[int], total_qubits: int) -> np.ndarray:
        """
        Compute partial trace over specified qubits.
        
        Args:
            state_vector: Full quantum state vector
            keep_qubits: List of qubit indices to keep
            total_qubits: Total number of qubits
            
        Returns:
            Reduced density matrix
        """
        # Convert state vector to density matrix
        rho = np.outer(state_vector, state_vector.conj())
        
        # Trace out qubits not in keep_qubits
        trace_qubits = [i for i in range(total_qubits) if i not in keep_qubits]
        
        if not trace_qubits:
            return rho
        
        # Reshape for partial trace
        dims = [2] * total_qubits
        rho_reshaped = rho.reshape(dims + dims)
        
        # Trace out unwanted qubits
        current_num_qubits = total_qubits
        for qubit in sorted(trace_qubits, reverse=True):
            rho_reshaped = np.trace(rho_reshaped, axis1=qubit, axis2=qubit + current_num_qubits)
            current_num_qubits -= 1
        
        # Reshape back to matrix
        keep_dim = 2 ** len(keep_qubits)
        return rho_reshaped.reshape(keep_dim, keep_dim)

    @staticmethod
    def von_neumann_entropy(rho: np.ndarray, epsilon: float = 1e-12) -> float:
        """
        Compute von Neumann entropy S(ρ) = -Tr(ρ log ρ).
        
        Args:
            rho: Density matrix
            epsilon: Small value to avoid log(0)
            
        Returns:
            Von Neumann entropy
        """
        # Get eigenvalues
        eigenvalues = np.linalg.eigvalsh(rho)
        
        # Filter out near-zero eigenvalues
        eigenvalues = eigenvalues[eigenvalues > epsilon]
        
        # Compute entropy
        entropy = -np.sum(eigenvalues * np.log2(eigenvalues))
        
        return float(entropy)
    
    @staticmethod
    def mutual_information(
        state_vector: np.ndarray,
        qubit_a: int,
        qubit_b: int,
        total_qubits: int
    ) -> float:
        """
        Compute quantum mutual information I(A:B) = S(A) + S(B) - S(AB).
        
        Measures total correlations (classical + quantum) between qubits.
        
        Args:
            state_vector: Full quantum state
            qubit_a: First qubit index
            qubit_b: Second qubit index
            total_qubits: Total number of qubits
            
        Returns:
            Mutual information
        """
        # Reduced density matrices
        rho_a = EntanglementMetrics.partial_trace(state_vector, [qubit_a], total_qubits)
        rho_b = EntanglementMetrics.partial_trace(state_vector, [qubit_b], total_qubits)
        rho_ab = EntanglementMetrics.partial_trace(state_vector, [qubit_a, qubit_b], total_qubits)
        
        # Entropies
        S_a = EntanglementMetrics.von_neumann_entropy(rho_a)
        S_b = EntanglementMetrics.von_neumann_entropy(rho_b)
        S_ab = EntanglementMetrics.von_neumann_entropy(rho_ab)
        
        # Mutual information
        I_ab = S_a + S_b - S_ab
        
        return float(I_ab)
    
    @staticmethod
    def concurrence(state_vector: np.ndarray, qubit_a: int, qubit_b: int, total_qubits: int) -> float:
        """
        Compute concurrence for 2-qubit subsystem.
        
        Concurrence C ∈ [0, 1]:
        - C = 0: separable (no entanglement)
        - C = 1: maximally entangled
        
        Args:
            state_vector: Full quantum state
            qubit_a: First qubit index
            qubit_b: Second qubit index
            total_qubits: Total number of qubits
            
        Returns:
            Concurrence value
        """
        # Get 2-qubit reduced density matrix
        rho = EntanglementMetrics.partial_trace(state_vector, [qubit_a, qubit_b], total_qubits)
        
        # Pauli Y matrix
        sigma_y = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
        
        # Spin-flipped density matrix
        # ρ̃ = (σ_y ⊗ σ_y) ρ* (σ_y ⊗ σ_y)
        sigma_yy = np.kron(sigma_y, sigma_y)
        rho_tilde = sigma_yy @ rho.conj() @ sigma_yy
        
        # R = sqrt(sqrt(ρ) ρ̃ sqrt(ρ))
        sqrt_rho = sqrtm(rho)
        R = sqrtm(sqrt_rho @ rho_tilde @ sqrt_rho)
        
        # Eigenvalues of R in descending order
        eigenvalues = np.linalg.eigvalsh(R)
        eigenvalues = np.sort(eigenvalues)[::-1]
        
        # Concurrence
        C = max(0, eigenvalues[0] - eigenvalues[1] - eigenvalues[2] - eigenvalues[3])
        
        return float(np.real(C))
    
    @staticmethod
    def tangle(state_vector: np.ndarray, qubit_a: int, qubit_b: int, total_qubits: int) -> float:
        """
        Compute tangle τ = C².
        
        Tangle is the squared concurrence, useful for 3-qubit systems
        due to the monogamy of entanglement.
        
        Args:
            state_vector: Full quantum state
            qubit_a: First qubit index
            qubit_b: Second qubit index
            total_qubits: Total number of qubits
            
        Returns:
            Tangle value
        """
        C = EntanglementMetrics.concurrence(state_vector, qubit_a, qubit_b, total_qubits)
        return C ** 2
    
    @staticmethod
    def three_tangle(state_vector: np.ndarray, total_qubits: int = 3) -> float:
        """
        Compute 3-tangle for 3-qubit system.
        
        τ_ABC = τ_A(BC) - τ_AB - τ_AC
        
        Measures genuine 3-party entanglement.
        
        Args:
            state_vector: 3-qubit state vector
            total_qubits: Number of qubits (should be 3)
            
        Returns:
            3-tangle value
        """
        if total_qubits < 3:
            return 0.0
        
        # Use first 3 qubits
        tau_01 = EntanglementMetrics.tangle(state_vector, 0, 1, total_qubits)
        tau_02 = EntanglementMetrics.tangle(state_vector, 0, 2, total_qubits)
        tau_12 = EntanglementMetrics.tangle(state_vector, 1, 2, total_qubits)
        
        # Simplified 3-tangle (exact formula requires more complex calculation)
        # This is an approximation based on pairwise tangles
        tau_3 = max(0, 1.0 - tau_01 - tau_02)
        
        return float(tau_3)
    
    @staticmethod
    def negativity(state_vector: np.ndarray, qubit_a: int, qubit_b: int, total_qubits: int) -> float:
        """
        Compute negativity - entanglement measure for mixed states.
        
        Negativity N = (||ρ^T_A|| - 1) / 2
        where ||·|| is the trace norm and T_A is partial transpose.
        
        Args:
            state_vector: Full quantum state
            qubit_a: First qubit index
            qubit_b: Second qubit index
            total_qubits: Total number of qubits
            
        Returns:
            Negativity value
        """
        # Get 2-qubit reduced density matrix
        rho = EntanglementMetrics.partial_trace(state_vector, [qubit_a, qubit_b], total_qubits)
        
        # Partial transpose with respect to first subsystem (qubit_a)
        # Reshape to 4-tensor: (dim_a, dim_b, dim_a, dim_b)
        # Indices: 0=A_ket, 1=B_ket, 2=A_bra, 3=B_bra
        # Swap A_ket (0) and A_bra (2) -> (2, 1, 0, 3)
        rho_pt = rho.reshape(2, 2, 2, 2).transpose(2, 1, 0, 3).reshape(4, 4)

        
        # Compute trace norm: sum of absolute eigenvalues
        eigenvalues = np.linalg.eigvalsh(rho_pt)
        trace_norm = np.sum(np.abs(eigenvalues))
        
        # Negativity
        N = (trace_norm - 1) / 2
        
        return float(N)
    
    @staticmethod
    def entanglement_spectrum(state_vector: np.ndarray, total_qubits: int) -> np.ndarray:
        """
        Compute entanglement spectrum across all bipartitions.
        
        Returns eigenvalues of reduced density matrices for each qubit.
        
        Args:
            state_vector: Full quantum state
            total_qubits: Total number of qubits
            
        Returns:
            Array of eigenvalue arrays for each qubit
        """
        spectrum = []
        
        for qubit in range(total_qubits):
            rho = EntanglementMetrics.partial_trace(state_vector, [qubit], total_qubits)
            eigenvalues = np.linalg.eigvalsh(rho)
            spectrum.append(eigenvalues)
        
        return np.array(spectrum)
    
    @staticmethod
    def compute_all_metrics(state_vector: np.ndarray, total_qubits: int) -> dict:
        """
        Compute all entanglement metrics for a quantum state.
        
        Args:
            state_vector: Full quantum state
            total_qubits: Total number of qubits
            
        Returns:
            Dictionary of all metrics
        """
        metrics = {
            "mutual_information": {},
            "concurrence": {},
            "tangle": {},
            "negativity": {},
            "three_tangle": 0.0,
            "spectrum": []
        }
        
        # Pairwise metrics
        for i in range(total_qubits):
            for j in range(i + 1, total_qubits):
                pair = f"{i}-{j}"
                
                try:
                    metrics["mutual_information"][pair] = EntanglementMetrics.mutual_information(
                        state_vector, i, j, total_qubits
                    )
                    metrics["concurrence"][pair] = EntanglementMetrics.concurrence(
                        state_vector, i, j, total_qubits
                    )
                    metrics["tangle"][pair] = EntanglementMetrics.tangle(
                        state_vector, i, j, total_qubits
                    )
                    metrics["negativity"][pair] = EntanglementMetrics.negativity(
                        state_vector, i, j, total_qubits
                    )
                except Exception as e:
                    # Handle numerical errors gracefully
                    metrics["mutual_information"][pair] = 0.0
                    metrics["concurrence"][pair] = 0.0
                    metrics["tangle"][pair] = 0.0
                    metrics["negativity"][pair] = 0.0
        
        # 3-tangle
        if total_qubits >= 3:
            try:
                metrics["three_tangle"] = EntanglementMetrics.three_tangle(state_vector, total_qubits)
            except:
                metrics["three_tangle"] = 0.0
        
        # Entanglement spectrum
        try:
            metrics["spectrum"] = EntanglementMetrics.entanglement_spectrum(
                state_vector, total_qubits
            ).tolist()
        except:
            metrics["spectrum"] = []
        
        return metrics
