# A Lazy guide to working on this project

# Running the code
.venv\Scripts\Activate.ps1
python run.py

python run.py -f -d

python -m agent.debugger

# DB is initialized in run but you can manually create it:
python -m db.init_db
## optional args
-f --force
-d --dry-run
# All pip installs
pip install openai
pip install python-dotenv
pip install feedparser
pip install openai numpy