# EchoGenesis Backend 🔬

FastAPI-based backend for the EchoGenesis quantum-emotional organism.

## Architecture

### Core Components

- **`main.py`** - FastAPI application with REST and WebSocket endpoints
- **`quantum_bridge.py`** - High-fidelity quantum simulator (Python) with Rust integration support
- **`state_manager.py`** - Orchestrates Echo's internal state and interaction loop
- **`emotion_analyzer.py`** - Sentiment analysis for user messages

### Services

- **`memory_engine.py`** - Hybrid memory system (FAISS + NetworkX + ColBERT)
- **`prompt_builder.py`** - Constructs context-rich LLM prompts
- **`developmental_engine.py`** - Manages growth stages and affect regulation
- **`llm_interface.py`** - Connects to external LLMs (OpenAI/Gemini)

## Installation

```bash
# Create virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

## Running

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### REST

- **GET `/`** - Health check
- **POST `/chat`** - Send message to Echo
  ```json
  {
    "message": "Hello Echo!",
    "user_id": "user123"
  }
  ```

### WebSocket

- **WS `/ws`** - Real-time state updates
  - Broadcasts Echo's state every time it changes
  - Used by frontend for live visualization

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_core.py -v

# Run quantum logic tests
pytest tests/test_rust_logic.py -v

# With coverage
pytest tests/ --cov=app --cov-report=html
```

## Configuration

### Environment Variables

Create a `.env` file:

```env
# LLM Configuration
LLM_PROVIDER=mock  # Options: mock, openai, gemini
LLM_API_KEY=your_api_key_here
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=true
```

### State Persistence

Echo's state is saved to:
- `echogenesis_data.json` - Main state (needs, personality, growth)
- `user_memory.json` - User interaction history (deprecated, now in memory engine)
- `memory_data/` - FAISS index, documents, and knowledge graph

## Quantum Engine

### Python Simulator (Active)

The Python simulator in `quantum_bridge.py` implements:
- Emotional Hamiltonian evolution
- Entanglement entropy calculation
- FFT-based resonance spectrogram
- Trotterized time evolution

### Rust Engine (Optional)

To use the native Rust quantum engine:

1. Build the Rust module:
   ```bash
   cd ../quantum_engine
   cargo build --release
   ```

2. Copy the compiled library to the backend:
   ```bash
   # Windows
   copy target\release\quantum_engine.pyd ..\backend\

   # Linux/Mac
   cp target/release/libquantum_engine.so ../backend/quantum_engine.so
   ```

3. Restart the backend - it will automatically detect and use the Rust engine

## Development

### Adding New Features

1. **New Service**: Create in `app/services/`
2. **New Endpoint**: Add to `app/main.py`
3. **Tests**: Add to `tests/`
4. **Documentation**: Update this README

### Code Style

- Follow PEP 8
- Use type hints
- Document complex functions
- Keep functions focused and small

### Debugging

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Print quantum state
print(state_manager.quantum_bridge.state_vector)

# Check regulation history
print(state_manager.developmental_engine.get_regulation_stats())
```

## Performance

- **Quantum Optimization**: ~50ms per interaction (Python), ~5ms (Rust)
- **Memory Retrieval**: ~20ms for 1000 memories
- **LLM Call**: ~1-3s (depends on provider)

## Troubleshooting

### Common Issues

**Import Error: quantum_engine**
- This is expected if Rust engine isn't compiled
- Backend will use Python simulator automatically

**FAISS Index Error**
- Delete `memory_data/` folder to reset
- Will rebuild on next interaction

**WebSocket Connection Failed**
- Check CORS settings in `main.py`
- Ensure frontend is running on expected port

## Dependencies

Key packages:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `numpy` - Numerical computing
- `faiss-cpu` - Vector search
- `networkx` - Graph database
- `sentence-transformers` - Embeddings
- `websockets` - Real-time communication

See `requirements.txt` for full list.

## License

MIT License - see root LICENSE file
