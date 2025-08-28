# RHOC Podcast Data Pipeline

This repository contains the scaffolding for a data-driven podcast project based on *The Real Housewives of Orange County*. See `RHOC_Podcast_Project_Plan.md` for the detailed project roadmap.

## Development Setup

1. Create a virtual environment and install dependencies:

   ```bash
   make install
   ```

2. Copy `.env.example` to `.env` and populate API keys.

3. Initialize the SQLite database:

   ```bash
   python -m src.db.init_db
   ```

4. Run tests:

   ```bash
   make test
   ```

## CLI Usage

Placeholder CLI entry points exist under `src/cli`. For example:

```bash
python -m src.cli fetch --help
```
