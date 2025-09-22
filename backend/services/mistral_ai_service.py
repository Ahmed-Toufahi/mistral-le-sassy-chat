"""
Mistral AI integration service
"""
import requests
import json
import random
from typing import Optional
from core.models import CatState, CatResponse, Position
from config.settings import settings

class MistralAIService:
    def __init__(self):
        self.api_key = settings.MISTRAL_API_KEY
        self.base_url = settings.MISTRAL_BASE_URL
        self.model = settings.MISTRAL_MODEL
        self.simple_mode = False  
        
    def extract_json(self, content: str) -> dict:
        """Extract valid JSON from AI response, handling markdown formatting"""
        try:
            content = content.strip()
            
            if content.startswith("```json"):
                content = content.replace("```json", "").replace("```", "").strip()
            elif content.startswith("```"):
                content = content.replace("```", "").strip()
            
            content = content.strip()
            
            return json.loads(content)
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Content was: {content}")
            return None
        except Exception as e:
            print(f"JSON extraction error: {e}")
            return None
        
    async def respond_to_chat(self, user_message: str, current_state: CatState) -> CatResponse:
        """Generate response to user chat message"""
        if self.simple_mode:
            return self._smart_chat_response(user_message, current_state)
            
        prompt = f"""You are a cat. User says: "{user_message}"

Current position: x={current_state.position.x}, y={current_state.position.y}

Rules:
- If user says "come here" or "come", move to x:50, y:50
- If user says "move up", decrease y by 20
- If user says "move down", increase y by 20  
- If user says "move left", decrease x by 20
- If user says "move right", increase x by 20
- If no movement command, keep current position
- action MUST be: "walking", "sitting", "sleeping", "playing", "grooming", or "stretching"
- mood MUST be: "sleepy", "playful", "curious", "aloof", or "hungry"

Respond with JSON only:
{{"text": "short cat response", "action": "sitting", "thought": "brief thought", "new_position": {{"x": {current_state.position.x}, "y": {current_state.position.y}}}, "mood": "playful"}}"""

        try:
            print(f"Sending chat request to Mistral Medium API...")
            response = requests.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.5,
                    "max_tokens": 150
                },
                timeout=15
            )
            
            print(f"Mistral API response status: {response.status_code}")
            
            if response.status_code == 200:
                content = response.json()["choices"][0]["message"]["content"]
                print(f"AI response content: {content}")
                
                data = self.extract_json(content)
                if not data:
                    print("Failed to extract JSON, using fallback")
                    return self._fallback_response(user_message, current_state)
                
                print(f"Parsed JSON: {data}")
                
                # Validate and fix action if needed
                valid_actions = ["walking", "sitting", "sleeping", "playing", "grooming", "stretching"]
                action = data.get("action", "sitting")
                if action not in valid_actions:
                    # Map invalid actions to valid ones
                    action_mapping = {
                        "pawing_at_nothing": "playing",
                        "pouncing": "playing", 
                        "meowing": "sitting",
                        "purring": "sitting",
                        "hunting": "playing",
                        "exploring": "walking",
                        "resting": "sitting",
                        "lounging": "sitting"
                    }
                    action = action_mapping.get(action, "sitting")
                    print(f"Mapped invalid action to: {action}")
                
                valid_moods = ["sleepy", "playful", "curious", "aloof", "hungry"]
                mood = data.get("mood", "playful")
                if mood not in valid_moods:
                    mood_mapping = {
                        "excited": "playful",
                        "happy": "playful",
                        "content": "curious", 
                        "relaxed": "sleepy",
                        "energetic": "playful",
                        "calm": "curious"
                    }
                    mood = mood_mapping.get(mood, "playful")
                    print(f"Mapped invalid mood to: {mood}")
                
                new_pos = data.get("new_position")
                if new_pos:
                    new_pos["x"] = max(15, min(85, new_pos["x"]))
                    new_pos["y"] = max(15, min(85, new_pos["y"]))
                
                return CatResponse(
                    text=data.get("text", "Meow! I'm here for you!"),
                    action=action,
                    thought=data.get("thought", "I love my human!"),
                    new_position=Position(**new_pos) if new_pos else None,
                    mood=mood
                )
            else:
                print(f"API Error: {response.status_code} - {response.text}")
            
        except Exception as e:
            print(f"Chat AI Error: {e}")
        
        return self._fallback_response(user_message, current_state)
    
    def _fallback_response(self, user_message: str, state: CatState) -> CatResponse:
        """Basic fallback responses"""
        responses = ["Meow!", "Yes human!", "I hear you!", "What can I do?", "At your service!"]
        actions = ["sitting", "walking", "playing", "stretching"]
        
        new_x = max(20, min(80, state.position.x + random.randint(-15, 15)))
        new_y = max(20, min(80, state.position.y + random.randint(-15, 15)))
        
        return CatResponse(
            text=random.choice(responses),
            action=random.choice(actions),
            thought="I love my human!",
            new_position=Position(x=new_x, y=new_y),
            mood="playful"
        )
    
    def _smart_chat_response(self, user_message: str, state: CatState) -> CatResponse:
        """Smart responses based on user input without API calls"""
        msg = user_message.lower()
        
        if any(word in msg for word in ["hello", "hi", "hey"]):
            if any(word in msg for word in ["how are you", "how's it going", "how do you feel"]):
                responses = [
                    "I'm doing great! Thank you for asking! *purrs happily*",
                    "I'm wonderful! Just enjoying life as a digital cat! *stretches contentedly*",
                    "I'm fantastic! Ready to play or chat whenever you want! *tail swishes*",
                    "I'm doing purr-fectly! How are you doing, human?",
                    "I'm feeling great! Thanks for caring about me! *rubs against screen*"
                ]
            else:
                responses = ["Hello human!", "Hi there!", "Meow hello!", "Purr! Hi!", "Greetings! *wave paw*"]
            action = "sitting"
            new_x, new_y = state.position.x, state.position.y
            
        elif any(word in msg for word in ["come", "here", "over"]):
            responses = ["Coming right away!", "On my way!", "Here I come!", "Yes, master!"]
            action = "walking"
            new_x, new_y = 50, 50  
            
        elif any(word in msg for word in ["sit", "stay", "down"]):
            responses = ["Sitting pretty!", "I'm sitting!", "Good cat position!", "Sitting like a good kitty!"]
            action = "sitting"
            new_x, new_y = state.position.x, state.position.y  # Stay in place
            
        elif any(word in msg for word in ["play", "fun", "toy"]):
            responses = ["Let's play!", "Playtime!", "I love playing!", "Yay, games!"]
            action = "playing"
            new_x = max(20, min(80, state.position.x + random.randint(-20, 20)))
            new_y = max(20, min(80, state.position.y + random.randint(-20, 20)))
            
        elif any(word in msg for word in ["move", "walk", "go"]):
            if "up" in msg:
                responses = ["Moving up!", "Going up as requested!", "Upward bound!"]
                action = "walking"
                new_x = state.position.x
                new_y = max(20, state.position.y - 20)
            elif "down" in msg:
                responses = ["Moving down!", "Going down as requested!", "Downward bound!"]
                action = "walking"
                new_x = state.position.x
                new_y = min(80, state.position.y + 20)
            elif "left" in msg:
                responses = ["Moving left!", "Going left as requested!", "Leftward bound!"]
                action = "walking"
                new_x = max(20, state.position.x - 20)
                new_y = state.position.y
            elif "right" in msg:
                responses = ["Moving right!", "Going right as requested!", "Rightward bound!"]
                action = "walking"
                new_x = min(80, state.position.x + 20)
                new_y = state.position.y
            else:
                responses = ["Moving as requested!", "Going where you want!", "Walking around!", "On the move!"]
                action = "walking"
                new_x = max(20, min(80, random.randint(30, 70)))
                new_y = max(20, min(80, random.randint(30, 70)))
                
        else:
            responses = ["Meow!", "Yes human!", "I hear you!", "What can I do?", "At your service!"]
            action = "sitting"
            new_x, new_y = state.position.x, state.position.y
        
        return CatResponse(
            text=random.choice(responses),
            action=action,
            thought="I love chatting with my human!",
            new_position=Position(x=new_x, y=new_y),
            mood="playful"
        )