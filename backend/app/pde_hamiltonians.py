"""
PDE-Inspired Hamiltonians for Emotional Evolution

Implements time-dependent Hamiltonians inspired by partial differential equations
for modeling emotional state dynamics.
"""

import numpy as np
from typing import Callable, Tuple
import math


class PDEHamiltonian:
    """
    PDE-inspired Hamiltonians for quantum emotional evolution.
    
    Models emotional dynamics using concepts from:
    - Heat equation (emotional diffusion/regulation)
    - Wave equation (emotional oscillations)
    - Schrödinger equation (quantum coherence)
    """
    
    def __init__(self, n_qubits: int = 4):
        """
        Initialize PDE Hamiltonian.
        
        Args:
            n_qubits: Number of qubits in the system
        """
        self.n_qubits = n_qubits
        self.time = 0.0
    
    def heat_diffusion_hamiltonian(
        self,
        t: float,
        diffusion_rate: float = 1.0,
        emotional_gradient: float = 0.5
    ) -> Tuple[float, float, float]:
        """
        Heat equation-inspired Hamiltonian for emotional regulation.
        
        ∂ψ/∂t = D∇²ψ
        
        Models how emotions "diffuse" and regulate over time.
        High anxiety → faster diffusion (seeking equilibrium)
        
        Args:
            t: Current time
            diffusion_rate: Rate of emotional diffusion
            emotional_gradient: Spatial gradient of emotion
            
        Returns:
            (h_longitudinal, h_transverse, j_coupling)
        """
        # Diffusion creates damping in longitudinal field
        h_long = 1.0 * np.exp(-diffusion_rate * t)
        
        # Transverse field drives toward equilibrium
        h_trans = diffusion_rate * emotional_gradient
        
        # Coupling decreases as system equilibrates
        j_coupling = 0.5 * np.exp(-0.5 * diffusion_rate * t)
        
        return h_long, h_trans, j_coupling
    
    def wave_oscillation_hamiltonian(
        self,
        t: float,
        frequency: float = 1.0,
        amplitude: float = 1.0,
        phase: float = 0.0
    ) -> Tuple[float, float, float]:
        """
        Wave equation-inspired Hamiltonian for emotional oscillations.
        
        ∂²ψ/∂t² = c²∇²ψ
        
        Models periodic emotional states (mood cycles, arousal rhythms).
        
        Args:
            t: Current time
            frequency: Oscillation frequency (mood cycle rate)
            amplitude: Oscillation amplitude (emotional intensity)
            phase: Phase offset
            
        Returns:
            (h_longitudinal, h_transverse, j_coupling)
        """
        # Oscillating fields
        omega = 2 * np.pi * frequency
        
        h_long = amplitude * np.cos(omega * t + phase)
        h_trans = amplitude * np.sin(omega * t + phase)
        
        # Coupling oscillates with different frequency (harmonic)
        j_coupling = 0.5 * amplitude * np.cos(2 * omega * t)
        
        return h_long, h_trans, j_coupling
    
    def schrodinger_coherent_hamiltonian(
        self,
        t: float,
        energy_level: float = 1.0,
        coherence_time: float = 10.0
    ) -> Tuple[float, float, float]:
        """
        Schrödinger-inspired Hamiltonian for quantum coherence.
        
        iℏ∂ψ/∂t = Ĥψ
        
        Models coherent emotional states with decoherence.
        
        Args:
            t: Current time
            energy_level: Base energy level
            coherence_time: Decoherence timescale
            
        Returns:
            (h_longitudinal, h_transverse, j_coupling)
        """
        # Coherent evolution with decoherence
        decoherence_factor = np.exp(-t / coherence_time)
        
        h_long = energy_level * decoherence_factor
        h_trans = energy_level * 0.5 * decoherence_factor
        j_coupling = 1.0 * decoherence_factor
        
        return h_long, h_trans, j_coupling
    
    def reaction_diffusion_hamiltonian(
        self,
        t: float,
        reaction_rate: float = 1.0,
        diffusion_rate: float = 0.5,
        stimulus: float = 0.0
    ) -> Tuple[float, float, float]:
        """
        Reaction-diffusion equation-inspired Hamiltonian.
        
        ∂u/∂t = D∇²u + R(u)
        
        Models emotional reactions to stimuli with spatial spread.
        Used for modeling emotional contagion, empathy.
        
        Args:
            t: Current time
            reaction_rate: Rate of emotional reaction
            diffusion_rate: Rate of emotional spread
            stimulus: External emotional stimulus
            
        Returns:
            (h_longitudinal, h_transverse, j_coupling)
        """
        # Reaction term (local response to stimulus)
        reaction = reaction_rate * stimulus * (1 - np.tanh(t))
        
        # Diffusion term (spreading to neighbors)
        diffusion = diffusion_rate * np.exp(-0.1 * t)
        
        h_long = 1.0 + reaction
        h_trans = diffusion
        j_coupling = diffusion * 2.0  # Strong coupling for spreading
        
        return h_long, h_trans, j_coupling
    
    def adaptive_hamiltonian(
        self,
        t: float,
        emotional_state: str = "calm",
        needs: dict = None
    ) -> Tuple[float, float, float]:
        """
        Adaptive Hamiltonian that switches between PDE models based on emotional state.
        
        Args:
            t: Current time
            emotional_state: Current emotional state
            needs: Dictionary of emotional needs
            
        Returns:
            (h_longitudinal, h_transverse, j_coupling)
        """
        needs = needs or {"comfort": 50, "stimulation": 50, "connection": 50}
        
        # Choose PDE model based on emotional state
        if emotional_state in ["anxious", "stressed", "overwhelmed"]:
            # Use heat diffusion for regulation
            diffusion_rate = 1.0 + (100 - needs["comfort"]) / 100
            return self.heat_diffusion_hamiltonian(t, diffusion_rate)
        
        elif emotional_state in ["excited", "joyful", "energetic"]:
            # Use wave oscillation for dynamic states
            frequency = 0.5 + needs["stimulation"] / 200
            amplitude = 1.0 + needs["stimulation"] / 100
            return self.wave_oscillation_hamiltonian(t, frequency, amplitude)
        
        elif emotional_state in ["lonely", "disconnected"]:
            # Use reaction-diffusion for seeking connection
            stimulus = (100 - needs["connection"]) / 100
            return self.reaction_diffusion_hamiltonian(t, stimulus=stimulus)
        
        else:  # calm, neutral, content
            # Use coherent Schrödinger for stable states
            coherence_time = 10.0 + needs["comfort"] / 10
            return self.schrodinger_coherent_hamiltonian(t, coherence_time=coherence_time)
    
    def time_dependent_evolution(
        self,
        apply_gate_fn: Callable,
        duration: float = 1.0,
        dt: float = 0.1,
        hamiltonian_type: str = "adaptive",
        **kwargs
    ) -> list:
        """
        Evolve quantum state using time-dependent Hamiltonian.
        
        Args:
            apply_gate_fn: Function to apply quantum gates
            duration: Total evolution time
            dt: Time step
            hamiltonian_type: Type of Hamiltonian to use
            **kwargs: Additional parameters for Hamiltonian
            
        Returns:
            List of (time, h_long, h_trans, j_coupling) tuples
        """
        evolution_history = []
        steps = int(duration / dt)
        
        for step in range(steps):
            t = step * dt
            
            # Get Hamiltonian parameters
            if hamiltonian_type == "heat":
                h_long, h_trans, j_coupling = self.heat_diffusion_hamiltonian(t, **kwargs)
            elif hamiltonian_type == "wave":
                h_long, h_trans, j_coupling = self.wave_oscillation_hamiltonian(t, **kwargs)
            elif hamiltonian_type == "schrodinger":
                h_long, h_trans, j_coupling = self.schrodinger_coherent_hamiltonian(t, **kwargs)
            elif hamiltonian_type == "reaction_diffusion":
                h_long, h_trans, j_coupling = self.reaction_diffusion_hamiltonian(t, **kwargs)
            else:  # adaptive
                h_long, h_trans, j_coupling = self.adaptive_hamiltonian(t, **kwargs)
            
            # Apply evolution for this time step
            for q in range(self.n_qubits):
                apply_gate_fn("RZ", q, h_long * dt)
                apply_gate_fn("RX", q, h_trans * dt)
                
                if j_coupling > 0.1 and q < self.n_qubits - 1:
                    # Apply coupling (simplified as rotation)
                    apply_gate_fn("RY", q, j_coupling * dt * 0.1)
            
            evolution_history.append((t, h_long, h_trans, j_coupling))
        
        return evolution_history


