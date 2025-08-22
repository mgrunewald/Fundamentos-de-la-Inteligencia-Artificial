""" NO COMMITEAR CAMBIOS EN ESTE ARCHIVO!"""
""" 1v1 between two agents """

import time

import gymnasium as gym

# **Import the agents HERE!**
from agents.test_agents.gian import GianAgent
from agents.test_agents.half import HalfAgent
from agents.test_agents.human import HumanAgent
from agents.test_agents.no3inRow import No3inRowAgent
from agents.test_agents.randy import RandomAgent
from agents.GRUNEWALD.grunewaldAgent import grunewaldAgent
# **Add your agents HERE!**
agent1 = grunewaldAgent()
agent2 = HumanAgent()

ROUNDS = 1
SIZE = 11

env = gym.make(
    "gomoku_udesa/Gomoku-v0",
    render_mode="human",
    max_episode_steps=SIZE * SIZE + 1,
    num_rows=SIZE,
    num_cols=SIZE,
    num_in_row=5,
)

board, _ = env.reset()
env.render()
terminated, truncated = False, False
n = 0
while not terminated and not truncated:
    if n % 2 == 0:
        action = agent1.action(board)
        board, reward1, terminated, truncated, info = env.step(action)
    else:
        action = agent2.action(-board)
        board, reward2, terminated, truncated, info = env.step(action)
    n += 1
    #eliminar despues
    print(board)
    env.render()
    time.sleep(0.2)
time.sleep(1)
