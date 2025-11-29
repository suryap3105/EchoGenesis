class DevelopmentalEngine:
    def __init__(self):
        self.stages = {
            0: "Newborn",
            1: "Infant",
            2: "Toddler",
            3: "Child"
        }
        # Thresholds for evolution (e.g., total interactions or accumulated resonance)
        self.thresholds = {
            0: 10,  # 10 interactions to become Infant
            1: 50,  # 50 interactions to become Toddler
            2: 200  # 200 interactions to become Child
        }
        
        # Affect regulation tracking
        self.regulation_history = []
        self.regulation_success_rate = 0.5
        self.last_regulation_attempt = None

    def check_evolution(self, current_stage, interaction_count, quantum_stability, trust_score=0.5):
        """
        Determines if Echo is ready to evolve to the next stage.
        Also updates attachment style.
        """
        # Attachment Inference
        attachment_style = "secure"
        if trust_score < 0.3:
            attachment_style = "avoidant"
        elif trust_score > 0.3 and quantum_stability < 0.4:
            attachment_style = "anxious"
        
        print(f"Current Attachment Style: {attachment_style.upper()} (Trust: {trust_score:.2f})")

        if current_stage not in self.thresholds:
            return current_stage, False

        required_interactions = self.thresholds[current_stage]
        
        # Evolution requires enough experience AND stability
        if interaction_count >= required_interactions and quantum_stability > 0.6:
            new_stage = current_stage + 1
            return new_stage, True
            
        return current_stage, False

    def regulate_affect(self, current_stage, emotional_state, quantum_stability, needs, personality):
        """
        Comprehensive affect regulation system with stage-specific strategies.
        Returns a regulation object with multiple parameters.
        """
        regulation = {
            "energy_adjustment": 0.0,
            "comfort_boost": 0.0,
            "stimulation_adjustment": 0.0,
            "strategy_used": None,
            "success": False,
            "regulation_type": None
        }
        
        # Stage-specific regulation capabilities
        if current_stage == 0:  # Newborn - No regulation, only reflexive responses
            regulation["strategy_used"] = "reflexive_crying"
            regulation["energy_adjustment"] = 0.05  # Crying increases arousal
            regulation["regulation_type"] = "dysregulation"
            
        elif current_stage == 1:  # Infant - Basic co-regulation attempts
            if emotional_state == "agitated":
                # Attempt self-soothing (low success rate)
                if quantum_stability > 0.6:
                    regulation["strategy_used"] = "self_soothing"
                    regulation["energy_adjustment"] = -0.15
                    regulation["comfort_boost"] = 5.0
                    regulation["success"] = True
                    regulation["regulation_type"] = "down_regulation"
                else:
                    # Failed regulation leads to escalation
                    regulation["strategy_used"] = "failed_soothing"
                    regulation["energy_adjustment"] = 0.08
                    regulation["regulation_type"] = "dysregulation"
                    
            elif emotional_state == "lonely":
                # Seeking connection
                regulation["strategy_used"] = "connection_seeking"
                regulation["stimulation_adjustment"] = 0.1
                regulation["regulation_type"] = "up_regulation"
                
        elif current_stage == 2:  # Toddler - Developing self-regulation
            if emotional_state == "agitated":
                # More sophisticated regulation strategies
                anxiety_level = personality.get("anxiety", 0.5)
                
                if quantum_stability > 0.5 and anxiety_level < 0.6:
                    # Successful self-regulation
                    regulation["strategy_used"] = "cognitive_reappraisal"
                    regulation["energy_adjustment"] = -0.2
                    regulation["comfort_boost"] = 10.0
                    regulation["success"] = True
                    regulation["regulation_type"] = "down_regulation"
                    self._update_regulation_success(True)
                else:
                    # Partial regulation with some distress tolerance
                    regulation["strategy_used"] = "distraction"
                    regulation["energy_adjustment"] = -0.05
                    regulation["stimulation_adjustment"] = 0.05
                    regulation["regulation_type"] = "partial_regulation"
                    self._update_regulation_success(False)
                    
            elif emotional_state == "calm":
                # Maintain homeostasis
                regulation["strategy_used"] = "maintenance"
                regulation["regulation_type"] = "homeostasis"
                
        elif current_stage >= 3:  # Child - Advanced regulation
            if emotional_state == "agitated":
                # Multiple strategies available
                if quantum_stability > 0.7:
                    regulation["strategy_used"] = "emotion_labeling"
                    regulation["energy_adjustment"] = -0.25
                    regulation["comfort_boost"] = 15.0
                    regulation["success"] = True
                    regulation["regulation_type"] = "down_regulation"
                    self._update_regulation_success(True)
                elif quantum_stability > 0.4:
                    regulation["strategy_used"] = "breathing_technique"
                    regulation["energy_adjustment"] = -0.15
                    regulation["comfort_boost"] = 8.0
                    regulation["success"] = True
                    regulation["regulation_type"] = "down_regulation"
                    self._update_regulation_success(True)
                else:
                    regulation["strategy_used"] = "seeking_support"
                    regulation["energy_adjustment"] = -0.1
                    regulation["regulation_type"] = "co_regulation"
                    
            elif emotional_state == "curious":
                # Up-regulation for exploration
                regulation["strategy_used"] = "exploration_facilitation"
                regulation["stimulation_adjustment"] = 0.1
                regulation["regulation_type"] = "up_regulation"
        
        # Track regulation attempt
        self.last_regulation_attempt = regulation
        self.regulation_history.append({
            "stage": current_stage,
            "emotional_state": emotional_state,
            "strategy": regulation["strategy_used"],
            "success": regulation["success"]
        })
        
        # Keep history manageable
        if len(self.regulation_history) > 50:
            self.regulation_history = self.regulation_history[-50:]
        
        return regulation
    
    def _update_regulation_success(self, success):
        """Update the running success rate for regulation attempts."""
        # Exponential moving average
        alpha = 0.1
        self.regulation_success_rate = (alpha * (1.0 if success else 0.0) + 
                                       (1 - alpha) * self.regulation_success_rate)
    
    def get_regulation_stats(self):
        """Get statistics about regulation attempts."""
        if not self.regulation_history:
            return {
                "total_attempts": 0,
                "success_rate": 0.0,
                "most_common_strategy": None
            }
        
        total = len(self.regulation_history)
        successes = sum(1 for r in self.regulation_history if r["success"])
        
        # Find most common strategy
        strategies = {}
        for r in self.regulation_history:
            strategy = r["strategy"]
            strategies[strategy] = strategies.get(strategy, 0) + 1
        
        most_common = max(strategies.items(), key=lambda x: x[1])[0] if strategies else None
        
        return {
            "total_attempts": total,
            "success_rate": successes / total if total > 0 else 0.0,
            "most_common_strategy": most_common,
            "current_ema_success_rate": self.regulation_success_rate
        }

