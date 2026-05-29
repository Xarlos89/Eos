# Contributing

Some short guidelines and points on contributing to Eos.

- If you are a collaborator on the repo, create a branch directly and open your PR from it as normal.
- If you are not a collaborator, fork the repo first, push your branch to your fork, then open a PR from your fork against `master`.
- All changes must come via PR to `master`, this requires 1 approval.
- I recommend sticking with `feature/some-feature`, `bugfix/some-bug`, `chore/some-chore` for branch names.

## pre-commit

We use [pre-commit](https://pre-commit.com) to run formatting and linting checks (ruff for formatting + linting, bandit, and a few file hygiene hooks) before each commit.

Install the hooks once after cloning:

```bash
pre-commit install
```

After this, the checks run automatically whenever you `git commit`. Stage your changes with `git add <file>` first; if a hook modifies a file (e.g. ruff reformats it), re-stage it and commit again.

To run the checks manually against everything without committing:

```bash
pre-commit run --all-files
```

## Local development with uv

The bot and API normally run via `docker compose` (see the README). For quicker iteration or debugging you can run them directly on your machine using [uv](https://docs.astral.sh/uv/), a fast Python package manager.

Install `uv`:

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Dependencies are split into two files: `src/api/requirements-api.txt` and `src/bot/requirements-bot.txt`. Create a virtual environment and install whichever service you're working on:

```bash
uv venv                                       # create .venv
source .venv/bin/activate                     # Windows: .venv\Scripts\activate

uv pip install -r src/bot/requirements-bot.txt   # for the bot
uv pip install -r src/api/requirements-api.txt   # for the API
```

You can also install `pre-commit` as a uv-managed tool so it's available without activating a venv:

```bash
uv tool install pre-commit
```

Note: running a service locally still depends on its surroundings — the bot needs the API reachable (`FLASK_URL`), and both need a populated `src/.env`. The easiest setup is to keep Postgres (and optionally the API) running in Docker while you run the service you're editing locally.
