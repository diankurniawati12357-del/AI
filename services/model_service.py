"""BIOVA AI Model Service
Handles safe TensorFlow/Keras model loading, preprocessing, inference, and error handling.
Never produces simulated or fabricated predictions when models are missing.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import numpy as np
from PIL import Image
import streamlit as st

from services.config import (
    ANIMAL_MODEL_PATH,
    ANIMAL_FT_MODEL_PATH,
    ANIMAL_LABEL_PATH,
    PLANT_MODEL_PATH,
    PLANT_LABEL_PATH,
)

CONFIDENCE_THRESHOLD = 0.40


def get_model_path_for_category(category: str) -> Optional[Path]:
    """Finds the existing model path for a category, checking fine-tuned checkpoints first."""
    cat = category.lower()
    if cat == "hewan":
        if ANIMAL_FT_MODEL_PATH.exists():
            return ANIMAL_FT_MODEL_PATH
        if ANIMAL_MODEL_PATH.exists():
            return ANIMAL_MODEL_PATH
    elif cat == "tumbuhan":
        if PLANT_MODEL_PATH.exists():
            return PLANT_MODEL_PATH
    return None


def get_label_config(category: str) -> Dict[str, Any]:
    """Reads the JSON label configuration for the category."""
    cat = category.lower()
    path = ANIMAL_LABEL_PATH if cat == "hewan" else PLANT_LABEL_PATH
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    # Fallback default classes
    if cat == "hewan":
        return {"classes": ["Mamalia", "Aves", "Reptil", "Amfibi", "Pisces", "Invertebrata"], "input_shape": [224, 224, 3]}
    else:
        return {"classes": ["Dikotil", "Monokotil"], "input_shape": [224, 224, 3]}


@st.cache_resource(show_spinner=False)
def load_keras_model(model_path_str: str):
    """Loads a Keras model and caches it across Streamlit reruns."""
    try:
        from tensorflow.keras.models import load_model
        return load_model(model_path_str)
    except Exception as e:
        return None


def check_model_availability(category: str) -> Tuple[bool, str]:
    """Checks whether a valid trained model is available on disk for the category."""
    model_path = get_model_path_for_category(category)
    if model_path is None or not model_path.exists():
        expected = "model_hewan.keras" if category.lower() == "hewan" else "model_tumbuhan.keras"
        return False, f"Model AI belum tersedia untuk kategori {category.title()}. Harap latih atau tempatkan file {expected} di folder models/."
    return True, str(model_path)


def classify_image(category: str, img: Image.Image) -> Dict[str, Any]:
    """Preprocesses the image, executes neural network inference, and formats the output.
    Returns status: 'success', 'model_unavailable', 'low_confidence', or 'error'.
    """
    category = category.lower()
    is_avail, model_info = check_model_availability(category)
    if not is_avail:
        return {
            "status": "model_unavailable",
            "category": category,
            "message": model_info,
            "predicted_group": None,
            "confidence": 0.0,
        }

    try:
        model = load_keras_model(model_info)
        if model is None:
            return {
                "status": "error",
                "category": category,
                "message": "Gagal memuat model Keras dari disk.",
                "predicted_group": None,
                "confidence": 0.0,
            }

        label_cfg = get_label_config(category)
        target_size = tuple(label_cfg.get("input_shape", [224, 224, 3])[:2])

        # Preprocessing: Convert to RGB and resize
        processed_img = img.convert("RGB").resize(target_size)
        arr = np.array(processed_img, dtype=np.float32)

        # Normalization
        norm_type = label_cfg.get("normalization", "rescale_1_255")
        if norm_type == "rescale_1_255":
            arr = arr / 255.0
        elif norm_type == "tf_vgg":
            arr = arr - np.array([123.68, 116.779, 103.939])

        batch = np.expand_dims(arr, axis=0)

        # Run inference
        preds = model.predict(batch, verbose=0)[0]
        top_idx = int(np.argmax(preds))
        confidence = float(preds[top_idx])

        classes = label_cfg.get("classes", [])
        if top_idx < len(classes):
            predicted_class = classes[top_idx]
        else:
            predicted_class = f"Class_{top_idx}"

        # Evaluate confidence
        if confidence < CONFIDENCE_THRESHOLD:
            return {
                "status": "low_confidence",
                "category": category,
                "predicted_group": predicted_class,
                "confidence": confidence,
                "message": "Tingkat keyakinan model terlalu rendah untuk mengidentifikasi objek dengan pasti.",
            }

        return {
            "status": "success",
            "category": category,
            "predicted_group": predicted_class,
            "confidence": confidence,
            "model_version": Path(model_info).name,
            "message": "Objek Berhasil Terdeteksi!",
        }

    except Exception as e:
        return {
            "status": "error",
            "category": category,
            "message": f"Terjadi kesalahan saat inferensi: {str(e)}",
            "predicted_group": None,
            "confidence": 0.0,
        }
