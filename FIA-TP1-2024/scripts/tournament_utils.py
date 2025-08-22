import logging
import os
import random
import sys
import time

import gymnasium as gym
import numpy as np
import pandas as pd
import tqdm
import trueskill
from agents.test_agents.randy import RandomAgent


def set_seeds():
    hashseed = os.getenv("PYTHONHASHSEED")
    if not hashseed:
        os.environ["PYTHONHASHSEED"] = "0"
        os.execv(sys.executable, [sys.executable] + sys.argv)
    random.seed(42)
    np.random.seed(42)


class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, "w")

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


def print_full_table(agents):
    print("Full table:")
    print(
        f"|{'Legajo':9}|{'Agent':32}|{'Rating (μ ± σ)':14}|{'Iteration time':17}|{'Notes':30}|"
    )  # noqa
    print(f"|{'-'*9}|{'-'*32}|{'-'*14}|{'-'*17}|{'-'*30}|")
    for agent in sorted(
        agents, key=lambda x: x.rating.mu - 3 * x.rating.sigma, reverse=True
    ):
        try:
            legajo = (
                str(agent.name()["legajo"])
                if hasattr(agent, "name")
                and isinstance(agent.name(), dict)
                and "legajo" in agent.name()
                else "-"
            )
            print(
                f"|{legajo:9}|{str(agent):32}|{agent.rating.mu:6.2f} ± {agent.rating.sigma:5.2f}|{str(agent.time*1e3)[:14]:14} ms|{agent.notes:30}|"
            )
        except Exception:
            continue


def print_full_final_table(agents):
    print("Full table:")
    results = []
    for agent in sorted(
        agents, key=lambda x: x.rating.mu - 3 * x.rating.sigma, reverse=True
    ):
        if agent.notes != "OK":
            continue
        try:
            legajo = (
                str(agent.name()["legajo"])
                if hasattr(agent, "name")
                and isinstance(agent.name(), dict)
                and "legajo" in agent.name()
                else "-"
            )
            results.append(
                {
                    "Legajo": legajo,
                    "Best Agent": str(agent),
                    "Rating (μ ± σ)": f"{agent.rating.mu:6.2f} ± {agent.rating.sigma:5.2f}",
                    "Iteration time": f"{str(agent.time * 1e3)[:14]:14} ms",
                    "Errors": "{:.2%}".format(agent.errors / agent.matches),
                    "Timeouts": "{:.2%}".format(agent.timeouts / agent.matches),
                }
            )
        except Exception:
            continue
    results = pd.DataFrame(results)
    print(results.to_markdown())


def print_results(agents):
    print("Results for best agents:")
    results = []
    for agent in sorted(
        agents, key=lambda x: x.rating.mu - 3 * x.rating.sigma, reverse=True
    ):
        try:
            legajo = (
                str(agent.name()["legajo"])
                if hasattr(agent, "name")
                and isinstance(agent.name(), dict)
                and "legajo" in agent.name()
                else "-"
            )
            results.append(
                {
                    "Legajo": legajo,
                    "Best Agent": str(agent),
                    "Rating (μ ± σ)": f"{agent.rating.mu:6.2f} ± {agent.rating.sigma:5.2f}",
                    "Iteration time": f"{str(agent.time * 1e3)[:14]:14} ms",
                    "Notes": agent.notes,
                }
            )
        except Exception:
            continue
    results = pd.DataFrame(results)
    results = results.drop_duplicates("Legajo", keep="first").reset_index(drop=True)
    print(results.to_markdown())


def print_final_results(agents):
    print("Results for best agents:")
    results = []
    for agent in sorted(
        agents, key=lambda x: x.rating.mu - 3 * x.rating.sigma, reverse=True
    ):
        try:
            legajo = (
                str(agent.name()["legajo"])
                if hasattr(agent, "name")
                and isinstance(agent.name(), dict)
                and "legajo" in agent.name()
                else "-"
            )
            results.append(
                {
                    "Legajo": legajo,
                    "Best Agent": str(agent),
                    "Rating (μ ± σ)": f"{agent.rating.mu:6.2f} ± {agent.rating.sigma:5.2f}",
                    "Iteration time": f"{str(agent.time * 1e3)[:14]:14} ms",
                    "Errors": "{:.2%}".format(agent.errors / agent.matches),
                    "Timeouts": "{:.2%}".format(agent.timeouts / agent.matches),
                }
            )
        except Exception:
            continue
    results = pd.DataFrame(results)
    results = results.drop_duplicates("Legajo", keep="first").reset_index(drop=True)
    print(results.to_markdown())


