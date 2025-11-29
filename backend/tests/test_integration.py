"""
End-to-End Integration Tests

Tests the full EchoGenesis system integration.
"""

import pytest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.quantum_bridge import QuantumBridge
from app.state_manager import StateManager
from app.services.developmental_engine import DevelopmentalEngine
from app.services.llm_interface import LLMInterface


class TestQuantumBridgeIntegration:
    """Test QuantumBridge integration with advanced features."""
    
    def test_optimize_state_with_entanglement_metrics(self):
        """Test that optimize_state works with entanglement metrics."""
        qb = QuantumBridge()
        
        needs = {"comfort": 30, "stimulation": 70, "connection": 80}
        personality = {"anxiety": 0.6}
        
        # Optimize state
        result = qb.optimize_state(needs, personality)
        
        # Compute entanglement metrics
        metrics = qb.compute_entanglement_metrics()
        
        # Should have computed metrics
        assert "mutual_information" in metrics
        assert "concurrence" in metrics
        
        # High connection need should create some entanglement
        if "0-1" in metrics["concurrence"]:
            assert metrics["concurrence"]["0-1"] >= 0
    
    def test_pde_evolution_integration(self):
        """Test PDE Hamiltonian evolution integration."""
        qb = QuantumBridge()
        
        # Apply PDE evolution
        stats = qb.apply_pde_evolution(
            emotional_state="anxious",
            needs={"comfort": 20, "stimulation": 50, "connection": 50},
            duration=1.0,
            hamiltonian_type="adaptive"
        )
        
        # Should have evolution statistics
        assert "type" in stats
        assert "duration" in stats
        assert "steps" in stats
        assert stats["steps"] > 0
    
    def test_emotional_relaxation(self):
        """Test emotional relaxation feature."""
        qb = QuantumBridge()
        
        # Apply relaxation
        stats = qb.emotional_relaxation(anxiety_level=0.8, duration=2.0)
        
        assert stats["type"] == "relaxation"
        assert stats["duration"] == 2.0
        assert stats["steps"] > 0


class TestStateManagerIntegration:
    """Test StateManager integration."""
    
    @pytest.fixture(autouse=True)
    def mock_dependencies(self, monkeypatch):
        """Mock external dependencies."""
        # Mock SentenceTransformer
        class MockEncoder:
            def encode(self, texts):
                return [np.random.rand(384).astype(np.float32) for _ in texts]
        
        monkeypatch.setattr("app.services.memory_engine.SentenceTransformer", lambda x: MockEncoder())
        monkeypatch.setattr("app.services.memory_engine.COLBERT_AVAILABLE", False)
        
        # Mock LLM generation to avoid Ollama dependency
        async def mock_generate(*args, **kwargs):
            return "Mock response"
            
        monkeypatch.setattr("app.services.llm_interface.LLMInterface.generate_emotional_reply", mock_generate)
    
    @pytest.mark.asyncio
    async def test_state_manager_initialization(self, tmp_path):
        """Test StateManager initializes all components."""
        qb = QuantumBridge()
        sm = StateManager(qb, persistence_dir=str(tmp_path))
        
        # Check all components initialized
        assert sm.quantum_bridge is not None
        assert sm.developmental_engine is not None
        assert sm.llm_interface is not None
        assert sm.memory_engine is not None
    
    @pytest.mark.asyncio
    async def test_process_interaction_flow(self, tmp_path):
        """Test full interaction processing flow."""
        qb = QuantumBridge()
        sm = StateManager(qb, persistence_dir=str(tmp_path))
        
        # Process interaction
        result = await sm.process_interaction("Hello, how are you?")
        
        # Should have response
        assert "reply" in result
        assert "emotional_state" in result
        assert "quantum_metrics" in result
    
    @pytest.mark.asyncio
    async def test_developmental_progression(self, tmp_path):
        """Test developmental stage progression."""
        qb = QuantumBridge()
        sm = StateManager(qb, persistence_dir=str(tmp_path))
        
        initial_stage = sm.state["growth_stage"]
        
        # Simulate many interactions
        for i in range(50):
            await sm.process_interaction(f"Interaction {i}")
        
        # Stage might have progressed
        final_stage = sm.state["growth_stage"]
        assert final_stage >= initial_stage



