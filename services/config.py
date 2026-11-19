"""BIOVA Configuration & Constants
Defines directory paths, color system, and application settings.
"""

from pathlib import Path
import os

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
LABELS_DIR = MODELS_DIR / "labels"
CONTENT_DIR = BASE_DIR / "content"
ASSETS_DIR = BASE_DIR / "assets"
MASCOT_DIR = ASSETS_DIR / "mascot"
ICONS_DIR = ASSETS_DIR / "icons"
IMAGES_DIR = ASSETS_DIR / "images"
THREED_DIR = ASSETS_DIR / "3d"
REFERENCES_DIR = BASE_DIR / "references" / "ui"

# Ensure runtime directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)
LABELS_DIR.mkdir(parents=True, exist_ok=True)
CONTENT_DIR.mkdir(parents=True, exist_ok=True)
(BASE_DIR / ".keras").mkdir(parents=True, exist_ok=True)
(BASE_DIR / ".matplotlib").mkdir(parents=True, exist_ok=True)

# Safe environment settings for Keras & Matplotlib within workspace
os.environ.setdefault("KERAS_HOME", str(BASE_DIR / ".keras"))
os.environ.setdefault("MPLCONFIGDIR", str(BASE_DIR / ".matplotlib"))
os.environ.setdefault("TF_ENABLE_ONEDNN_OPTS", "0")

# Database configuration
DB_PATH = DATA_DIR / "biova.db"

# Color Palette (consistent with design system)
COLOR_BG = "#E5E6E1"
COLOR_CARD = "#EAE9DE"
COLOR_PRIMARY = "#263C2B"
COLOR_SECONDARY = "#416848"
COLOR_HIGHLIGHT = "#CFDFA6"
COLOR_BORDER = "#8BA28B"
COLOR_TEXT = "#263C2B"
COLOR_SUCCESS = "#416848"
COLOR_ERROR = "#A13D2D"
COLOR_WHITE = "#FFFFFF"

# Model paths
ANIMAL_MODEL_PATH = MODELS_DIR / "model_hewan.keras"
ANIMAL_FT_MODEL_PATH = MODELS_DIR / "model_hewan_ft.keras"
ANIMAL_SPECIES_MODEL_PATH = MODELS_DIR / "model_jenis.keras"
PLANT_MODEL_PATH = MODELS_DIR / "model_tumbuhan.keras"
ANIMAL_LABEL_PATH = LABELS_DIR / "label_hewan.json"
PLANT_LABEL_PATH = LABELS_DIR / "label_tumbuhan.json"

# App Info
APP_NAME = "BIOVA"
APP_TITLE = "BIOVA – Belajar dari Alam"
APP_TAGLINE = "Jelajahi Sekitarmu! Temukan, Kenali, & Pelajari."
