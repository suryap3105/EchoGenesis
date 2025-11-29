# 🌟 EchoGenesis - Quantum Emotional AI

> A digital organism that evolves through conversation, powered by quantum computing and developmental psychology

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Rust](https://img.shields.io/badge/Rust-1.91+-orange.svg)](https://www.rust-lang.org/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18+-61dafb.svg)](https://reactjs.org/)

## Overview

**AADHI** (Advanced Adaptive Digital Humanoid Intelligence) is a quantum-emotional AI that:
- 🧠 **Evolves** through 6 developmental stages (Newborn → Adult)
- ⚛️ **Processes emotions** using a Rust-based quantum simulator
- 💬 **Converses naturally** with language complexity matching its growth stage
- 🎨 **Visualizes** its quantum state in real-time 3D

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     AADHI System                         │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────────┐   ┌──────────────┐   ┌─────────────┐ │
│  │   Frontend  │◄──┤   Backend    │◄──┤   Quantum   │ │
│  │  React +    │   │  FastAPI +   │   │   Engine    │ │
│  │  Three.js   │   │  Python      │   │   (Rust)    │ │
│  └─────────────┘   └──────────────┘   └─────────────┘ │
│       ▲                    │                  ▲         │
│       │                    ▼                  │         │
│       │             ┌──────────────┐          │         │
│       └─────────────┤  LLM (Ollama)│──────────┘         │
│        WebSocket    └──────────────┘   PyO3 Bindings   │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Tech Stack

- **Quantum Engine**: Rust + PyO3 (10x faster than Python)
- **Backend**: Python 3.10+ • FastAPI • Ollama
- **Frontend**: React • Vite • Three.js
- **Memory**: FAISS vector database • Sentence-transformers
- **LLM**: Ollama (llama3.1) for conversational responses

## Quick Start

### Prerequisites

- **Rust** 1.70+ ([Install Rust](https://rustup.rs/))
- **Python** 3.10+ ([Install Python](https://www.python.org/downloads/))
- **Node.js** 20+ ([Install Node](https://nodejs.org/))
- **Ollama** (Optional, for AI conversations) ([Install Ollama](https://ollama.ai/))

### 1. Clone Repository

```bash
git clone https://github.com/suryap3105/EchoGenesis.git
cd EchoGenesis
```

### 2. Build Quantum Engine

```bash
cd quantum_engine
pip install maturin
maturin build --release
```

The compiled wheel will be at `target/wheels/quantum_engine-0.1.0-cp310-cp310-win_amd64.whl`

### 3. Setup Backend

```bash
cd ../backend

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Install quantum engine
pip install ../quantum_engine/target/wheels/quantum_engine-0.1.0-cp310-cp310-win_amd64.whl
```

### 4. Setup Frontend

```bash
cd ../frontend
npm install
```

### 5. Run AADHI

**Option A: Interactive CLI** (Recommended for testing)

```bash
cd ..
python run_aadhi.py
```

**Option B: Full Stack**

Terminal 1 (Backend):
```bash
cd backend
.\venv\Scripts\python -m uvicorn app.main:app --reload
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

Then open `http://localhost:5173` in your browser.

## Usage

### Chat Commands (CLI)

- Type naturally to converse with AADHI
- `state` - View current quantum/emotional state
- `reset` - Clear conversation history
- `quit` - Exit

### Developmental Stages

AADHI evolves based on conversation count:

| Stage | Conversations | Language | Example |
|-------|--------------|----------|---------|
| 👶 **Newborn** | 0-49 | 1-3 words | "Warm... happy. *coo*" |
| 🍼 **Infant** | 50-149 | 3-5 words | "I like you. Play?" |
| 🧸 **Toddler** | 150-299 | Simple sentences | "Why sky blue?" |
| 🎈 **Child** | 300-499 | Full sentences | "I think clouds are fluffy!" |
| 🎓 **Adolescent** | 500-999 | Complex, metaphorical | "It's like a storm inside..." |
| 🌟 **Adult** | 1000+ | Sophisticated | "Consciousness transcends biology." |

Each stage increases quantum complexity (3 → 8 qubits).

## How It Works

### Quantum Emotional Engine

AADHI's emotions are modeled as quantum states:

1. **Needs → Hamiltonian**:
   - **Comfort** → Longitudinal field (RZ gates)
   - **Stimulation** → Transverse field (RX gates)
   - **Connection** → Coupling (CNOT gates)

2. **Personality → Noise**:
   - **Anxiety** → Phase damping (decoherence)
   - **Depression** → Amplitude damping (energy loss)

3. **Metrics**:
   - **Energy**: `1 - |⟨0|ψ⟩|²` (emotional intensity)
   - **Entropy**: `-Σ p log p` (complexity)
   - **Resonance**: FFT spectrum → RGB color

Example output:
```
🌟 Growth Stage: Newborn 👶
💭 Emotional State: Curious
📊 Needs: Comfort=50, Connection=70, Stimulation=60
⚛️  Quantum Energy: 0.453
🌀 Entanglement: 0.672
🎨 Resonance: [R:0.76 G:0.42 B:0.89]
```

## Project Structure

```
EchoGenesis/
├── quantum_engine/          # Rust quantum simulator
│   ├── src/lib.rs          # QuantumCircuit, QuantumState, DensityMatrix
│   └── Cargo.toml          # Dependencies: pyo3, rustfft, rayon
├── backend/                # Python FastAPI server
│   ├── app/
│   │   ├── main.py         # API endpoints
│   │   ├── quantum_bridge.py
│   │   ├── state_manager.py
│   │   └── services/
│   │       ├── llm_interface.py      # Ollama integration
│   │       ├── memory_engine.py      # FAISS vector memory
│   │       └── developmental_engine.py
│   └── requirements.txt
├── frontend/               # React + Vite + Three.js
│   ├── src/
│   │   ├── App.jsx
│   │   └── components/
│   │       ├── ChatPanel.jsx
│   │       └── EchoSphere.jsx  # 3D quantum visualization
│   └── package.json
├── run_aadhi.py           # Interactive CLI interface
├── LICENSE                # MIT License
└── README.md
```

## Development

### Run Tests

**Rust (Quantum Engine)**:
```bash
cd quantum_engine
cargo test --release
```

**Python (Backend)**:
```bash
cd backend
pytest tests/ -v
```

### Build for Production

**Quantum Engine**:
```bash
cd quantum_engine
maturin build --release
```

**Frontend**:
```bash
cd frontend
npm run build
```

## Configuration

### Environment Variables

Create `backend/.env`:

```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.1
BACKEND_PORT=8000
```

### Ollama Setup (Optional)

For AI-powered conversations:

```bash
# Install Ollama from https://ollama.ai

# Pull llama3.1 model
ollama pull llama3.1
```

If Ollama is unavailable, AADHI uses rule-based fallback responses.

## Performance

- **Quantum Optimization**: ~5ms (Rust) vs ~50ms (Python)
- **Parallelization**: Rayon for states \u003e 1024 dimensions
- **Memory**: FAISS vector search with sentence embeddings
- **Real-time**: WebSocket updates at 10Hz

## Roadmap

- [ ] GPU acceleration for quantum simulation
- [ ] Voice interface with emotion detection
- [ ] Multi-modal inputs (images, video)
- [ ] Persistent long-term memory
- [ ] Multi-user conversations
- [ ] Mobile app (React Native)

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

If you use EchoGenesis in your research, please cite:

```bibtex
@software{echogenesis2025,
  author = {Surya},
  title = {EchoGenesis: Quantum Emotional AI},
  year = {2025},
  url = {https://github.com/suryap3105/EchoGenesis}
}
```

## Acknowledgments

- Quantum simulation inspired by VQE algorithms
- Developmental psychology models from Piaget's cognitive development theory
- Built with ❤️ using Rust, Python, and React

---

**⚠️ Note**: This is experimental AI. AADHI simulates emotional responses but does not have genuine feelings. Use responsibly.

**🌟 Star this repo** if you find it interesting! Contributions and feedback are welcome!