def print_disqualified_agents(agents):
    print("Disqualified Agents:")
    print(f"|{'Legajo':9}|{'Agent':32}|{'Notes':30}|")  # noqa
    print(f"|{'-'*9}|{'-'*32}|{'-'*30}|")
    for agent in agents:
        try:
            legajo = (
                str(agent.name()["legajo"])
                if hasattr(agent, "name")
                and isinstance(agent.name(), dict)
                and "legajo" in agent.name()
                else "-"
            )
            print(f"|{legajo:9}|{str(agent):32}|{agent.notes:30}|")
        except Exception:
            continue


def evaluate_agent_moves(agents):
    random_agent = RandomAgent()

    for agent in tqdm.tqdm(agents):
        if agent.notes != "":
            continue
        if hasattr(agent, "reset"):
            agent.reset()
        SIZE = 5

        env = gym.make(
            "gomoku_udesa/Gomoku-v0",
            render_mode=None,
            max_episode_steps=SIZE * SIZE + 1,
            num_rows=SIZE,
            num_cols=SIZE,
            num_in_row=3,
        )
        board, _ = env.reset()
        terminated, truncated = False, False
        n = 0
        with HiddenPrints():
            while not terminated and not truncated:
                if n % 2 == 0:
                    num_non_zero = len(board[board != 0])
                    try:
                        start = time.perf_counter()
                        action = agent.action(board)
                        time_elapsed = time.perf_counter() - start
                        board, reward, terminated, truncated, info = env.step(action)
                    except Exception as e:
                        agent.notes += f"Exception {e} while running"
                        break
                    if time_elapsed > 5:
                        agent.notes += "Agent too slow in smaller board"
                        break
                    if num_non_zero == len(board[board != 0]):
                        agent.notes += "Agent takes invalid moves."
                        break
                else:
                    action = random_agent.action(-board)
                    board, _, _, _, _ = env.step(action)
                n += 1

        # test again with the opponent starting
        n = 0
        if hasattr(agent, "reset"):
            agent.reset()
        SIZE = 5
        env = gym.make(
            "gomoku_udesa/Gomoku-v0",
            render_mode=None,
            max_episode_steps=SIZE * SIZE + 1,
            num_rows=SIZE,
            num_cols=SIZE,
            num_in_row=3,
        )
        board, _ = env.reset()
        terminated, truncated = False, False
        with HiddenPrints():
            while not terminated and not truncated:
                if n % 2 == 0:
                    action = random_agent.action(board)
                    board, _, _, _, _ = env.step(action)
                else:
                    try:
                        start = time.perf_counter()
                        action = agent.action(-board)
                        time_elapsed = time.perf_counter() - start
                        board, reward, terminated, truncated, info = env.step(action)
                    except Exception as e:
                        agent.notes += (
                            f"Exception {e} while running when opponent starts"
                        )
                        break
                    if time_elapsed > 5:
                        agent.notes += "Agent too slow in smaller board"
                        break
                    if action is None or action > SIZE * SIZE:
                        agent.notes += "Agent takes invalid moves."
                        break

                n += 1


def evaluate_code_quality(agents):
    for agent in tqdm.tqdm(agents):
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

        try:
            int(agent.name()["legajo"])
        except Exception:
            agent.notes += "The legajo is not numeric"


