# RHOC Podcast: Data-Driven Season Plan (Scrape → Index → 10 Scripts)

**Project goal:** Build a repeatable pipeline to gather episode summaries, fan sentiment, and representative comments for *The Real Housewives of Orange County*, organize them into an index, then produce 10 fully written podcast scripts based on the data.

---

## Phase A — Scope & Sources
**Objective:** Define what we’ll gather, where from, and how we’ll use it (ToS‑compliant).

### Episode Catalog
- Canonical season/episode data (title, air date, synopsis) from **TVMaze/TMDb APIs** or scrape **Wikipedia/Fandom** (backup).
- Store: `episodes` table with `{season, episode, title, air_date, synopsis, canonical_urls[]}`.

### Summaries
- Prefer APIs/encyclopedic sources for short synopses (**TVMaze/TMDb/Wikipedia**).

### Fan Sentiment & Comments (priority order)
- **Reddit**: r/BravoRealHousewives, r/realhousewives, episode megathreads (via **PRAW**).
- **YouTube**: Comments from official Bravo clips & popular recap channels (via **YouTube Data API v3**).
- **(Optional) Blogs/Recaps**: Vulture, AV Club, Reality Blurb (headlines & brief excerpts only).

### Legal/Ethical Guardrails
- Respect robots.txt & site ToS; use APIs when offered.
- Store **links + short excerpts** for context; no wholesale copying.
- In podcasts: attribute sources verbally (“per *[source]*”) and paraphrase.

---

## Phase B — Data Pipeline (ETL)
**Stack:** Python (`httpx`/`requests`, `BeautifulSoup4`/`lxml`, **Playwright** for dynamic pages), **PRAW**, **google‑api‑python‑client** (YouTube), **pandas**, **sqlite3**; sentiment via **VADER** + optional transformer (RoBERTa); topic modeling via **BERTopic** or sklearn LDA; **spaCy** (entity tagging).

### Flow
1. **Ingest**
   - Build `episodes` table from catalog.
   - Resolve per‑episode source URLs (Reddit threads, YouTube video IDs).
2. **Collect**
   - For each episode, pull N comments per source with timestamps, upvotes/likes, author (hashed), permalink.
3. **Normalize**
   - De‑dupe; strip HTML; language detect (keep English); persist raw → `/data/raw` (JSONL per source).
4. **Analyze**
   - Sentiment scores (compound, pos/neu/neg) with VADER + model ensemble.
   - Topic clusters & key phrases (per source and overall).
   - Cast entities with spaCy + custom dictionary (Vicki, Tamra, Shannon, Heather, etc.).
5. **Summarize**
   - **Episode Fan Pulse**: top themes, rep quotes (short), sentiment distribution.
   - **Moments Heatmap** (if timestamps available): spikes of engagement.
6. **Persist**
   - SQLite + CSV/JSON exports → `/db/episodes.sqlite`, `/exports/index.csv`, `/exports/comments_sample.csv`.

### Data Model (core tables)
- `episodes(season INT, ep INT, title TEXT, air_date DATE, synopsis TEXT, sources JSON)`
- `comments(episode_key TEXT, source TEXT, ts DATETIME, text TEXT, author_hash TEXT, score INT, permalink TEXT)`
- `analysis(episode_key TEXT, sentiment JSON, topics JSON, entities JSON, engagement JSON)`

---

## Phase C — Organized Index (Deliverables)
**Index fields (per episode):**
- Season, Episode, Air date, Title, Logline/Synopsis
- Sources scraped, # of comments used
- Sentiment snapshot (mean/median/stdev; %pos/%neg)
- Top 5 fan themes (one‑liners)
- 3–5 representative comments (short, source‑linked)
- Cast entities most mentioned

**Formats:**
- `exports/index.csv` (flat), `exports/index.json` (nested per season)
- `db/episodes.sqlite`
- **Optional**: mini **Streamlit** dashboard for browsing/filtering.

---

