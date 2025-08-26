import google.generativeai as genai
import os
import json
import re
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class SentimentAnalyzer:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            raise ValueError("GEMINI_API_KEY not found")
    
    def analyze_single_text(self, text):
        """Analyze sentiment of a single text"""
        try:
            prompt = f"""
            Analyze the sentiment of the following text and return ONLY a JSON response:
            
            Text: "{text}"
            
            Return exactly this JSON format:
            {{
                "sentiment": "positive" or "negative" or "neutral",
                "confidence": confidence_score_0_to_1,
                "emotions": ["happy", "sad", "angry", "excited", "neutral"],
                "key_phrases": ["important", "phrases", "from", "text"],
                "intensity": intensity_score_1_to_10
            }}
            
            Rules:
            - sentiment must be exactly "positive", "negative", or "neutral"
            - confidence must be a number between 0 and 1
            - emotions should be relevant emotions detected
            - key_phrases should be 3-5 important words/phrases
            - intensity should be 1-10 (1=very mild, 10=very strong)
            """
            
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                result = json.loads(json_str)
                
                # Validate and clean result
                result = self.validate_result(result, text)
                return result
            else:
                return self.fallback_analysis(text)
                
        except Exception as e:
            print(f"Error analyzing text: {e}")
            return self.fallback_analysis(text)
    
    def analyze_batch(self, texts):
        """Analyze multiple texts efficiently"""
        results = []
        
        # Process in batches of 5 for efficiency
        batch_size = 5
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            batch_results = self.analyze_batch_gemini(batch)
            results.extend(batch_results)
        
        return results
    
    def analyze_batch_gemini(self, texts):
        """Analyze a batch of texts with Gemini"""
        try:
            texts_json = json.dumps([{"id": i, "text": text} for i, text in enumerate(texts)])
            
            prompt = f"""
            Analyze the sentiment of these texts and return ONLY a JSON array:
            
            Texts: {texts_json}
            
            Return exactly this JSON format:
            [
                {{
                    "id": 0,
                    "sentiment": "positive" or "negative" or "neutral",
                    "confidence": confidence_score_0_to_1,
                    "emotions": ["relevant", "emotions"],
                    "key_phrases": ["important", "phrases"],
                    "intensity": intensity_score_1_to_10
                }},
                ...
            ]
            
            Rules:
            - Return analysis for each text with matching id
            - sentiment must be exactly "positive", "negative", or "neutral"
            - confidence must be between 0 and 1
            - intensity must be between 1 and 10
            """
            
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Extract JSON array from response
            json_match = re.search(r'\[.*\]', result_text, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                results = json.loads(json_str)
                
                # Validate results
                validated_results = []
                for i, result in enumerate(results):
                    if i < len(texts):
                        validated_result = self.validate_result(result, texts[i])
                        validated_results.append(validated_result)
                
                return validated_results
            else:
                # Fallback to individual analysis
                return [self.analyze_single_text(text) for text in texts]
                
        except Exception as e:
            print(f"Error in batch analysis: {e}")
            # Fallback to individual analysis
            return [self.analyze_single_text(text) for text in texts]
    
    def validate_result(self, result, original_text):
        """Validate and clean analysis result"""
        # Ensure required fields exist
        validated = {
            "sentiment": result.get("sentiment", "neutral").lower(),
            "confidence": float(result.get("confidence", 0.5)),
            "emotions": result.get("emotions", ["neutral"]),
            "key_phrases": result.get("key_phrases", []),
            "intensity": int(result.get("intensity", 5)),
            "original_text": original_text[:100] + "..." if len(original_text) > 100 else original_text,
            "analyzed_at": datetime.now().isoformat()
        }
        
        # Validate sentiment values
        if validated["sentiment"] not in ["positive", "negative", "neutral"]:
            validated["sentiment"] = "neutral"
        
        # Validate confidence range
        validated["confidence"] = max(0.0, min(1.0, validated["confidence"]))
        
        # Validate intensity range
        validated["intensity"] = max(1, min(10, validated["intensity"]))
        
        return validated
    
    def fallback_analysis(self, text):
        """Simple fallback analysis when AI fails"""
        positive_words = ["good", "great", "excellent", "amazing", "love", "best", "wonderful", "fantastic"]
        negative_words = ["bad", "terrible", "awful", "hate", "worst", "horrible", "disappointing"]
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            sentiment = "positive"
            confidence = 0.6
        elif negative_count > positive_count:
            sentiment = "negative"
            confidence = 0.6
        else:
            sentiment = "neutral"
            confidence = 0.5
        
        return {
            "sentiment": sentiment,
            "confidence": confidence,
            "emotions": ["neutral"],
            "key_phrases": [],
            "intensity": 5,
            "original_text": text[:100] + "..." if len(text) > 100 else text,
            "analyzed_at": datetime.now().isoformat()
        }
    
    def get_summary_stats(self, results):
        """Calculate summary statistics from analysis results"""
        if not results:
            return {}
        
        total = len(results)
        positive = sum(1 for r in results if r["sentiment"] == "positive")
        negative = sum(1 for r in results if r["sentiment"] == "negative")
        neutral = sum(1 for r in results if r["sentiment"] == "neutral")
        
        avg_confidence = sum(r["confidence"] for r in results) / total
        avg_intensity = sum(r["intensity"] for r in results) / total
        
        # Get most common emotions
        all_emotions = []
        for r in results:
            all_emotions.extend(r["emotions"])
        
        emotion_counts = {}
        for emotion in all_emotions:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        top_emotions = sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "total_analyzed": total,
            "positive_count": positive,
            "negative_count": negative,
            "neutral_count": neutral,
            "positive_percentage": round((positive / total) * 100, 1),
            "negative_percentage": round((negative / total) * 100, 1),
            "neutral_percentage": round((neutral / total) * 100, 1),
            "average_confidence": round(avg_confidence, 2),
            "average_intensity": round(avg_intensity, 1),
            "top_emotions": top_emotions
        }
