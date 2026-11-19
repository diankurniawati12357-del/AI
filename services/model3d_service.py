"""BIOVA 3D Model Mapping Service
Maps identified flora and fauna classes to corresponding 3D .glb assets with existence validation.
"""

from pathlib import Path
from typing import Dict, Any, Optional
from services.config import THREED_DIR
from services.edukasi_service import get_education_info


def get_model3d_info(category: str, class_name: str) -> Dict[str, Any]:
    """Retrieves 3D model path and animation metadata for an identified object.
    Never pretends an asset exists if it is not physically on disk.
    """
    category = category.lower()
    subfolder = "hewan" if category == "hewan" else "tumbuhan"
    folder_path = THREED_DIR / subfolder

    edu = get_education_info(category, class_name)
    model_filename = edu.get("model_3d_file", f"{class_name.lower()}.glb") if edu else f"{class_name.lower()}.glb"

    model_path = folder_path / model_filename
    exists = model_path.exists()

    # Animation configuration map
    animation_map = {
        "bird.glb": "Fly",
        "cat.glb": "Idle",
        "frog.glb": "Jump",
        "butterfly.glb": "Flap",
    }

    anim_name = animation_map.get(model_filename) if exists else None

    return {
        "model_path": model_path if exists else None,
        "exists": exists,
        "has_animation": bool(anim_name),
        "animation_name": anim_name,
        "filename": model_filename,
    }
