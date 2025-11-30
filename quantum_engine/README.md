# Quantum Emotional Engine ⚛️ 🧠

Rust implementation of the **Biomimetic Quantum-Inspired Emotional Simulator** for EchoGenesis.

## Overview

This module implements a high-performance quantum statevector simulator designed to model **neuro-affective dynamics**. It is a **computational simulation** inspired by Quantum Cognition theory (Pothos, Busemeyer) and biological neural architecture, not a claim of quantum biological processes in the human brain.

It maps quantum circuit topology to specific brain regions (Amygdala, PFC) to simulate the non-linear, interference-prone nature of human emotion.

## Features

- **Biomimetic Topology** - Qubits mapped to specific brain regions (Amygdala, PFC, Hippocampus)
- **Top-Down Regulation** - PFC qubits control Amygdala qubits via Entanglement (CNOT/CRZ)
- **Homeostatic Stability** - Damping mechanisms to prevent "emotional runaway" (State Explosion)
- **Synaptic Plasticity Stub** - Parameter adaptation interface for future reinforcement learning
- **Lobotomy Mode** - Ablation switch for comparing Quantum vs. Classical baselines
- **PyO3 Bindings** - Native Python integration

## Building

### Prerequisites

- Rust 1.70+ (`rustup` recommended)
- Python 3.10+
- Cargo

### Compilation

```bash
# Build in release mode (optimized)
cargo build --release

# Run tests
cargo test

# Build with Python bindings
maturin develop --release
```

### Installation

After building, copy the compiled library to the backend:

**Windows:**
```bash
copy target\release\quantum_engine.pyd ..\backend\
```

**Linux:**
```bash
cp target/release/libquantum_engine.so ../backend/quantum_engine.so
```

**macOS:**
```bash
cp target/release/libquantum_engine.dylib ../backend/quantum_engine.so
```

## Usage

### From Python

```python
import quantum_engine

# Create quantum state (4 qubits)
state = quantum_engine.QuantumState(4)

# Apply gates
state.apply_gate("H", 0, None)  # Hadamard on qubit 0
state.apply_gate("RX", 1, 1.57)  # RX(π/2) on qubit 1

# Optimize emotional state
energy, entropy, resonance, stability = state.optimize_state(
    needs_comfort=75.0,
    needs_stimulation=50.0,
    needs_connection=60.0,
    anxiety=0.4
)

print(f"Energy: {energy}")
print(f"Entropy: {entropy}")
print(f"Resonance: {resonance}")
print(f"Stability: {stability}")
```

### From Rust

```rust
use quantum_engine::QuantumState;

let mut state = QuantumState::new(4);
state.apply_gate("H", 0, None).unwrap();

let (energy, entropy, resonance, stability) = 
    state.optimize_state(75.0, 50.0, 60.0, 0.4);
```

## Architecture

### QuantumState Struct

```rust
pub struct QuantumState {
    qubits: usize,           // Number of qubits
    state: Vec<Complex32>,   // Statevector (2^N elements)
}
```

### Key Methods

- **`new(qubits: usize)`** - Initialize to |0...0⟩
- **`apply_gate(gate: &str, target: usize, param: Option<f32>)`** - Apply single-qubit gate
- **`optimize_state(...)`** - Hamiltonian evolution + metrics
- **`measure_energy()`** - Ground state energy (distance from |0⟩)
- **`entropy()`** - Von Neumann entropy
- **`calculate_resonance()`** - FFT-based color mapping

## Quantum Gates

### Implemented Gates

| Gate | Matrix | Parameter |
|------|--------|-----------|
| H | Hadamard | None |
| X | Pauli-X (NOT) | None |
| RX | X-rotation | θ (radians) |
| RY | Y-rotation | θ (radians) |
| RZ | Z-rotation | φ (radians) |

### Gate Application

Gates are applied via tensor product expansion:

```
U_total = I ⊗ ... ⊗ U_target ⊗ ... ⊗ I
```

## Neuro-Quantum Topology

The circuit architecture mimics the **limbic-cortical loops** of the human brain:

### Qubit Mapping
| Qubit ID | Brain Region | Function | Quantum Role |
|----------|--------------|----------|--------------|
| 0 | **Amygdala (Basolateral)** | Valence (Good/Bad) | Target for sensory input (RX/RY) |
| 1 | **Amygdala (Central)** | Arousal (Intensity) | Coupled to Q0 via CNOT |
| 2 | **Prefrontal Cortex (vmPFC)** | Regulation/Inhibition | Control qubit for Amygdala (CRZ) |
| 3 | **Hippocampus** | Context/Memory | Entanglement hub for history |

### Dynamics
1.  **Bottom-Up Arousal**: Sensory inputs rotate Amygdala qubits (0, 1).
2.  **Top-Down Control**: PFC qubits (2, 3) apply controlled-rotations (CRZ) to dampen or amplify Amygdala states.
3.  **Homeostasis**: Global non-unitary evolution (damping) pulls the system back to a ground state to simulate metabolic limits.

## Emotional Hamiltonian

The system evolves under a Hamiltonian inspired by these interactions:

```
H(t) = H_limbic + H_cortical + H_regulation
```

Where:
- **H_limbic** = Σ ω_j σ_j (Raw emotional reactivity)
- **H_cortical** = Σ Ω_j σ_j (Cognitive state)
- **H_regulation** = Σ J_ij σ_i σ_j (PFC inhibiting Amygdala)

## Performance

### Benchmarks (4 qubits, 5 Trotter steps)

- **Rust**: ~5ms per optimization
- **Python**: ~50ms per optimization

**Speedup**: ~10x

### Scaling

| Qubits | State Size | Memory | Time (Rust) |
|--------|-----------|--------|-------------|
| 4 | 16 | 128 B | 5 ms |
| 6 | 64 | 512 B | 15 ms |
| 8 | 256 | 2 KB | 50 ms |

## Dependencies

```toml
[dependencies]
pyo3 = { version = "0.19.0", features = ["extension-module"] }
num-complex = "0.4"
rand = "0.8"
rustfft = "6.1"
```

## Development

### Running Tests

```bash
cargo test --release
```

### Benchmarking

```bash
cargo bench
```

### Profiling

```bash
cargo build --release
perf record --call-graph=dwarf ./target/release/quantum_engine
perf report
```

## Troubleshooting

### Compilation Errors

**Missing Rust:**
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

**PyO3 Version Mismatch:**
- Ensure Python version matches PyO3 expectations
- Check `python --version` and update `Cargo.toml` if needed

### Runtime Errors

**Import Error in Python:**
- Verify library is in Python path
- Check file extension (.pyd on Windows, .so on Linux/Mac)

**Numerical Instability:**
- Reduce Trotter steps
- Increase dt (time step)
- Check for NaN values in input parameters

## Future Optimizations

- [ ] SIMD vectorization for gate application
- [ ] GPU acceleration via CUDA/OpenCL
- [ ] Sparse matrix representation for large systems
- [ ] Quantum circuit optimization (gate fusion)
- [ ] Multi-threading for independent qubit operations

## References

- **VQE**: Peruzzo et al., "A variational eigenvalue solver on a photonic quantum processor" (2014)
- **Trotterization**: Trotter, "On the product of semi-groups of operators" (1959)
- **PyO3**: https://pyo3.rs/

## License

MIT License - see root LICENSE file
