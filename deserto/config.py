from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "desert.db"
STATE_PATH = BASE_DIR / "memory" / "state.json"
STATE_TEMPLATE_PATH = BASE_DIR / "memory" / "state.template.json"

# Model IDs. Unchanged in Step 0; swapped in Step 2.
EMBEDDING_MODEL = "text-embedding-3-small"
SUMMARIZE_MODEL = "gpt-4o-mini"
