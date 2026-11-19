"""BIOVA Educational Description Service
Provides biological facts and descriptive details for recognized animal and plant classes.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from services.config import CONTENT_DIR


def get_catalog() -> Dict[str, Any]:
    """Loads the curated species and class catalog from content/spesies.json."""
    path = CONTENT_DIR / "spesies.json"
    if not path.exists():
        return {"categories": {}}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"categories": {}}


def get_education_info(category: str, class_name: str) -> Optional[Dict[str, Any]]:
    """Retrieves educational details for a detected animal or plant class."""
    catalog = get_catalog()
    cat_data = catalog.get("categories", {}).get(category.lower(), {})
    groups = cat_data.get("groups", {})

    # Case-insensitive match on group key or group name
    for k, v in groups.items():
        if k.lower() == class_name.lower() or v.get("name", "").lower() == class_name.lower():
            return v

    # Fallback to default group if partial match
    for k, v in groups.items():
        if class_name.lower() in k.lower():
            return v

    return None
