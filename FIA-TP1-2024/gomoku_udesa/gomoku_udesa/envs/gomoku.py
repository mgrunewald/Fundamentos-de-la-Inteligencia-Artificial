import gymnasium as gym
import numpy as np
import pygame
from gymnasium import spaces


class GomokuEnv(gym.Env):
    metadata = {"render_modes": ["human", "console"], "render_fps": float("inf")}
    cell_size = 30
    margin = 30

    def __init__(self, render_mode=None, num_rows=15, num_cols=15, num_in_row=5):
        super().__init__()
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.num_in_row = num_in_row
        self.board = np.zeros((num_rows, num_cols), dtype=int)
        self.current_player = 1
        self.action_space = spaces.Discrete(num_rows * num_cols)
        self.observation_space = spaces.Box(
            low=-1, high=1, shape=(num_rows, num_cols), dtype=int
        )
        self.render_mode = render_mode
        self.last_move = None

        if self.render_mode == "human":
            pygame.init()
            self.window_width = self.num_cols * self.cell_size + self.margin
            self.window_height = self.num_rows * self.cell_size + self.margin
            self.screen = pygame.display.set_mode(
                (self.window_width, self.window_height)
            )
            pygame.display.set_caption("Gomoku")

    def reset(self, seed=None, options=None):
        if options is not None and "board" in options:
            self.board = options["board"]
        else:
            self.board = np.zeros((self.num_rows, self.num_cols), dtype=int)
        self.current_player = 1
        self.last_move = None
        return self.board.copy(), {}

    def step(self, action):
        """Execute one step in the environment given an action."""
        row = action // self.num_cols
        col = action % self.num_cols
        self.last_move = (row, col)

        # To avoid pygame giving non-responding errors
        if self.render_mode == "human":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

        if self.board[row][col] != 0:
            self.current_player = -self.current_player
            return self.board.copy(), 0, False, False, {}

        self.board[row][col] = self.current_player
        done = self.check_win(row, col)

        reward = 1 if done else 0
        info = {}

        if done:
            info["outcome"] = "win"
        elif self.check_draw():
            done = True
            reward = 0
            info["outcome"] = "draw"

        self.current_player = -self.current_player
        return self.board.copy(), reward, False, done, info

    def render(self, mode=None):
        if self.render_mode == "human":
            self._render_human()
        elif self.render_mode == "console":
            self._render_console()

    def _render_human(self):
        self.screen.fill((155, 110, 80))
        # Draw vertical lines
        for i in range(self.num_cols + 1):
            pygame.draw.line(
                self.screen,
                (115, 60, 40),
                (self.margin + i * self.cell_size - 1, self.margin),
                (
                    self.margin + i * self.cell_size - 1,
                    self.window_height - self.margin,
                ),
                2,
            )
        # Draw horizontal lines
        for i in range(self.num_rows + 1):
            pygame.draw.line(
                self.screen,
                (135, 80, 60),
                (self.margin, self.margin + i * self.cell_size - 1),
                (self.window_width - self.margin, self.margin + i * self.cell_size - 1),
                2,
            )

        # Draw numbers and letters
        for i in range(self.num_cols):
            font = pygame.font.SysFont("Arial", 14)
            text = font.render(str(i + 1), True, (40, 40, 40))
            self.screen.blit(
                text,
                (
                    self.margin + i * self.cell_size - 6,
                    self.margin // 2 - 6,
                ),
            )
            text = font.render(str(i + 1), True, (40, 40, 40))
            self.screen.blit(
                text,
                (
                    self.margin // 2 - 6,
                    self.margin + i * self.cell_size - 6,
                ),
            )

        # Draw the last move
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if self.board[row][col] == 1:
                    color = (40, 40, 40)  # black for player 1
                    pygame.draw.circle(
                        self.screen,
                        color,
                        (
                            self.margin + col * self.cell_size,
                            self.margin + row * self.cell_size,
                        ),
                        self.cell_size // 2.2,
                    )
                elif self.board[row][col] == -1:
                    color = (225, 225, 225)  # white for player 2
                    pygame.draw.circle(
                        self.screen,
                        color,
                        (
                            self.margin + col * self.cell_size,
                            self.margin + row * self.cell_size,
                        ),
                        self.cell_size // 2.2,
                    )
                if self.last_move == (row, col):
                    pygame.draw.circle(
                        self.screen,
                        (80, 80, 80) + np.random.randint(0, 155, 3),
                        (
                            self.margin + col * self.cell_size,
                            self.margin + row * self.cell_size,
                        ),
                        self.cell_size // 4,
                    )

        pygame.display.flip()

    def _render_console(self):
        """Render the current state of the game in the console."""
        print(f"Current player: {self.current_player}")
        for row in self.board:
            for cell in row:
                symbol = "." if cell == 0 else "X" if cell == 1 else "O"
                print(symbol, end=" ")
            print()

    def check_win(self, row, col):
        """Check if the last move at position (row, col) results in a win."""
        directions = [(1, 0), (0, 1), (1, -1), (1, 1)]

        for dx, dy in directions:
            count = 1

            for direction in [-1, 1]:
                cur_row = row
                cur_col = col

                while True:
                    cur_row += direction * dx
                    cur_col += direction * dy

                    if not (
                        0 <= cur_row < self.num_rows and 0 <= cur_col < self.num_cols
                    ):
                        break

                    if self.board[cur_row][cur_col] == self.current_player:
                        count += 1
                    else:
                        break

            if count >= self.num_in_row:
                return True

        return False

    def check_draw(self):
        """Check if the game is a draw."""
        return np.count_nonzero(self.board) == self.num_rows * self.num_cols

    def close(self):
        if self.render_mode == "human":
            pygame.quit()
