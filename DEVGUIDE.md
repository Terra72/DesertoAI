# A Lazy guide to working on this project

# Running the code
.venv\Scripts\Activate.ps1
python -m deserto

python -m deserto -f -d

python -m deserto.debug

# Running UI
python -m deserto.fixture   # load eval-set fixture (offline)
python app.py
http://127.0.0.1:5000/
# DB is initialized on every run (deserto/store/schema.py)
## optional args
-f --force
-d --dry-run
# Weekly scrape (GitHub Action, Mondays 06:00 UTC)
# Needs repo secret OPENAI_API_KEY. Run manually: Actions > Weekly scrape > Run workflow
# Commits new events to data/exports/events-<year>-W<week>.jsonl
python -m deserto.weekly   # same thing locally, writes data/exports

# All pip installs
pip install openai
pip install python-dotenv
pip install feedparser
pip install openai numpy
pip install flask