def verbose_competition_match(agent1, agent2, env, max_time_allowed, rendered):
    if agent1.notes != "OK" or agent2.notes != "OK":
        return
    if hasattr(agent1, "reset"):
        agent1.reset()
    if hasattr(agent2, "reset"):
        agent2.reset()
    board, _ = env.reset()
    terminated, truncated = False, False
    time1, time2, n = 0, 0, 0
    reward1, reward2 = 0, 0
    while not terminated and not truncated and len(board[board == 0]) > 0:
        if n % 2 == 0:
            try:
                start = time.perf_counter()
                action = agent1.action(board)
                delta = time.perf_counter() - start
                time1 += delta
            except Exception as e:
                agent1.notes = (
                    f"During Competition: Exception {e} while running. "
                    f"This happened while playing with {agent2.name()}"
                )
                logging.exception(
                    f"Error running agent {agent1.name()} against {agent2.name()} while the board is {board}"
                )
                break
            if delta > max_time_allowed:
                agent1.notes = f"During Competition: Too slow"
                break
            try:
                board, reward1, terminated, truncated, info = env.step(action)
            except Exception as e:
                agent1.notes = (
                    f"During Competition: Exception {e} while running. "
                    f"This happened while playing with {agent2.name()}"
                )
                logging.exception(
                    f"Error running agent {agent1.name()} against {agent2.name()} while the board is {board}"
                )
                break
        else:
            try:
                start = time.perf_counter()
                action = agent2.action(-board)
                delta = time.perf_counter() - start
                time2 += delta
            except Exception as e:
                agent2.notes = (
                    f"During Competition: Exception {e} in the agent code while running. "
                    f"This happened while playing with {agent1.name()}"
                )
                logging.exception(
                    f"Error running agent {agent2.name()} against {agent1.name()} while the board is {board}"
                )
                break
            if delta > max_time_allowed:
                agent2.notes = f"During Competition: Too slow"
                break
            try:
                board, reward2, terminated, truncated, info = env.step(action)
            except Exception as e:
                agent2.notes = (
                    f"During Competition: Exception {e} while running in the . "
                    f"This happened while playing with {agent1.name()}"
                )
                logging.exception(
                    f"Error running agent {agent2.name()} against {agent1.name()} while the board is {board}"
                )
                break
        n += 1
        if rendered:
            env.render()

    agent1.time = time1 / (max(n, 1) / 2)
    agent2.time = time2 / (max(n, 1) / 2)

    if reward1 == 1:
        agent1.rating, agent2.rating = trueskill.rate_1vs1(agent1.rating, agent2.rating)
    elif reward2 == 1:
        agent2.rating, agent1.rating = trueskill.rate_1vs1(agent2.rating, agent1.rating)
    else:
        agent1.rating, agent2.rating = trueskill.rate_1vs1(
            agent1.rating, agent2.rating, drawn=True
        )


def reward_win(winner, looser):
    winner.rating, looser.rating = trueskill.rate_1vs1(winner.rating, looser.rating)


def competition_match(agent1, agent2, env, max_time_allowed, rendered):
    if agent1.notes != "OK" or agent2.notes != "OK":
        return
    agent1.matches += 1
    agent2.matches += 1
    with HiddenPrints():
        if hasattr(agent1, "reset"):
            agent1.reset()
        if hasattr(agent2, "reset"):
            agent2.reset()
        board, _ = env.reset()
        terminated, truncated = False, False
        time1, time2, n = 0, 0, 0
        reward1, reward2 = 0, 0
        while not terminated and not truncated and len(board[board == 0]) > 0:
            if n % 2 == 0:
                try:
                    start = time.perf_counter()
                    action = agent1.action(board)
                    delta = time.perf_counter() - start
                    time1 += delta
                except Exception as e:
                    agent1.errors += 1
                    logging.exception(
                        f"Error running agent {agent1.name()} against {agent2.name()} while the board is {board}"
                    )
                    return reward_win(agent2, agent1)
                if delta > max_time_allowed:
                    agent1.timeouts += 1
                    return reward_win(agent2, agent1)
                try:
                    board, reward1, terminated, truncated, info = env.step(action)
                except Exception as e:
                    agent1.errors += 1
                    logging.exception(
                        f"Error running agent {agent1.name()} against {agent2.name()} while the board is {board}"
                    )
                    return reward_win(agent2, agent1)
            else:
                try:
                    start = time.perf_counter()
                    action = agent2.action(-board)
                    delta = time.perf_counter() - start
                    time2 += delta
                except Exception as e:
                    agent2.errors += 1
                    logging.exception(
                        f"Error running agent {agent2.name()} against {agent1.name()} while the board is {board}"
                    )
                    return reward_win(agent1, agent2)
                if delta > max_time_allowed:
                    agent2.timeouts += 1
                    return reward_win(agent1, agent2)
                try:
                    board, reward2, terminated, truncated, info = env.step(action)
                except Exception as e:
                    agent2.errors += 1
                    logging.exception(
                        f"Error running agent {agent2.name()} against {agent1.name()} while the board is {board}"
                    )
                    return reward_win(agent1, agent2)
            n += 1
            if rendered:
                env.render()

        agent1.time = time1 / (max(n, 1) / 2)
        agent2.time = time2 / (max(n, 1) / 2)

        if reward1 == 1:
            reward_win(agent1, agent2)
        elif reward2 == 1:
            reward_win(agent2, agent1)
        else:
            agent1.rating, agent2.rating = trueskill.rate_1vs1(
                agent1.rating, agent2.rating, drawn=True
            )
