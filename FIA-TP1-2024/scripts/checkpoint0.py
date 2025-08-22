""" NO COMMITEAR CAMBIOS EN ESTE ARCHIVO!"""
"""Test file for checkpoint 0.
tests methods:
    - action
    - name
    - __str__"""

import time
from itertools import permutations

from agents.test_agents.adjacent import AdjacentAgent
from agents.test_agents.anti import AntiAgent
from agents.test_agents.bad import BadAgent
from agents.test_agents.center import CenterAgent
from agents.test_agents.first import FirstAgent
from agents.test_agents.gian import GianAgent
from agents.test_agents.half import HalfAgent
from agents.test_agents.no3inRow import No3inRowAgent
from agents.test_agents.randy import RandomAgent

AGENTS = {
    RandomAgent(),
    FirstAgent(),
    AdjacentAgent(),
    CenterAgent(),
    AntiAgent(),
    No3inRowAgent(),
    HalfAgent(),
}
RENDERED = True

import glob
import importlib
import inspect
import os

for agent_path in os.listdir('scripts/agents'):
    if agent_path == "test_agents":
        continue
    agents_path = 'agents/' + agent_path
    path = "scripts/" + agents_path
    modules = [os.path.basename(f)[:-3] for f in glob.glob(path + "/*.py")
               if not (os.path.basename(f)[0] == '_' or os.path.basename(f)[0] == '.')]
    stripped_path = os.path.relpath(agents_path).replace('/', '.')
    for module in modules:
        mod = importlib.import_module(stripped_path + "." + module)
        for name, obj in inspect.getmembers(mod):
            try:
                if inspect.isclass(obj) and hasattr(obj, "action"):
                    AGENTS.add(obj())
            except Exception:
                continue


import gymnasium as gym
import tqdm
import trueskill
from tournament_utils import print_results

import gomoku_udesa

for agent in AGENTS:
    # test __str__
    agent.notes = ""
    if not hasattr(agent, "__str__"):
        agent.notes += "No __str__ method implemented. "
    else:
        if not isinstance(agent.__str__(), str):
            agent.notes += "__str__ should return a string. "

    # test method name()
    try:
        if not hasattr(agent, "name"):
            if not hasattr(agent, "names"):
                agent.notes += "No name() method implemented. "
            else:
                agent.notes += "rename names() to name(). "
        else:
            if not isinstance(agent.name(), dict):
                agent.notes += "name() should return a dict. "
            else:
                if not agent.name()["legajo"]:
                    agent.notes += "name() should return a dict with legajo. "
    except:
        agent.notes += "agent.name() failed. "

    # test action
    if not hasattr(agent, "action"):
        agent.notes += "No action() method implemented. "

    # test no invalid moves

    SIZE = 9

    env = gym.make(
        "gomoku_udesa/Gomoku-v0",
        render_mode=None,
        max_episode_steps=SIZE * SIZE + 1,
        num_rows=SIZE,
        num_cols=SIZE,
        num_in_row=5,
    )
    obs, _ = env.reset()
    terminated, truncated = False, False
    while not terminated and not truncated:
        num_non_zero = len(obs[obs != 0])
        action = agent.action(obs)
        obs, reward, terminated, truncated, info = env.step(action)
        if num_non_zero == len(obs[obs != 0]):
            agent.notes += "Agent takes invalid moves."
            break

    # test smaller board 3x3
    SIZE = 3
    env = gym.make(
        "gomoku_udesa/Gomoku-v0",
        render_mode=None,
        max_episode_steps=SIZE * SIZE + 1,
        num_rows=SIZE,
        num_cols=SIZE,
        num_in_row=3,
    )
    obs, _ = env.reset()
    terminated, truncated = False, False
    try:
        while not terminated and not truncated:
            action = agent.action(obs)
            if action is None or action > SIZE * SIZE:
                agent.notes += "Agent fails in smaller boards."
                break
            obs, reward, terminated, truncated, info = env.step(action)
    except:
        agent.notes += "Agent fails in smaller boards."

    if agent.notes == "":
        agent.notes = "OK"

# print errors
for agent in AGENTS:
    print(f"{str(agent):30} {agent.notes}")
