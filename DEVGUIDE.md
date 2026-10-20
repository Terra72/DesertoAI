# A Lazy guide to working on this project

# Running the code
.venv\Scripts\Activate.ps1
python -m deserto

python -m deserto -f -d

python -m deserto.debug

# Running UI
python app.py
http://127.0.0.1:5000/
# DB is initialized on every run (deserto/store/schema.py)
## optional args
-f --force
-d --dry-run
# All pip installs
pip install openai
pip install python-dotenv
pip install feedparser
pip install openai numpy
pip install flask