class EmotionalDynamics:
    """
    High-level emotional dynamics using PDE Hamiltonians.
    """
    
    @staticmethod
    def emotional_relaxation(
        apply_gate_fn: Callable,
        anxiety_level: float,
        n_qubits: int = 4,
        duration: float = 2.0
    ) -> dict:
        """
        Model emotional relaxation using heat diffusion.
        
        Args:
            apply_gate_fn: Gate application function
            anxiety_level: Current anxiety (0-1)
            n_qubits: Number of qubits
            duration: Relaxation duration
            
        Returns:
            Evolution statistics
        """
        pde = PDEHamiltonian(n_qubits)
        
        history = pde.time_dependent_evolution(
            apply_gate_fn,
            duration=duration,
            hamiltonian_type="heat",
            diffusion_rate=1.0 + anxiety_level,
            emotional_gradient=anxiety_level
        )
        
        return {
            "type": "relaxation",
            "duration": duration,
            "steps": len(history),
            "final_coupling": history[-1][3] if history else 0.0
        }
    
    @staticmethod
    def emotional_oscillation(
        apply_gate_fn: Callable,
        mood_frequency: float,
        n_qubits: int = 4,
        duration: float = 5.0
    ) -> dict:
        """
        Model emotional oscillations (mood cycles).
        
        Args:
            apply_gate_fn: Gate application function
            mood_frequency: Frequency of mood cycles
            n_qubits: Number of qubits
            duration: Observation duration
            
        Returns:
            Evolution statistics
        """
        pde = PDEHamiltonian(n_qubits)
        
        history = pde.time_dependent_evolution(
            apply_gate_fn,
            duration=duration,
            hamiltonian_type="wave",
            frequency=mood_frequency,
            amplitude=1.0
        )
        
        return {
            "type": "oscillation",
            "frequency": mood_frequency,
            "duration": duration,
            "steps": len(history)
        }
