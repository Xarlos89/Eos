# Contributing

Some short guidelines and points on contributing to Eos.

- If you are a collaborator on the repo, create a branch directly and open your PR from it as normal.
- If you are not a collaborator, fork the repo first, push your branch to your fork, then open a PR from your fork against `master`.
- All changes must come via PR to `master`, this requires 1 approval.
- I recommend sticking with `feature/some-feature`, `bugfix/some-bug`, `chore/some-chore` for branch names.

## pre-commit

We use [pre-commit](https://pre-commit.com) to run formatting and linting checks (black, isort, flake8, mypy, bandit, and a few file hygiene hooks) before each commit.

Install the hooks once after cloning:

```bash
pre-commit install
```

After this, the checks run automatically whenever you `git commit`. Stage your changes with `git add <file>` first; if a hook modifies a file (e.g. black reformats it), re-stage it and commit again.

To run the checks manually against everything without committing:

```bash
pre-commit run --all-files
```

## Local development with uv

The bot and API normally run via `docker compose` (see the README). For quicker iteration or debugging you can run them directly on your machine using [uv](https://docs.astral.sh/uv/), a fast Python package manager.

You can find the installation instruction for `uv` from [here](https://docs.astral.sh/uv/getting-started/installation/)

The project is split into two workspaces namely:
- `eos-api`: Source for the API backend made with `flask`.
- `eos-bot`: Source for the bot implementation made with `discord.py

`eos-api` workspace is located under `src/api/` and `eos-bot` workspace is located under `src/bot/`

Similarly, dependencies are split into two files: `src/api/pyproject.toml` and `src/bot/pyproject.toml` for the API and Bot source respectively. For the most part you won't be needing to manually edit these files.

### Setting up uv environment

In your project run the following command to setup your environment-

```bash
uv sync
```

Activate your virtual environment for your respective OS-

For Linux / MacOS-
```bash
source .venv/bin/activate
```
For Windows-
```
.venv\Scripts\Activate.ps1  # For Windows PowerShell
.venv\Scripts\activate.bat  # For Windows Command Prompt
```

### Managing dependencies via uv

To add any dependency you must first know which under which workspace you want to add them to (`eos-api` or `eos-bot`).
Once you know that, run the following command to add it to the particular workspace-
```bash
uv add --package <WORKSPACE-NAME> <LIBRARY-NAME>
```

For example if you want to add `Django` to the api workspace, the command will be-
```bash
uv add --package eos-api Django
```

To remove a dependency, you can do so like-
```bash
uv remove --package eos-bot Django
```
And then don't forget to re-sync your dependencies-
```bash
uv sync
```

You can also install `pre-commit` as a uv-managed tool so it's available without activating a venv:

```bash
uv tool install pre-commit
```

Note: running a service locally still depends on its surroundings — the bot needs the API reachable (`FLASK_URL`), and both need a populated `src/.env`. The easiest setup is to keep Postgres (and optionally the API) running in Docker while you run the service you're editing locally.
