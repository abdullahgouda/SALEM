import torch
import timm
import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score
)

from src.config import (
    DEVICE,
    NUM_CLASSES,
    CLASS_NAMES,
    MODEL_DIR,
    OUTPUT_DIR
)

from src.dataset import test_loader

# =========================
# LOAD MODEL
# =========================

model = timm.create_model(
    "efficientnet_b0",
    pretrained=False,
    num_classes=NUM_CLASSES
)

model.load_state_dict(
    torch.load(
        MODEL_DIR / "best_model.pth",
        map_location=DEVICE
    )
)

model = model.to(DEVICE)
model.eval()

# =========================
# PREDICTION
# =========================

y_true = []
y_pred = []

with torch.no_grad():

    for images, labels in test_loader:

        images = images.to(DEVICE)

        outputs = model(images)

        preds = torch.argmax(outputs, dim=1)

        y_true.extend(labels.numpy())
        y_pred.extend(preds.cpu().numpy())

# =========================
# METRICS
# =========================

acc = accuracy_score(y_true, y_pred)

print("\n" + "=" * 50)
print(f"TEST ACCURACY: {acc:.4f}")
print("=" * 50)

report = classification_report(
    y_true,
    y_pred,
    target_names=CLASS_NAMES
)

print("\nCLASSIFICATION REPORT\n")
print(report)

# save report

with open(
    OUTPUT_DIR / "classification_report.txt",
    "w",
    encoding="utf-8"
) as f:

    f.write(report)

# =========================
# CONFUSION MATRIX
# =========================

cm = confusion_matrix(y_true, y_pred)

plt.figure(figsize=(8, 6))

plt.imshow(cm)

plt.colorbar()

plt.xticks(
    np.arange(len(CLASS_NAMES)),
    CLASS_NAMES,
    rotation=45
)

plt.yticks(
    np.arange(len(CLASS_NAMES)),
    CLASS_NAMES
)

plt.xlabel("Predicted")
plt.ylabel("Actual")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "confusion_matrix.png",
    dpi=300
)

print("\nConfusion Matrix Saved")