# Ollama Setup Guide for EchoGenesis

## Installation

### 1. Install Ollama

**Windows:**
- Download from: https://ollama.com/download/windows
- Run the installer
- Ollama will start automatically

**Mac:**
```bash
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 2. Pull the Llama 3.1 Model

```bash
# Default model (8B parameters - fast, good quality)
ollama pull llama3.1

# Or use a smaller model for faster responses (3B parameters)
ollama pull llama3.2

# Or use a larger model for better quality (70B parameters - requires 40GB+ RAM)
ollama pull llama3.1:70b
```

### 3. Verify Installation

```bash
# List installed models
ollama list

# Test the model
ollama run llama3.1
>>> Hello!
```

Type `/bye` to exit the test.

## Configuration

### Environment Variables

Create `.env` in `backend/` directory:

```env
# LLM Configuration
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.1

# Alternative models:
# OLLAMA_MODEL=llama3.2        # Smaller, faster
# OLLAMA_MODEL=llama3.1:70b    # Larger, better quality
# OLLAMA_MODEL=mistral         # Alternative model
# OLLAMA_MODEL=gemma2          # Google's model
```

## Model Recommendations

| Model | Size | RAM Required | Speed | Quality | Best For |
|-------|------|--------------|-------|---------|----------|
| `llama3.2` | 2GB | 8GB | ⚡⚡⚡⚡⚡ | ⭐⭐⭐ | Development, testing |
| `llama3.1` | 4.7GB | 8GB | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | **Production (recommended)** |
| `llama3.1:70b` | 40GB | 64GB | ⚡⚡ | ⭐⭐⭐⭐⭐ | High-quality research |
| `mistral` | 4.1GB | 8GB | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | Alternative option |
| `gemma2` | 5.4GB | 8GB | ⚡⚡⚡ | ⭐⭐⭐⭐ | Google's model |

## Usage in EchoGenesis

Once Ollama is installed and a model is pulled, EchoGenesis will automatically:

1. **Detect Ollama** on startup
2. **Generate emotional responses** using the selected model
3. **Extract emotions** from user messages using JSON mode
4. **Adapt responses** based on Echo's developmental stage and emotional state

### Example Output

```
✓ Ollama connected. Using model: llama3.1
RUST ENGINE: Not found. Using Python simulator.
INFO: Uvicorn running on http://127.0.0.1:8000
```

## Troubleshooting

### "Ollama not available" Error

**Solution:**
```bash
# Check if Ollama is running
ollama list

# If not, start Ollama service
# Windows: Ollama starts automatically
# Mac/Linux:
ollama serve
```

### Model Not Found

**Solution:**
```bash
# Pull the model
ollama pull llama3.1

# Verify it's installed
ollama list
```

### Slow Responses

**Solutions:**
1. Use a smaller model: `ollama pull llama3.2`
2. Update `.env`: `OLLAMA_MODEL=llama3.2`
3. Reduce `num_predict` in `llm_interface.py` (default: 256 tokens)

### Out of Memory

**Solutions:**
1. Use smaller model: `llama3.2` instead of `llama3.1`
2. Close other applications
3. Restart Ollama: `ollama serve`

## Advanced Configuration

### Custom Model Parameters

Edit `backend/app/services/llm_interface.py`:

```python
options={
    "temperature": 0.9,      # Creativity (0.0-2.0)
    "num_predict": 150,      # Max tokens
    "top_p": 0.9,           # Nucleus sampling
    "top_k": 40,            # Top-k sampling
    "repeat_penalty": 1.1   # Avoid repetition
}
```

### Using Different Models for Different Tasks

```python
# In llm_interface.py
self.emotion_model = "llama3.2"      # Fast for emotion extraction
self.response_model = "llama3.1:70b" # High quality for responses
```

## Performance Benchmarks

**llama3.1 (8B) on typical hardware:**
- **CPU (8-core)**: ~2-3s per response
- **GPU (RTX 3060)**: ~0.5-1s per response
- **Apple M1/M2**: ~1-2s per response

**llama3.2 (3B):**
- **CPU**: ~1-1.5s per response
- **GPU**: ~0.3-0.5s per response

## Benefits of Ollama

✅ **100% Free** - No API costs  
✅ **Unlimited** - No rate limits  
✅ **Private** - Data never leaves your machine  
✅ **Fast** - Local inference, no network latency  
✅ **Offline** - Works without internet  
✅ **Customizable** - Full control over models and parameters

## Next Steps

1. Install Ollama
2. Pull `llama3.1`
3. Start EchoGenesis backend
4. Chat with Echo and see real AI responses!

For more models, visit: https://ollama.com/library
