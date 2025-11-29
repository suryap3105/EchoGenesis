class EmotionAnalyzer:
    def analyze(self, text: str):
        # Very basic keyword analysis
        text = text.lower()
        sentiment = 0.0
        keywords = {
            "love": 0.8, "good": 0.5, "happy": 0.6,
            "bad": -0.5, "sad": -0.6, "hate": -0.8,
            "hello": 0.2, "hi": 0.2
        }
        
        for word, score in keywords.items():
            if word in text:
                sentiment += score
                
        return {
            "sentiment": max(-1.0, min(1.0, sentiment)),
            "intensity": abs(sentiment)
        }