## Phase D — Editorial Planning from Data
**Goal:** Translate data into a compelling 10‑episode podcast season.

- Select episodes/arcs with highest engagement and strongest themes.
- Standard show segments:
  - **Cold Open** (hook), **Recap**, **Fan Pulse** (what the internet said),
  - **Theme Deep‑Dive**, **Cast Dynamics**, **Receipts Corner** (citations),
  - **Mailbag/Hot Takes**, **Outro/CTA**.

**Draft 10‑Episode Angles (editable):**
1. RHOC origin & why it still hits (data‑driven overview)
2. Most divisive episode of Season X (where the audience split and why)
3. Vicki vs. [Rival]: anatomy of a feud (timeline + sentiment trend)
4. Tamra’s arc: comeback mechanics & audience reaction
5. Shannon’s vulnerability storylines: empathy vs. fatigue in comments
6. Heather Dubrow & status performances: wealth aesthetics, fan takes
7. Iconic group trips: what always sparks drama (trope breakdown)
8. Editing & narrative beats Bravo uses (and fans notice)
9. Fashion, taglines, and memes: what fans reward vs. roast
10. Reunion psychology: conflict resolution or re‑litigation?

---

## Phase E — Script Writing (10 Full Episodes)
**Per episode output (approx. 1,800–2,300 written words):**
- **Cold open** (30–45 sec)
- **Intro & credits** (host names, show identity)
- **Context & recap** (brief, spoiler policy defined)
- **Fan Pulse** (data + short excerpts with source callouts)
- **Theme Deep‑Dive** (cultural/psych dynamics w/ light scholarship)
- **Cast Dynamics** (case examples tied to themes)
- **Mailbag/Hot Takes** (from the corpus)
- **Outro/CTA** (subscribe, socials, next ep tease)

**Exports:** `.md`, `.docx` (if requested), and printer‑friendly `.pdf`.

---

## Phase F — Packaging & DevOps
- **Repo scaffold (GitHub‑ready):**
  - `src/`, `data/`, `exports/`, `notebooks/`, `tests/`, `README.md`, `LICENSE`, `.env.example`, `Makefile`, `requirements.txt`, `Dockerfile`, `run.bat` (Windows).
- **CLI commands:**
  - `python -m src.cli fetch --seasons 18-19`
  - `python -m src.cli analyze --limit 400`
  - `python -m src.cli index --out exports/index.csv`
  - `python -m src.cli write-scripts --plan plan.yaml`
- **Config** via `config.yaml` (sources on/off, limits, time windows).
- **Resilience:** Tenacity for retries; crawl delays; rotating UA; optional proxy.

---

## Defaults & Decisions (can be changed later)
1. **Scope:** Start with latest 2 fully‑aired seasons; expandable.
2. **Sources:** Reddit + YouTube + Wikipedia/API included; IMDb scraping excluded to avoid ToS risk.
3. **Comment caps:** Up to **300 Reddit + 300 YouTube** comments per episode (after filters).
4. **Script voice:** **Two‑host**, witty but kind; PG‑13; minimal profanity.
5. **Episode length:** Target **25 minutes** runtime; write ~2,000 words to leave room for ad‑libs.
6. **Branding:** Placeholder show name & host names; to be swapped later.
7. **Dashboard:** Include small **Streamlit** browser for review.

---

## Next Steps (Section 1 Execution Plan)
1. **Repo scaffold & environment** (requirements, Makefile, Dockerfile, `.env.example`).
2. **Data schema** & SQLite init scripts.
3. **Source adapters:** `catalog`, `reddit`, `youtube`, `wiki` with rate‑limits.
4. **CLI stubs:** `fetch`, `analyze`, `index`, `write-scripts` (no‑op bodies).
5. **Smoke test:** Pull 1 episode, fetch 50 comments, run sentiment, generate a one‑row `index.csv`.
6. **Review w/ you**, then scale to all targeted seasons and start script writing.

---

*Prepared for: RHOC Podcast multi‑phase project (Scrape → Index → Scripts)*
