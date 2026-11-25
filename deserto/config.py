from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "desert.db"
STATE_PATH = BASE_DIR / "memory" / "state.json"
STATE_TEMPLATE_PATH = BASE_DIR / "memory" / "state.template.json"
EXPORT_DIR = BASE_DIR / "data" / "exports"

# Model IDs. Unchanged in Step 0; swapped in Step 2.
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # local, no API key
SUMMARIZE_MODEL = "claude-haiku-5-5"
