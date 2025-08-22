import gomoku_udesa
import numpy as np
import random
import time
import math

class grunewaldAgent:
    
    def __init__(self):
        self.nombre = "Martina"
        self.apellido = "Grünewald"
        self.legajo = "34582"
        self.agentName = "CaroPardiaco🎀"

    def action(self, board):
        size = len(board[0])
        game = BoardGame() 
        center = size // 2

        turn = game.count_total_pieces(board)

        if turn <= 1: 
            if board[center][center] == 0:
                return center * size + center
            else: 
                return center * size + center + 1
                  
        if turn >= 7:
            win_or_block = game.forced_to_play(board, player=1)
            if win_or_block:
                return win_or_block[0] * size + win_or_block[1]

        x, y = game.find_best_move(board, depth=6, player=1)
        
        jugada = x * size + y
    
        if game.is_valid_move(x, y, board):
            return jugada
        else:
            legal_moves = game.find_legal_moves(board)
            if legal_moves:
                random_move = random.choice(legal_moves)
                return random_move[0] * size + random_move[1]
            else: 
                return -1

    def name(self):
        return {'nombre': self.nombre, 'apellido': self.apellido, 'legajo': self.legajo}

    def __str__(self):
        return self.agentName

class BoardGame:
    def __init__(self):
        self.visited_boards = set()

    def is_valid_move(self, i, j, board):
        if (i, j) in self.find_legal_moves(board):
            return True
        else:
            return False
        
    def find_legal_moves(self, board):
        legal_moves = []
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 0:
                    legal_moves.append((i, j))
        return legal_moves
    
    def count_total_pieces(self, board):
        flat_board = np.array(board).flatten()
        total = np.sum(np.square(flat_board))
        return total

    def move_evaluation(self, board, player, move):
        patterns_6 = {
            (0, 1, 1, 1, 1, 0) : 800,
            (0, -1, -1, -1, -1, 0) : -800, 
            (0, 1, -1, -1, -1, 0) : 600,
            (0, 0, -1, -1, -1, 1) : 600,
            (0, -1, -1, -1, 1, 0) : 600,
            (1, -1, -1, -1, 0, 0) : 600,
            (0, -1, 1, -1, -1, 0) : 600,
            (0, -1, -1, 1, -1, 0) : 600,
            }
        
        patterns_5 = {
            (1, 1, 1, 1, 1) : 1000,
            (-1, -1, -1, -1, -1) : -1000,

            (1, -1, -1, -1, -1) : 900,
            (-1, 1, -1, -1, -1) : 900,
            (-1, -1, 1, -1, -1) : 900,
            (-1, -1, -1, 1, -1) : 900,
            (-1, -1, -1, -1, 1) : 900,

            (1, -1, -1, -1, 1) : 600,

            (0, 1, 1, 1, 1) : 700, 
            (1, 0, 1, 1, 1) : 700,
            (1, 1, 0, 1, 1) : 700,
            (1, 1, 1, 0, 1) : 700,
            (1, 1, 1, 1, 0) : 700,

            (0, -1, -1, -1, -1) : -600,
            (-1, 0, -1, -1, -1) : -600,
            (-1, -1, 0, -1, -1) : -600,
            (-1, -1, -1, 0, -1) : -600,
            (-1, -1, -1, -1, 0) : -600, 
            
            (1, 1, 1, 0, 0) : 300,
            (0, 1, 1, 1, 0) : 350,
            (0, 0, 1, 1, 1) : 300,

            (1, 1, 0, 0, 0) : 200,
            (0, 1, 1, 0, 0) : 250,
            (0, 0, 1, 1, 0) : 250,
            (0, 0, 0, 1, 1) : 200,            
            
            }
       
        patterns_3 = {
            (1, 1, 1) : 150,
            }
        
        patterns_2 = {
            (-1, -1) : -50,
            (1, 1) : 50, }
        
        max_score = -1001
        size = len(board)
        i, j = move
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        new_board = self.make_move(board, move, player)

        for length, patterns in [(6, patterns_6),(5, patterns_5), (3, patterns_3), (2, patterns_2)]: 
            for di, dj in directions:
                for delta in range(-length + 1, 1):
                    sequence = []
                    for offset in range(length):
                        ni, nj = i + (delta + offset) * di, j + (delta + offset) * dj
                        if 0 <= ni < size and 0 <= nj < size:
                            sequence.append(new_board[ni][nj])
                    for pattern, score in patterns.items():
                        if tuple(sequence) == pattern:
                            if max_score == 1000: 
                                return 1000
                            max_score = max(max_score, score)

        return max_score        
    
    def board_evaluation(self, board, player):
        legal_moves = self.find_legal_moves(board)
        scores = np.zeros(len(legal_moves))
        for i, move in enumerate(legal_moves):
            scores[i] = self.move_evaluation(board, player, move)
        max_score = np.max(scores)
        return max_score

    def game_over(self, board):
        total_pieces = np.sum(np.abs(board))
        board_size = len(board[0]) ** 2
        return total_pieces == board_size

    def make_move(self, board, move, player):
        new_board = np.copy(board)
        i, j = move
        new_board[i][j] = player
        return new_board
            
    def ordenar_movimientos_a_analizar(self, board, player):
        legal_moves = self.find_legal_moves(board)
        evaluations = np.array([self.move_evaluation(self.make_move(board, move, player), player, move) for move in legal_moves])
        sorted_legal_moves = [move for _, move in sorted(zip(evaluations, legal_moves), reverse=True)]
        return sorted_legal_moves

    def find_best_move(self, board, depth, player):
        sorted_legal_moves = self.ordenar_movimientos_a_analizar(board, player)
        
        if len(board) > 11:
            pieces_on_board = self.count_total_pieces(board)
            if len(board) ** 2 - pieces_on_board > 100:
                relevant_moves_amount = math.ceil(len(sorted_legal_moves) * 2 // 9)
            else:
                relevant_moves_amount = len(sorted_legal_moves)
            sorted_legal_moves = sorted_legal_moves[:relevant_moves_amount]

        for d in range(1, depth + 1):
            _, best_board = self.minimax(board, d, -math.inf, math.inf, True, player, sorted_legal_moves)
            if best_board is not None:
                return self.get_move_difference(board, best_board)
        return None
    

    def minimax(self, board, depth, alpha, beta, maximizing, player, sorted_legal_moves):
        self.visited_boards.add(tuple(map(tuple, board.tolist())))
        if depth == 0 or self.game_over(board):
            board_value = self.board_evaluation(board, player)
            if board_value is not None:
                return board_value, board
            else:
                some_valid_random_move = random.choice(sorted_legal_moves)
                not_the_best_board_but_a_valid_one = self.make_move(board, some_valid_random_move, player)
                return 0, not_the_best_board_but_a_valid_one

        occupied_positions = set()
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] != 0:
                    occupied_positions.add((i, j))

        if maximizing:
            value = -math.inf
            for move in sorted_legal_moves:
                if move in occupied_positions:  
                    continue
                new_board = self.make_move(board, move, player)
                board_tuple = tuple(map(tuple, new_board.tolist()))
                if board_tuple in self.visited_boards:
                    continue  
                new_value, _ = self.minimax(new_board, depth - 1, alpha, beta, False, -player, sorted_legal_moves)
                if new_value > value:
                    value = new_value
                    best_board = new_board
                alpha = max(alpha, value)
                if value >= beta:
                    break
            return value, best_board
        else:
            value = math.inf
            for move in sorted_legal_moves:
                if move in occupied_positions: 
                    continue
                new_board = self.make_move(board, move, player)
                board_tuple = tuple(map(tuple, new_board.tolist())) 
                if board_tuple in self.visited_boards:
                    continue 
                new_value, _ = self.minimax(new_board, depth - 1, alpha, beta, True, player, sorted_legal_moves)
                if new_value < value:
                    value = new_value
                    best_board = new_board
                beta = min(value, beta)
                if value <= alpha:
                    break
            return value, best_board

    def get_move_difference(self, board, best_board):
        difference = np.where(board != best_board)
        if difference[0].size > 0:
            return difference[0][0], difference[1][0]
        else:
            return None
        
    
    def forced_to_play(self, board, player):
        legal_moves = self.find_legal_moves(board)
        if len(legal_moves) == 1:
            coordinates = legal_moves[0]
            return coordinates[0], coordinates[1]
        
        size = len(board)
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for i in range(size):
            for j in range(size):
                if board[i][j] == 0:
                    for di, dj in directions:
                        sequence = []
                        for delta in range(-3, 2):
                            ni, nj = i + delta * di, j + delta * dj
                            if 0 <= ni < size and 0 <= nj < size:
                                sequence.append(board[ni][nj])
                            else:
                                sequence = []
                                break
                        if len(sequence) == 5 and sequence.count(player) == 4 and sequence.count(0) == 1:
                            return i, j
                        if len(sequence) == 5 and sequence.count(-player) == 4 and sequence.count(0) == 1:
                            return i, j
        return None
    