"""
Pydantic models for the cat application
"""
from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime

MoodType = Literal["sleepy", "playful", "curious", "aloof", "hungry"]
ActionType = Literal["walking", "sitting", "sleeping", "playing", "grooming", "stretching"]

class Position(BaseModel):
    x: float
    y: float
    
    def to_dict(self):
        return {"x": self.x, "y": self.y}

class CatState(BaseModel):
    position: Position = Position(x=50, y=50)
    mood: MoodType = "playful"
    action: ActionType = "sitting"
    thought: str = "Hello! I'm ready to play!"
    last_interaction: datetime = datetime.now()
    
    def update_from_response(self, response: 'CatResponse'):
        if response.new_position:
            self.position = response.new_position
        if response.action:
            self.action = response.action
        if response.thought:
            self.thought = response.thought
        if response.mood:
            self.mood = response.mood
        self.last_interaction = datetime.now()
    
    def to_dict(self):
        return {
            "position": {"x": self.position.x, "y": self.position.y},
            "mood": self.mood,
            "action": self.action,
            "thought": self.thought,
            "last_interaction": self.last_interaction.isoformat()
        }

class ChatMessage(BaseModel):
    text: str

class CatResponse(BaseModel):
    text: str
    action: ActionType = "sitting"
    thought: str = "I'm being a good cat!"
    new_position: Optional[Position] = None
    mood: MoodType = "playful"