class TestMemoryEngineIntegration:
    """Test Memory Engine integration."""
    
    @pytest.fixture(autouse=True)
    def mock_dependencies(self, monkeypatch):
        """Mock external dependencies."""
        # Mock SentenceTransformer
        class MockEncoder:
            def encode(self, texts):
                return [np.random.rand(384).astype(np.float32) for _ in texts]
        
        monkeypatch.setattr("app.services.memory_engine.SentenceTransformer", lambda x: MockEncoder())
        
        # Mock FAISS if needed (though code handles it)
        # Mock RAGatouille if needed
        monkeypatch.setattr("app.services.memory_engine.COLBERT_AVAILABLE", False)
    
    def test_memory_storage_and_retrieval(self, tmp_path):
        """Test storing and retrieving memories."""
        qb = QuantumBridge()
        sm = StateManager(qb, persistence_dir=str(tmp_path))
        
        # Add some memories
        sm.memory_engine.add_memory(
            "I love playing games",
            {"emotion": {"primary": "joy", "intensity": 0.8}}
        )
        sm.memory_engine.add_memory(
            "I feel sad when alone",
            {"emotion": {"primary": "sadness", "intensity": 0.6}}
        )
        
        # Retrieve related memories
        memories = sm.memory_engine.retrieve("feeling happy", k=2)
        
        assert len(memories) > 0
    
    def test_cluster_stats(self, tmp_path):
        """Test memory clustering statistics."""
        qb = QuantumBridge()
        sm = StateManager(qb, persistence_dir=str(tmp_path))
        
        # Add memories
        for i in range(10):
            sm.memory_engine.add_memory(
                f"Memory {i}",
                {"emotion": {"primary": "neutral"}}
            )
        
        # Get cluster stats
        stats = sm.memory_engine.get_cluster_stats()
        
        assert "total_memories" in stats
        assert stats["total_memories"] == 10


class TestLLMIntegration:
    """Test LLM interface integration."""
    
    @pytest.fixture(autouse=True)
    def mock_dependencies(self, monkeypatch):
        """Mock external dependencies."""
        # Mock ollama.chat
        class MockResponse:
            def __init__(self):
                self.message = {'content': "Mock response"}
            def __getitem__(self, key):
                return self.message[key] if key == 'message' else None
                
        def mock_chat(*args, **kwargs):
            return {'message': {'content': "Mock response"}}
            
        def mock_list():
            return {'models': []}
            
        monkeypatch.setattr("app.services.llm_interface.ollama.chat", mock_chat)
        monkeypatch.setattr("app.services.llm_interface.ollama.list", mock_list)
    
    @pytest.mark.asyncio
    async def test_llm_conversation_tracking(self):
        """Test conversation history tracking."""
        llm = LLMInterface()
        
        # Get initial stats
        stats = llm.get_conversation_stats()
        initial_exchanges = stats["total_exchanges"]
        
        # Generate reply
        reply = await llm.generate_emotional_reply(
            user_text="Hello",
            emotional_context={"emotional_state": "calm"},
            memories=[],
            personality={"trust": 0.5}
        )
        
        # Check conversation tracked
        stats = llm.get_conversation_stats()
        assert stats["total_exchanges"] == initial_exchanges + 1


class TestEndToEndFlow:
    """Test complete end-to-end flows."""
    
    @pytest.fixture(autouse=True)
    def mock_dependencies(self, monkeypatch):
        """Mock external dependencies."""
        # Mock SentenceTransformer
        class MockEncoder:
            def encode(self, texts):
                return [np.random.rand(384).astype(np.float32) for _ in texts]
        
        monkeypatch.setattr("app.services.memory_engine.SentenceTransformer", lambda x: MockEncoder())
        monkeypatch.setattr("app.services.memory_engine.COLBERT_AVAILABLE", False)
        
        # Mock LLM generation
        async def mock_generate(*args, **kwargs):
            return "Mock response"
            
        monkeypatch.setattr("app.services.llm_interface.LLMInterface.generate_emotional_reply", mock_generate)
    
    @pytest.mark.asyncio
    async def test_full_conversation_cycle(self, tmp_path):
        """Test a complete conversation cycle."""
        qb = QuantumBridge()
        sm = StateManager(qb, persistence_dir=str(tmp_path))
        
        # User says hello
        result1 = await sm.process_interaction("Hello!")
        assert "reply" in result1
        
        # User asks about feelings
        result2 = await sm.process_interaction("How are you feeling?")
        assert "reply" in result2
        
        # Check state evolved
        assert sm.state["interaction_count"] == 2
    
    @pytest.mark.asyncio
    async def test_emotional_state_evolution(self, tmp_path):
        """Test that emotional state evolves over interactions."""
        qb = QuantumBridge()
        sm = StateManager(qb, persistence_dir=str(tmp_path))
        
        initial_emotion = sm.state["emotional_state"]
        
        # Positive interactions
        for _ in range(5):
            await sm.process_interaction("I love you!")
        
        # Emotional state might have changed
        final_emotion = sm.state["emotional_state"]
        # State should have been updated
        assert sm.state["interaction_count"] == 5



if __name__ == "__main__":
    pytest.main([__file__, "-v"])
