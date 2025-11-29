import numpy as np
import networkx as nx
import json
import os
import pickle
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Tuple
import warnings
from collections import deque

# Optional imports - graceful degradation
try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    warnings.warn("FAISS not available. Using simple vector search fallback.")

try:
    import metis
    METIS_AVAILABLE = True
except (ImportError, RuntimeError, OSError):
    METIS_AVAILABLE = False
    print("[Memory] METIS not available (DLL missing). Using NetworkX fallback.")

try:
    from ragatouille import RAGPretrainedModel
    COLBERT_AVAILABLE = True
except ImportError:
    COLBERT_AVAILABLE = False
    warnings.warn("RAGatouille not available. ColBERT re-ranking disabled.")

class HierarchicalMemory:
    """
    3-Tier Hierarchical Retrieval Memory (HRM) System:
    - L1: Working Memory (10 most recent, instant access)
    - L2: Cluster Memory (50 items, FAISS search)
    - L3: Long-term Memory (All items, NetworkX + ColBERT)
    """
    def __init__(self, l1_size=10, l2_size=50):
        self.l1_size = l1_size
        self.l2_size = l2_size
        
        # L1: Working Memory (deque for O(1) append/pop)
        self.l1_memory = deque(maxlen=l1_size)
        
        # L2: Cluster Memory (track cluster IDs for fast access)
        self.l2_indices = set()
        
        # Importance scores (for L2/L3 promotion)
        self.importance_scores = {}
    
    def add_to_l1(self, doc_id: int, text: str):
        """Add to working memory (L1)."""
        self.l1_memory.append((doc_id, text))
    
    def is_in_l1(self, doc_id: int) -> bool:
        """Check if doc is in working memory."""
        return any(did == doc_id for did, _ in self.l1_memory)
    
    def get_l1_texts(self) -> List[str]:
        """Get all L1 texts."""
        return [text for _, text in self.l1_memory]
    
    def promote_to_l2(self, doc_id: int):
        """Promote document to L2 (cluster memory)."""
        self.l2_indices.add(doc_id)
        if len(self.l2_indices) > self.l2_size:
            # Evict lowest importance
            min_id = min(self.l2_indices, key=lambda x: self.importance_scores.get(x, 0))
            self.l2_indices.discard(min_id)
    
    def update_importance(self, doc_id: int, score: float):
        """Update importance score for a document."""
        self.importance_scores[doc_id] = score


