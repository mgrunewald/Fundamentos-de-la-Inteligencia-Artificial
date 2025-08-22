import numpy as np


class HalfAgent:
    # this agent is missing name and __str__ methods
    def action(self, board):
        available = np.flatnonzero(board == 0)
        len_available = len(available)
        return available[len_available // 2]
    
    def name(self):
        return {"nombre": "Half", "apellido": "Agent", "legajo": 0.5}
    
    def __str__(self):
        return "🥥**Half**"
