# TP1 - Go-moku

## [Ver Consigna](TP1-Go-moku.md)

## Installing

```bash
# 1-
#Fork the repo into your account
# 2-
git clone https://github.com/YOUR_ACCOUNT/FIA-TP1.git
# 3-
cd TP1/gomoku_udesa
# 4-
pip install -e .
```

## Usage

Put your agents inside the `gomoku_udesa/agents/SURNAME` folder.
Then import them in one of the following scripts:

- `1v1.py` for a simple 1v1 game (you can play against yourself using `HumanAgent`)
- `test_agents.py` for a tournament between many agents and additional agent validations

Before making a submission, make sure your agent is compatible with the following scripts, no need to modify these, the agent imports are automatic:

- `checkpoint0.py` will be used to test your agent at checkpoint 0
- `swiss_tournament.py` will be used to test your agents final performance

## Bugs and Issues

Please report any bugs or issues with the engine.
PRs to add tests or fix bugs are welcome.

## Board

![board_image](assets/board.png "Board")
