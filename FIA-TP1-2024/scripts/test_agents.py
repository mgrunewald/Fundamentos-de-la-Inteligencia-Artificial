""" NO COMMITEAR CAMBIOS EN ESTE ARCHIVO!"""
"""Test file for Agents"""


def timeout_handler():
    raise TimeoutError()


import time
from itertools import permutations
from threading import Timer

import gymnasium as gym
import tqdm
import trueskill
from tournament_utils import (
    evaluate_agent_moves,
    evaluate_code_quality,
    print_disqualified_agents,
    print_results,
    set_seeds,
    verbose_competition_match,
)

import gomoku_udesa

set_seeds()

from agents.test_agents.adjacent import AdjacentAgent
from agents.test_agents.anti import AntiAgent
from agents.test_agents.bad import BadAgent
from agents.test_agents.center import CenterAgent
from agents.test_agents.first import FirstAgent
from agents.test_agents.gian import GianAgent
from agents.test_agents.half import HalfAgent
from agents.test_agents.human import HumanAgent
from agents.test_agents.no3inRow import No3inRowAgent
from agents.test_agents.randy import RandomAgent

AGENTS = [
    RandomAgent(),
    # FirstAgent(),
    # AdjacentAgent(),
    # CenterAgent(),
    # AntiAgent(),
    # No3inRowAgent(),
    # HalfAgent(),
    # BadAgent(),
    # GianAgent(),
    GianAgent(),  # Replace this with your agent
]
RENDERED = True

timer = Timer(2.0, timeout_handler)

print("Evaluating agents coding quality")
evaluate_code_quality(AGENTS)

print("Evaluating agents moves")
evaluate_agent_moves(AGENTS)


for agent in AGENTS:
    if agent.notes == "":
        agent.notes = "OK"

ROUNDS = 1
SIZE = 11

env = gym.make(
    "gomoku_udesa/Gomoku-v0",
    render_mode="human" if RENDERED else None,
    max_episode_steps=SIZE * SIZE + 1,
    num_rows=SIZE,
    num_cols=SIZE,
    num_in_row=5,
)

for agent in AGENTS:
    if agent.notes != "OK":
        continue
    agent.rating = trueskill.Rating()

print("Start competition")
for agent1, agent2 in tqdm.tqdm(list(permutations(AGENTS, 2)) * ROUNDS):
    verbose_competition_match(agent1, agent2, env, 5, RENDERED)

disqualified_agents = []
working_agents = []

for agent in AGENTS:
    if agent.notes != "OK":
        disqualified_agents.append(agent)
    else:
        working_agents.append(agent)
print_results(working_agents)
print_disqualified_agents(disqualified_agents)
