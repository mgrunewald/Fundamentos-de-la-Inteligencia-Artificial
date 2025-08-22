import numpy as np


class AdjacentAgent:
    def action(self, board):
        # Search empty neighbors of a player's piece and choose one randomly
        # If no empty neighbors, choose a random empty cell

        neighbors = set()
        for i in range(1, len(board) - 1):
            for j in range(1, len(board) - 1):
                if board[i][j] == 1:
                    neighbors = neighbors.union(self._get_neighbors(i, j, board))

        if len(neighbors) > 0:
            neighbors = list(neighbors)
            target = neighbors[np.random.randint(len(neighbors))]
            return target[0] * len(board) + target[1]
        return np.random.choice(np.flatnonzero(board == 0))

    def _get_neighbors(self, i, j, board):
        neighbors = set()
        for x in range(i - 1, i + 2):
            for y in range(j - 1, j + 2):
                if x == i and y == j:
                    continue
                if board[x][y] == 0:
                    neighbors.add((x, y))
        return neighbors

    def name(self):
        return {"nombre": "Adjacent", "apellido": "Agent", "legajo": 123}

    def __str__(self):
        return "🎭**Adjacent**"
