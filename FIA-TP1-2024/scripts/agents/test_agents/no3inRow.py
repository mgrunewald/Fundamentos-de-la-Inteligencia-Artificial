import numpy as np


class No3inRowAgent:
    # if there is a 3 in a row, block it
    # Otherwise, play last flat empty cell
    def action(self, board):
        self.len = len(board)

        for i in range(self.len):
            for j in range(self.len):
                if board[i][j] == 0:
                    board[i][j] = -1
                    if self._check_4(board, -1):
                        board[i][j] = 0
                        return i * self.len + j
                    board[i][j] = 0

        return np.flatnonzero(board == 0)[-1]

    def _check_4(self, board, player=1):
        # Checks four -1 in a row, column or diagonal
        for i in range(0, self.len - 4):
            for j in range(0, self.len - 4):
                if (
                    board[i][j] == player
                    and board[i + 1][j + 1] == player
                    and board[i + 2][j + 2] == player
                    and board[i + 3][j + 3] == player
                ):
                    return True
                if (
                    board[i][j] == player
                    and board[i + 1][j] == player
                    and board[i + 2][j] == player
                    and board[i + 3][j] == player
                ):
                    return True
                if (
                    board[i][j] == player
                    and board[i][j + 1] == player
                    and board[i][j + 2] == player
                    and board[i][j + 3] == player
                ):
                    return True
                if (
                    board[i][j + 3] == player
                    and board[i + 1][j + 2] == player
                    and board[i + 2][j + 1] == player
                    and board[i + 3][j] == player
                ):
                    return True
        return False

    def name(self):
        return {"nombre": "No3inRow", "apellido": "Agent", "legajo": -3}

    def __str__(self):
        return "❌**No3inRow**⚪⚪⚫"
