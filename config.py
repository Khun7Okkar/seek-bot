# config.py

# Job Search Criteria
JOB_ROLES = [
    "Site Engineer",
    "Project Engineer",
    "Project Manager",
    "Construction Manager"
]

INDUSTRY = "Construction, Civil Engineering"
LOCATION = "Auckland, New Zealand"

# Target Sites
# We can toggle these on/off
SITES = {
    "SEEK": True,
    "LINKEDIN": True
}

# LLM Settings (LM Studio)
LLM_API_BASE = "http://localhost:1234/v1"
LLM_API_KEY = "lm-studio"  # Usually not needed for local, but good practice to have a placeholder
LLM_MODEL = "local-model" # Placeholder, LM Studio often ignores this or you pick in UI

# Browser / Stealth Settings
HEADLESS_MODE = False  # Set to False to see what's happening (recommended for debugging/stealth)
MIN_DELAY = 2
MAX_DELAY = 5
SCROLL_PAUSE_TIME = 1.5
PAGES_TO_SCRAPE = 3

# Output Settings
# Output Settings
DATA_DIR = "data"

# User Files
CV_FILENAME = "Username - CV.pdf"
TEMPLATE_FILENAME = "Username - Cover Letter Format.docx"
