import pytest
from app.state_manager import StateManager
from app.quantum_bridge import QuantumBridge
from app.services.memory_engine import MemoryEngine
from app.services.prompt_builder import PromptBuilder

@pytest.fixture
def quantum_bridge():
    return QuantumBridge()

@pytest.fixture
def state_manager(quantum_bridge):
    return StateManager(quantum_bridge)

def test_quantum_initialization(quantum_bridge):
    assert quantum_bridge.qubits == 4
    assert len(quantum_bridge.state_vector) == 16
    assert quantum_bridge.state_vector[0] == 1.0 + 0j

def test_quantum_optimization(quantum_bridge):
    needs = {"comfort": 50, "stimulation": 50}
    personality = {"anxiety": 0.1}
    metrics = quantum_bridge.optimize_state(needs, personality, 0.5)
    
    assert "ground_state_energy" in metrics
    assert "entanglement_entropy" in metrics
    assert 0.0 <= metrics["ground_state_energy"] <= 1.0

def test_memory_engine():
    engine = MemoryEngine(persistence_dir="test_memory")
    engine.add_memory("I love you Echo", {"role": "user"})
    results = engine.retrieve("love")
    assert len(results) > 0
    assert "I love you Echo" in results

def test_prompt_builder():
    builder = PromptBuilder()
    state = {
        "growth_stage": 0,
        "needs": {"comfort": 80},
        "emotional_state": "calm",
        "quantum": {"energy": 0.1}
    }
    prompt = builder.build_prompt(state, "Hello")
    assert "You are a newborn" in prompt
    assert "Comfort: 80/100" in prompt

@pytest.mark.asyncio
async def test_full_interaction_loop(state_manager):
    result = await state_manager.process_interaction("Hello Echo")
    assert isinstance(result, dict)
    assert "reply" in result
    assert isinstance(result["reply"], str)
    assert len(result["reply"]) > 0
    
    # Check state update
    assert state_manager.state["needs"]["connection"] > 50 # Should have increased
