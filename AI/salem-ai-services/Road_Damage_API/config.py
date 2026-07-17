from pathlib import Path
import torch

# =========================
# ROOT
# =========================

ROOT_DIR = Path(__file__).resolve().parent

# =========================
# PATHS
# =========================

DATASET_DIR = ROOT_DIR / "Dataset" / "classification"

MODEL_DIR = ROOT_DIR
OUTPUT_DIR = ROOT_DIR / "outputs"

MODEL_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# =========================
# CLASSES
# =========================

CLASS_NAMES = [
    "Concrete_Collapse",
    "Electrical_Pole",
    "Fallen_Tree",
    "Fire",
    "Garbage",
    "Road_Damage",
]

NUM_CLASSES = len(CLASS_NAMES)

# =========================
# TRAINING
# =========================

IMAGE_SIZE = 224
BATCH_SIZE = 32

EPOCHS = 20

LEARNING_RATE = 1e-4

PATIENCE = 5

# =========================
# DEVICE
# =========================

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)