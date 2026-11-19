"""BIOVA Animal Model Training Pipeline
Trains a 6-class image classification model (Mamalia, Aves, Reptil, Amfibi, Pisces, Invertebrata)
using Transfer Learning with MobileNetV2 and exports model_hewan.keras with metadata.
"""

import os
import json
from pathlib import Path
import numpy as np

# Safe environment settings
BASE_DIR = Path(__file__).resolve().parent.parent
os.environ.setdefault("KERAS_HOME", str(BASE_DIR / ".keras"))
os.environ.setdefault("MPLCONFIGDIR", str(BASE_DIR / ".matplotlib"))

import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2

DATASET_DIR = BASE_DIR / "datasets" / "hewan"
OUTPUT_MODEL_PATH = BASE_DIR / "models" / "model_hewan.keras"
OUTPUT_LABEL_PATH = BASE_DIR / "models" / "labels" / "label_hewan.json"

IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 15
CLASSES = ["Mamalia", "Aves", "Reptil", "Amfibi", "Pisces", "Invertebrata"]


def train():
    print(f"=== Memulai Pipeline Pelatihan Model Hewan BIOVA ===")
    print(f"Direktori dataset: {DATASET_DIR}")

    if not DATASET_DIR.exists() or len(os.listdir(DATASET_DIR)) == 0:
        print(f"PERINGATAN: Direktori dataset {DATASET_DIR} kosong.")
        print("Harap isi folder kelas dengan foto-foto satwa sebelum menjalankan training.")
        return

    # Data loaders
    train_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_DIR,
        validation_split=0.2,
        subset="training",
        seed=42,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
    )

    val_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_DIR,
        validation_split=0.2,
        subset="validation",
        seed=42,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
    )

    detected_classes = train_ds.class_names
    print(f"Kelas terdeteksi: {detected_classes}")

    # Data augmentation pipeline (active only during training)
    data_augmentation = tf.keras.Sequential([
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.15),
        layers.RandomZoom(0.1),
    ])

    # Transfer Learning Base Model
    base_model = MobileNetV2(
        input_shape=(224, 224, 3),
        include_top=False,
        weights="imagenet",
    )
    base_model.trainable = False  # Freeze pre-trained weights

    # Build classification head
    inputs = tf.keras.Input(shape=(224, 224, 3))
    x = data_augmentation(inputs)
    x = layers.Rescaling(1.0 / 255)(x)
    x = base_model(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.3)(x)
    outputs = layers.Dense(len(detected_classes), activation="softmax")(x)

    model = models.Model(inputs, outputs)

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    print("Memulai proses fitting model...")
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS,
    )

    # Save trained model
    OUTPUT_MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    model.save(str(OUTPUT_MODEL_PATH))
    print(f"Model berhasil disimpan di: {OUTPUT_MODEL_PATH}")

    # Save label mappings
    OUTPUT_LABEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    label_meta = {
        "classes": detected_classes,
        "input_shape": [224, 224, 3],
        "normalization": "rescale_1_255",
        "epochs": EPOCHS,
    }
    with open(OUTPUT_LABEL_PATH, "w", encoding="utf-8") as f:
        json.dump(label_meta, f, indent=2)
    print(f"Label metadata disimpan di: {OUTPUT_LABEL_PATH}")


if __name__ == "__main__":
    train()
