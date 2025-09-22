"""
Common utility functions
"""
import random
from typing import List

def get_random_response(responses: List[str]) -> str:
    """Get a random response from a list of responses"""
    return random.choice(responses)

def clamp(value: float, min_value: float, max_value: float) -> float:
    """Clamp a value between min and max bounds"""
    return max(min_value, min(max_value, value))

def is_position_valid(x: float, y: float, margin: float = 15) -> bool:
    """Check if position is within valid screen bounds"""
    return margin <= x <= (100 - margin) and margin <= y <= (100 - margin)