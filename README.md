# AutoApply

A single Python script that points a browser-driving LLM agent at Indeed and has it run a job search for you. It uses [browser-use](https://github.com/browser-use/browser-use) to control a real Chromium browser and Google's Gemini 1.5 Pro to decide what to click. The task is written in plain English inside `job_search.py`: open indeed.com, pause 60 seconds so you can sign in by hand, search for "Principal Machine Learning Engineer", filter to remote roles paying $200,000 or more, then save the top 5 titles, companies, and links to a text file.

This is an early prototype. Despite the repo name, it does not submit applications yet. The one script here searches and records results.

## Features

- Browser automation driven by an LLM instead of hard-coded selectors, so the search survives Indeed layout changes better than a scraper would.
- Human-in-the-loop sign-in: the agent waits 60 seconds for you to log into Indeed yourself, which avoids storing credentials anywhere.
- Search criteria, filters, and output instructions live in one plain-English prompt string that you edit directly.
- Async run via `asyncio`, so the agent loop is non-blocking.

## Requirements

- Python 3.11 or newer (`python = "^3.11"`).
- A Google Gemini API key.
- Poetry, or any tool that can install from `pyproject.toml`.
- Dependencies: `browser-use` ^0.1.40, `langchain-google-genai` ^2.1.2, `python-dotenv` ^1.1.0.

`browser-use` drives a Chromium instance through Playwright. If the browser does not launch on first run, install the Playwright browsers (`playwright install chromium`).

## Installation

```bash
git clone https://github.com/espin086/AutoApply.git
cd AutoApply
poetry install
```

Create a `.env` file in the repo root with your key:

```
GEMINI_API_KEY=your_key_here
```

`.env` is gitignored.

## Usage

```bash
poetry run python job_search.py
```

There are no CLI flags. Everything is configured in two places:

| What | Where |
|---|---|
| `GEMINI_API_KEY` | `.env` (read via `python-dotenv`); the script raises `ValueError` if it is missing |
| Job title, filters, result count, output file | the `task=` string inside `main()` in `job_search.py` |
| Model and temperature | the `ChatGoogleGenerativeAI(...)` call: `gemini-1.5-pro`, `temperature=0.2` |

When the run starts, a browser window opens on indeed.com and the agent holds for roughly 60 seconds. Sign in during that window. After that it runs the search and filters on its own. The output file is whatever the agent decides to write, since the prompt asks for "a text file" without naming one.

## Project structure

```
AutoApply/
├── job_search.py    the whole program: loads .env, builds the browser-use Agent with a Gemini LLM, runs it
├── pyproject.toml   Poetry project metadata and the three runtime dependencies
├── poetry.lock      pinned dependency versions
├── LICENSE          MIT
└── .gitignore       standard Python ignores, including .env
```

## How it works

`job_search.py` does four things in order. It calls `load_dotenv()` and reads `GEMINI_API_KEY` from the environment, failing fast if the key is absent. It constructs a `browser_use.Agent` with the multi-step task written as a numbered list of instructions. It hands that agent a `ChatGoogleGenerativeAI` client for `gemini-1.5-pro` at temperature 0.2, low enough to keep the browsing steps predictable. Then `agent.run()` is awaited inside `asyncio.run(main())`.

The agent loop itself lives in `browser-use`: it screenshots the page, sends the state plus the task to Gemini, gets back the next action (click, type, scroll, extract), and executes it against the live browser. Nothing in this repo implements that loop, so behavior tracks whatever `browser-use` 0.1.x does.

## License

MIT. See [LICENSE](LICENSE).
