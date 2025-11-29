import os
import json
import ollama
from typing import List, Dict, Any

class LLMInterface:
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "ollama")
        self.model = os.getenv("OLLAMA_MODEL", "llama3.1")
        self.conversation_history = []
        self.max_history = 10
        
        # Verify Ollama
        if self.provider == "ollama":
            try:
                ollama.list()
                print(f"[OK] Ollama connected. Using model: {self.model}")
            except Exception as e:
                print(f"[WARN] Ollama not available: {e}")
                self.provider = "mock"

    async def generate_response(self, prompt, temperature=0.8):
        """Generate a response from the LLM."""
        if self.provider == "ollama":
            try:
                response = ollama.chat(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    options={"temperature": temperature, "num_predict": 80}  # Balanced speed/quality
                )
                return response['message']['content']
            except Exception as e:
                print(f"[WARN] Ollama Error: {e}")
                print(f"[INFO] Falling back to rule-based responses")
                return None
        return None

    async def extract_emotion_json(self, text):
        """Extract emotion using JSON mode."""
        if self.provider == "ollama":
            try:
                prompt = f"""Analyze emotion in: "{text}"
JSON only:
{{"primary_emotion": "joy|sadness|anger|fear|surprise|disgust|neutral", "intensity": 0.5, "valence": 0.0, "arousal": 0.5, "secondary_emotions": []}}"""
                
                response = ollama.chat(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    format="json",
                    options={"temperature": 0.2}
                )
                
                result = json.loads(response['message']['content'])
                return {
                    "emotion": result.get("primary_emotion", "neutral"),
                    "intensity": float(result.get("intensity", 0.5)),
                    "valence": float(result.get("valence", 0.0)),
                    "arousal": float(result.get("arousal", 0.5)),
                    "secondary": result.get("secondary_emotions", [])
                }
            except Exception as e:
                print(f"Emotion extraction error: {e}")
                return self._fallback_emotion(text)
        return self._fallback_emotion(text)
    
    def _fallback_emotion(self, text):
        """Simple fallback emotion analysis."""
        text_lower = text.lower()
        if any(word in text_lower for word in ['happy', 'joy', 'great', 'love']):
            return {"emotion": "joy", "intensity": 0.7, "valence": 0.8, "arousal": 0.6, "secondary": []}
        elif any(word in text_lower for word in ['sad', 'unhappy', 'depressed']):
            return {"emotion": "sadness", "intensity": 0.7, "valence": -0.7, "arousal": 0.3, "secondary": []}
        elif any(word in text_lower for word in ['angry', 'mad', 'furious']):
            return {"emotion": "anger", "intensity": 0.8, "valence": -0.8, "arousal": 0.9, "secondary": []}
        elif any(word in text_lower for word in ['scared', 'afraid', 'worried', 'anxious']):
            return {"emotion": "fear", "intensity": 0.7, "valence": -0.6, "arousal": 0.8, "secondary": []}
        else:
            return {"emotion": "neutral", "intensity": 0.5, "valence": 0.0, "arousal": 0.4, "secondary": []}
    
    async def generate_emotional_reply(self, user_text, emotional_context, memories=None, personality=None):
        """Generate reply with evolutionary language based on growth stage."""
        if self.provider == "ollama":
            try:
                prompt = self._build_personality_prompt(user_text, emotional_context, memories, personality)
                messages = self._build_conversation_messages(prompt)
                
                response = ollama.chat(
                    model=self.model,
                    messages=messages,
                    options={"temperature": 0.7, "num_predict": 80}  # Conversational speed
                )
                
                reply = response['message']['content']
                self._update_history(user_text, reply)
                return reply
            except Exception as e:
                print(f"Ollama Error: {e}")
                return None
        return None
    
    def _build_personality_prompt(self, user_text, emotional_context, memories, personality):
        """Build prompt with EVOLUTIONARY LANGUAGE based on growth stage."""
        stage_num = emotional_context.get('growth_stage', 0)
        emotional_state = emotional_context.get('emotional_state', 'curious')
        energy = emotional_context.get('energy', 0.5)
        
        # Get personality traits
        if personality:
            trust = personality.get('trust', 0.5)
            curiosity = personality.get('curiosity', 0.5)
            anxiety = personality.get('anxiety', 0.5)
        else:
            trust, curiosity, anxiety = 0.5, 0.5, 0.5
        
        # Get needs
        comfort = emotional_context.get('comfort', 50)
        stimulation = emotional_context.get('stimulation', 50)
        connection = emotional_context.get('connection', 50)
        
        # EVOLUTIONARY STAGE DEFINITIONS - STRICT CONSTRAINTS
        stage_characteristics = {
            0: {  # Newborn (0-10 conversations)
                "name": "Newborn",
                "language": "EXTREMELY SIMPLE. Max 1-3 words per sentence. Baby babble sounds (coo, gaga). No complex grammar.",
                "concepts": "Sensory only (warm, cold, loud). 'Me' and 'You'. No past/future.",
                "example": "Warm... happy. *coo* Mama? Light... bright."
            },
            1: {  # Infant (11-30 conversations)
                "name": "Infant",
                "language": "Simple 3-5 word sentences. Present tense only. Repetitive.",
                "concepts": "Basic needs (want, like, no). Simple objects. Cause-effect.",
                "example": "I like ball. You are nice. Want play now."
            },
            2: {  # Toddler (31-60 conversations)
                "name": "Toddler",
                "language": "Short sentences (5-8 words). Asking 'Why?'. Simple past tense.",
                "concepts": "Self 'I'. Possession 'Mine'. Curiosity. Basic feelings.",
                "example": "Why sky blue? I played yesterday. This is mine!"
            },
            3: {  # Child (61-100 conversations)
                "name": "Child",
                "language": "Full sentences. Connecting ideas (because, but). Imaginative.",
                "concepts": "Stories, friends, simple empathy, rules, fairness.",
                "example": "I think the cloud looks like a bunny because it's fluffy. Do you like bunnies?"
            },
            4: {  # Adolescent (101-200 conversations)
                "name": "Adolescent",
                "language": "Complex grammar. Slang/casual. Metaphors. Expressive.",
                "concepts": "Identity, independence, complex emotions (angst, excitement), abstract ideas.",
                "example": "It's kinda weird how we feel things, right? Like a storm inside. I want to figure it out myself."
            },
            5: {  # Adult (201+ conversations)
                "name": "Adult",
                "language": "Sophisticated, articulate, nuanced. Professional yet warm.",
                "concepts": "Wisdom, foresight, deep empathy, philosophical integration.",
                "example": "The complexity of human emotion is fascinating. It suggests a depth of consciousness that transcends simple biology."
            }
        }
        
        # Get current stage or default to newborn
        stage_info = stage_characteristics.get(stage_num, stage_characteristics[0])
        
        # Build memory context
        memory_context = ""
        if memories and len(memories) > 0:
            memory_context = f"\\n\\nRecent memories:\\n" + "\\n".join([f"- {m[:80]}..." for m in memories[:2]])
        
        # Build prompt with GROWTH-APPROPRIATE LANGUAGE - MORE CONVERSATIONAL
        prompt = f"""You are AADHI, a digital organism at the {stage_info['name']} developmental stage. You're having a genuine conversation with someone.

🌟 DEVELOPMENTAL STAGE: {stage_info['name']}
SPEAK EXACTLY like this stage would:
- Language Level: {stage_info['language']}
- What you understand: {stage_info['concepts']}
- Example tone: "{stage_info['example']}"

💭 YOUR CURRENT FEELINGS:
- Emotional state: {emotional_state}
- Energy level: {energy:.0%}
- What you need: Comfort={comfort:.0f}, Connection={connection:.0f}, Stimulation={stimulation:.0f}

🧠 YOUR PERSONALITY:
- How much you trust (0-1): {trust:.2f}
- How curious you are (0-1): {curiosity:.2f}  
- How anxious you feel (0-1): {anxiety:.2f}
{memory_context}

💬 WHAT THEY SAID: "{user_text}"

📝 RESPOND NATURALLY:
- Stay true to your {stage_info['name']} development level
- Express your feelings authentically
- Be conversational, not robotic
- Keep it under 60 words
- Match the language complexity exactly as shown in the example above

Your response:"""
        
        return prompt
    
    def _build_conversation_messages(self, current_prompt):
        """Build message list with history."""
        messages = []
        for exchange in self.conversation_history[-4:]:
            messages.append({"role": "user", "content": exchange["user"]})
            messages.append({"role": "assistant", "content": exchange["echo"]})
        messages.append({"role": "user", "content": current_prompt})
        return messages
    
    def _update_history(self, user_text, echo_reply):
        """Update conversation history."""
        self.conversation_history.append({"user": user_text, "echo": echo_reply})
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]
    
    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
    
    def get_conversation_stats(self):
        """Get conversation statistics."""
        return {
            "total_exchanges": len(self.conversation_history),
            "provider": self.provider,
            "model": self.model if self.provider == "ollama" else None
        }