class MemoryEngine:
    def __init__(self, persistence_dir="memory_data"):
        self.persistence_dir = persistence_dir
        if not os.path.exists(persistence_dir):
            os.makedirs(persistence_dir)
            
        # Hierarchical Memory System (HRM)
        self.hrm = HierarchicalMemory(l1_size=10, l2_size=50)
        
        # Vector Store (FAISS or fallback)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.dimension = 384
        
        if FAISS_AVAILABLE:
            self.faiss_index = faiss.IndexFlatL2(self.dimension)
            self.use_faiss = True
        else:
            self.faiss_index = None
            self.use_faiss = False
            self.vectors = []
            
        self.documents = []
        
        # Knowledge Graph (NetworkX)
        self.kg = nx.Graph()
        
        # Clustering
        self.clusters = {}
        self.doc_to_cluster = {}
        
        # ColBERT Re-ranker
        if COLBERT_AVAILABLE:
            try:
                self.reranker = RAGPretrainedModel.from_pretrained("colbert-ir/colbertv2.0")
                print("[OK] ColBERT re-ranker loaded")
            except Exception as e:
                print(f"[WARN] ColBERT loading failed: {e}")
                self.reranker = None
        else:
            self.reranker = None
        
        # Load existing data
        self.load()

    def add_memory(self, text: str, metadata: Dict[str, Any] = None):
        """Add memory with HRM integration."""
        metadata = metadata or {}
        
        # 1. Vector Store
        embedding = self.embedding_model.encode(text)
        mem_id = len(self.documents)
        
        # Store in FAISS or fallback
        if self.use_faiss:
            self.faiss_index.add(np.array([embedding], dtype="float32"))
        else:
            self.vectors.append(embedding)
        
        # Store document
        self.documents.append({"text": text, "metadata": metadata, "id": mem_id})
        
        # 2. HRM: Add to L1 (Working Memory)
        self.hrm.add_to_l1(mem_id, text)
        
        # 3. Knowledge Graph
        self.kg.add_node(mem_id, text=text[:50], **metadata)
        self._add_emotional_edges(mem_id, metadata.get("emotion", {}))
        
        # 4. Trigger clustering if needed
        if len(self.documents) % 10 == 0 and len(self.documents) >= 20:
            self._cluster_memories()
        
        self.save()

    def retrieve(self, query: str, k: int = 3, emotional_context: Dict = None) -> List[str]:
        """
        Hierarchical Retrieval with L1 → L2 → L3 cascade.
        """
        if not self.documents:
            return []
        
        # **L1: Working Memory Check** (Instant)
        l1_texts = self.hrm.get_l1_texts()
        if len(l1_texts) >= k:
            # If L1 has enough, return most recent
            return l1_texts[-k:]
        
        # **L2: Cluster-Based Fast FAISS** (Fast)
        query_embedding = self.embedding_model.encode(query)
        
        if self.use_faiss and self.faiss_index.ntotal > 0:
            # Search in FAISS
            distances, indices = self.faiss_index.search(
                np.array([query_embedding], dtype="float32"), 
                min(k * 3, len(self.documents))  # Over-retrieve for re-ranking
            )
            candidate_ids = indices[0].tolist()
        else:
            # Fallback: cosine similarity
            vectors = np.array(self.vectors)
            scores = np.dot(vectors, query_embedding) / (
                np.linalg.norm(vectors, axis=1) * np.linalg.norm(query_embedding)
            )
            candidate_ids = np.argsort(scores)[::-1][:k*3].tolist()
        
        # **L3: ColBERT Re-ranking** (Slower, high accuracy)
        if self.reranker and len(candidate_ids) > k:
            candidate_texts = [self.documents[i]["text"] for i in candidate_ids if i < len(self.documents)]
            try:
                ranked = self.reranker.rerank(query, candidate_texts, k=k)
                result_texts = [r["content"] for r in ranked]
            except:
                # Fallback to L2 results
                result_texts = [self.documents[i]["text"] for i in candidate_ids[:k] if i < len(self.documents)]
        else:
            result_texts = [self.documents[i]["text"] for i in candidate_ids[:k] if i < len(self.documents)]
        
        # **Update HRM importance scores**
        for idx in candidate_ids[:k]:
            if idx < len(self.documents):
                self.hrm.update_importance(idx, 1.0)
                self.hrm.promote_to_l2(idx)
        
        return result_texts[:k]

    def _add_emotional_edges(self, mem_id: int, emotion: Dict):
        """Add edges based on emotional similarity."""
        if not emotion:
            return
        
        current_valence = emotion.get("valence", 0)
        
        # Connect to similar emotional memories
        for node_id in list(self.kg.nodes())[-min(10, len(self.kg.nodes())):]:
            if node_id == mem_id:
                continue
            node_data = self.kg.nodes.get(node_id, {})
            other_emotion = node_data.get("emotion", {})
            other_valence = other_emotion.get("valence", 0)
            
            # High similarity = strong edge
            similarity = 1.0 - abs(current_valence - other_valence) / 2.0
            if similarity > 0.6:
                self.kg.add_edge(mem_id, node_id, weight=similarity)

    def _cluster_memories(self):
        """Cluster memories using NetworkX greedy modularity."""
        if len(self.documents) < 5:
            return
        
        try:
            import networkx.algorithms.community as community
            
            # Create graph from vectors
            G = nx.Graph()
            for i in range(len(self.documents)):
                G.add_node(i)
            
            # Get vectors for clustering
            if self.use_faiss:
                vectors_for_clustering = [self.embedding_model.encode(d["text"]) for d in self.documents]
            else:
                vectors_for_clustering = self.vectors
            
            if not vectors_for_clustering:
                return
            
            vectors = np.array(vectors_for_clustering)
            norms = np.linalg.norm(vectors, axis=1, keepdims=True)
            normalized = vectors / (norms + 1e-9)
            sim_matrix = np.dot(normalized, normalized.T)
            
            # Add edges
            rows, cols = np.where(sim_matrix > 0.7)
            for r, c in zip(rows, cols):
                if r < c:
                    G.add_edge(r, c, weight=float(sim_matrix[r, c]))
            
            # Detect communities
            communities = list(community.greedy_modularity_communities(G))
            
            # Update clusters
            self.clusters = {}
            self.doc_to_cluster = {}
            for cid, nodes in enumerate(communities):
                self.clusters[cid] = list(nodes)
                for node_id in nodes:
                    self.doc_to_cluster[node_id] = cid
                    if node_id in self.kg.nodes:
                        self.kg.nodes[node_id]['cluster'] = cid
            
            print(f"[HRM] Clustered {len(self.documents)} memories into {len(self.clusters)} communities")
        except Exception as e:
            print(f"[WARN] Clustering failed: {e}")

    def save(self):
        """Save memory engine state."""
        data = {
            "documents": self.documents,
            "clusters": self.clusters,
            "doc_to_cluster": self.doc_to_cluster,
            "hrm_importance": self.hrm.importance_scores
        }
        
        with open(os.path.join(self.persistence_dir, "docs.json"), "w") as f:
            json.dump(data, f)
        
        if self.use_faiss and self.faiss_index.ntotal > 0:
            faiss.write_index(self.faiss_index, os.path.join(self.persistence_dir, "faiss.index"))
        
        if self.kg.number_of_nodes() > 0:
            nx.write_gexf(self.kg, os.path.join(self.persistence_dir, "kg.gexf"))

    def load(self):
        """Load memory engine state."""
        docs_file = os.path.join(self.persistence_dir, "docs.json")
        if os.path.exists(docs_file):
            with open(docs_file, "r") as f:
                data = json.load(f)
                self.documents = data.get("documents", [])
                self.clusters = {int(k): v for k, v in data.get("clusters", {}).items()}
                self.doc_to_cluster = {int(k): v for k, v in data.get("doc_to_cluster", {}).items()}
                self.hrm.importance_scores = {int(k): v for k, v in data.get("hrm_importance", {}).items()}
        
        faiss_file = os.path.join(self.persistence_dir, "faiss.index")
        if self.use_faiss and os.path.exists(faiss_file):
            self.faiss_index = faiss.read_index(faiss_file)
        
        kg_file = os.path.join(self.persistence_dir, "kg.gexf")
        if os.path.exists(kg_file):
            self.kg = nx.read_gexf(kg_file)
        
        print(f"[OK] Memory loaded: {len(self.documents)} memories, {len(self.clusters)} clusters (HRM enabled)")
