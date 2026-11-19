"""BIOVA Model Evaluation Tool
Calculates Confusion Matrix, Accuracy, Precision, Recall, and F1-Score for trained models.
"""

import os
import json
from pathlib import Path
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
os.environ.setdefault("KERAS_HOME", str(BASE_DIR / ".keras"))
os.environ.setdefault("MPLCONFIGDIR", str(BASE_DIR / ".matplotlib"))

import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix


def evaluate(category: str = "hewan"):
    print(f"=== Evaluasi Model AI BIOVA: Kategori {category.title()} ===")
    model_name = "model_hewan.keras" if category.lower() == "hewan" else "model_tumbuhan.keras"
    model_path = BASE_DIR / "models" / model_name
    dataset_dir = BASE_DIR / "datasets" / category.lower()

    if not model_path.exists():
        print(f"Error: Model {model_path} tidak ditemukan.")
        return

    if not dataset_dir.exists():
        print(f"Error: Dataset {dataset_dir} tidak ditemukan.")
        return

    model = tf.keras.models.load_model(str(model_path))
    val_ds = tf.keras.utils.image_dataset_from_directory(
        dataset_dir,
        validation_split=0.2,
        subset="validation",
        seed=42,
        image_size=(224, 224),
        batch_size=32,
        shuffle=False,
    )

    class_names = val_ds.class_names
    y_true = []
    y_pred = []

    for images, labels in val_ds:
        preds = model.predict(images, verbose=0)
        y_true.extend(labels.numpy())
        y_pred.extend(np.argmax(preds, axis=1))

    print("\n--- CONFUSION MATRIX ---")
    cm = confusion_matrix(y_true, y_pred)
    print(cm)

    print("\n--- CLASSIFICATION REPORT ---")
    report = classification_report(y_true, y_pred, target_names=class_names)
    print(report)


if __name__ == "__main__":
    import sys
    cat = sys.argv[1] if len(sys.argv) > 1 else "hewan"
    evaluate(cat)
