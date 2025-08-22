from gymnasium.envs.registration import register

register(
    id="gomoku_udesa/Gomoku-v0",
    entry_point="gomoku_udesa.envs:GomokuEnv",
)
