class CenterAgent:
    # Tries to play as close to the center as possible
    def action(self, board):
        distances = {}
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == 0:
                    distances[i * len(board) + j] = self._distance(i, j, len(board))
        return min(distances, key=distances.get)

    def _distance(self, i, j, n):
        return abs(i - n // 2) + abs(j - n // 2)

    def name(self):
        return {"nombre": "Center", "apellido": "Agent", "legajo": 99}

    def __str__(self):
        return "🎯**Center**"
