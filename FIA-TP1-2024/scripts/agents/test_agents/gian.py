# Quiero lograr el mejor agente con minimax de profundidad 0

from typing import Tuple

import numpy as np


class BoardShape:
    def __init__(self, board):
        shapex, shapey = board.shape
        self.rangex = range(shapex)
        self.rangey = range(shapey)

    def __contains__(self, item):
        return item[0] in self.rangex and item[1] in self.rangey

class MoveLog:
    def __init__(self):
        self.moves = []

    def append(self, x, y):
        self.moves.append((x, y))

    def get_direction(self, x1, y1, x2, y2) -> Tuple[int, int]:
        dirx = (abs(x1 - x2) / max(abs(x1 - x2), 1))
        diry = (abs(y1 - y2) / max(abs(y1 - y2), 1))
        return dirx, diry

    def in_current_direction(self, x, y) -> bool:
        if len(self.moves) < 2:
            return False
        last_move = self.moves[-1]
        previous_to_last_move = self.moves[-1]
        current_dir = self.get_direction(*previous_to_last_move, *last_move)
        new_direction = self.get_direction(*last_move, *(x, y))
        return current_dir[0] == new_direction[0] and current_dir[1] == new_direction[1]

class SmartBoard:
    def __init__(self, board):
        self.board = board
        self.board_shape = BoardShape(board)
        self.adyacent_moves = {}
        self.move_log = MoveLog()

    def __hash__(self):
        return hash(str(self.board))

    def __eq__(self, other):
        return hash(self.board) == hash(other.board)

    def available(self, x, y):
        return x >= 0 and y >= 0 and (x, y) in self.board_shape and self.board[x][y] == 0

    def update(self, board):
        for i in range(board.shape[0]):
            for j in range(board.shape[1]):
                if board[i][j] != self.board[i][j] and (i, j) in self.adyacent_moves:
                    del self.adyacent_moves[(i, j)]
        self.board = board

    @staticmethod
    def middleness(pos, middle):
        return 1 - ( abs(pos-middle)/middle )

    def middleness_score(self, pos):
        middle = (self.board.shape[0] // 2, self.board.shape[1] // 2)
        return SmartBoard.middleness(pos[0], middle[0]) * SmartBoard.middleness(pos[1], middle[1])

    def get_best_next_move(self):
        if not self.adyacent_moves:
            move_score = 1
            valid_pos = np.where(self.board == 0)
            valid_pos = [(x, y) for x, y in zip(valid_pos[0], valid_pos[1])]
            valid_pos = sorted(valid_pos, key=lambda item: -self.middleness_score(item))
            x, y = valid_pos[0]
        else:
            (x, y), move_score = sorted(self.adyacent_moves.items(),
                                        key=lambda item: -(item[1] +
                                                           self.middleness_score(item[0])
                                                           + item[1] * self.move_log.in_current_direction(*item[0])))[0]


        for x_mov in range(-2, 3):
            for y_mov in range(-2, 3):
                if y_mov == 0 and x_mov == 0:
                    continue
                ady_x = x + x_mov
                ady_y = y + y_mov
                if abs(x_mov) > 1 or abs(y_mov) > 1:
                    if x_mov != 0 and y_mov != 0 and abs(x_mov) != abs(y_mov):
                        continue
                    ady_prev_x = ady_x - 1 if x_mov == 2 else (ady_x + 1 if x_mov == -2 else ady_x)
                    ady_prev_y = ady_y - 1 if y_mov == 2 else (ady_y + 1 if y_mov == -2 else ady_y)
                    if not self.available(ady_prev_x, ady_prev_y):
                        continue
                if self.available(ady_x, ady_y):
                    multiplier = (2 / ( max(abs(x_mov), abs(y_mov)) / 1 ) )
                    if (ady_x, ady_y) in self.adyacent_moves:
                        self.adyacent_moves[(ady_x, ady_y)] += move_score * multiplier
                    else:
                        self.adyacent_moves[(ady_x, ady_y)] = move_score * multiplier
        self.move_log.append(x, y)
        return x, y

    def force_move(self, pos: Tuple[int, int]):
        x, y = pos
        if not (x, y) in self.adyacent_moves:
            move_score = 1
        else:
            move_score = self.adyacent_moves[(x, y)]

        for x_mov in range(-2, 3):
            for y_mov in range(-2, 3):
                if y_mov == 0 and x_mov == 0:
                    continue
                ady_x = x + x_mov
                ady_y = y + y_mov
                if abs(x_mov) > 1 or abs(y_mov) > 1:
                    if x_mov != 0 and y_mov != 0 and abs(x_mov) != abs(y_mov):
                        continue
                    ady_prev_x = ady_x - 1 if x_mov == 2 else (ady_x + 1 if x_mov == -2 else ady_x)
                    ady_prev_y = ady_y - 1 if y_mov == 2 else (ady_y + 1 if y_mov == -2 else ady_y)
                    if not self.available(ady_prev_x, ady_prev_y):
                        continue
                if self.available(ady_x, ady_y):
                    multiplier = 2
                    if (ady_x, ady_y) in self.adyacent_moves:
                        self.adyacent_moves[(ady_x, ady_y)] += move_score * multiplier
                    else:
                        self.adyacent_moves[(ady_x, ady_y)] = move_score * multiplier
        self.move_log.append(x, y)


class EnemyBlocker:
    def block_enemy(self, board):
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == 0:
                    board[i][j] = -1
                    if self._check_4(board, -1):
                        board[i][j] = 0
                        return i * len(board) + j
                    board[i][j] = 0
        return None

    def _check_4(self, board, player=1):
        # Checks four -1 in a row, column or diagonal
        for i in range(0, board.shape[0] - 4):
            for j in range(0, board.shape[1] - 4):
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

class BoardWinner:
    def win_board(self, board, player=1):
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == 0:
                    board[i][j] = 1
                    if self._check_5(board, player):
                        board[i][j] = 0
                        return i * len(board) + j
                    board[i][j] = 0
        return None

    def _check_5(self, board, player=1):
        # Checks four -1 in a row, column or diagonal
        for i in range(0, board.shape[0] - 4):
            for j in range(0, board.shape[1] - 4):
                if (
                    board[i][j] == player
                    and board[i + 1][j + 1] == player
                    and board[i + 2][j + 2] == player
                    and board[i + 3][j + 3] == player
                    and board[i + 4][j + 4] == player
                ):
                    return True
                if (
                    board[i][j] == player
                    and board[i + 1][j] == player
                    and board[i + 2][j] == player
                    and board[i + 3][j] == player
                    and board[i + 4][j] == player
                ):
                    return True
                if (
                    board[i][j] == player
                    and board[i][j + 1] == player
                    and board[i][j + 2] == player
                    and board[i][j + 3] == player
                    and board[i][j + 4] == player
                ):
                    return True
                if (
                    board[i][j + 3] == player
                    and board[i + 1][j + 2] == player
                    and board[i + 2][j + 1] == player
                    and board[i + 3][j] == player
                    and board[i + 4][j] == player
                ):
                    return True
        return False


class GianAgent:
    def __init__(self):
        self.board = None
        self.enemy_blocker = EnemyBlocker()
        self.board_winner = BoardWinner()
        self.move_number = 1

    def action(self, board):
        win_move = self.board_winner.win_board(board)
        if win_move is not None:
            return win_move

        enemy_win_move = self.board_winner.win_board(board, player=-1)
        if enemy_win_move is not None:
            return enemy_win_move

        block_action = self.enemy_blocker.block_enemy(board)
        if block_action is not None:
            return block_action

        if self.board is None:
            self.board = SmartBoard(board)
        else:
            self.board.update(board)

        if self.move_number <= 2:
            middle = (board.shape[0] // 2, board.shape[1] // 2)
            if self.board.available(middle[0], middle[1]):
                x, y = middle[0], middle[1]
                self.board.force_move((x, y))
            elif self.board.available(middle[0] - 2, middle[1]) and self.board.available(middle[0] - 1, middle[1]):
                x, y = middle[0] - 2, middle[1]
                self.board.force_move((x, y))
            elif self.board.available(middle[0], middle[1] + 2) and self.board.available(middle[0], middle[1] + 1):
                x, y = middle[0] , middle[1] + 2
                self.board.force_move((x, y))
            elif self.board.available(middle[0] + 2, middle[1]) and self.board.available(middle[0] + 1, middle[1]):
                x, y = middle[0] + 2, middle[1]
                self.board.force_move((x, y))
            elif self.board.available(middle[0], middle[1] - 2) and self.board.available(middle[0], middle[1] - 1):
                x, y = middle[0], middle[1] - 2
                self.board.force_move((x, y))
            else:
                x, y = self.board.get_best_next_move()
        else:
            x, y = self.board.get_best_next_move()

        self.move_number += 1

        return x * len(board) + y

    def name(self):
        return {"nombre": "Gianmarco", "apellido": "Cafferata", "legajo": -1000}

    def reset(self):
        self.move_number = 1
        self.board = None

    def __str__(self):
        return "🤩**Gian**"