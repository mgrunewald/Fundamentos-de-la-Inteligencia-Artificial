import numpy as np


class FirstAgent:
    def action(self, board):
        return np.flatnonzero(board == 0)[0]

    def name(self):
        return {"nombre": "First", "apellido": "Agent", "legajo": -1}

    def __str__(self):
        return "🥇**First**"
