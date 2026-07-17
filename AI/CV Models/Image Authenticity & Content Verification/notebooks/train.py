import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from tqdm import tqdm
import timm

# =========================
# CONFIG
# =========================

DATA_DIR = "dataset_split"

IMAGE_SIZE = 224
BATCH_SIZE = 16
NUM_EPOCHS = 15
LEARNING_RATE = 1e-4

MODEL_PATH = "saved_model/best_model.pth"

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print(f"\nUsing Device: {DEVICE}")

# =========================
# TRANSFORMS
# =========================

train_transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ColorJitter(
        brightness=0.2,
        contrast=0.2
    ),
    transforms.ToTensor()
])

val_transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor()
])

# =========================
# DATASETS
# =========================

train_dataset = datasets.ImageFolder(
    os.path.join(DATA_DIR, "train"),
    transform=train_transform
)

val_dataset = datasets.ImageFolder(
    os.path.join(DATA_DIR, "val"),
    transform=val_transform
)

train_loader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    shuffle=True,
    num_workers=0
)

val_loader = DataLoader(
    val_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=0
)

print("Classes:", train_dataset.classes)

# =========================
# CLASS WEIGHTS
# =========================

authentic_count = 7807
spam_count = 2797

total = authentic_count + spam_count

weights = torch.tensor([
    total / authentic_count,
    total / spam_count
], dtype=torch.float32).to(DEVICE)

# =========================
# MODEL
# =========================

model = timm.create_model(
    "efficientnet_b0",
    pretrained=True,
    num_classes=2
)

model.to(DEVICE)

criterion = nn.CrossEntropyLoss(weight=weights)

optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=LEARNING_RATE
)

# =========================
# TRAINING
# =========================

best_f1 = 0

for epoch in range(NUM_EPOCHS):

    model.train()

    running_loss = 0

    train_bar = tqdm(
        train_loader,
        desc=f"Epoch {epoch+1}/{NUM_EPOCHS}"
    )

    for images, labels in train_bar:

        images = images.to(DEVICE)
        labels = labels.to(DEVICE)

        optimizer.zero_grad()

        outputs = model(images)

        loss = criterion(
            outputs,
            labels
        )

        loss.backward()
        optimizer.step()

        running_loss += loss.item()

    # =====================
    # VALIDATION
    # =====================

    model.eval()

    y_true = []
    y_pred = []

    with torch.no_grad():

        for images, labels in val_loader:

            images = images.to(DEVICE)
            labels = labels.to(DEVICE)

            outputs = model(images)

            preds = torch.argmax(
                outputs,
                dim=1
            )

            y_true.extend(
                labels.cpu().numpy()
            )

            y_pred.extend(
                preds.cpu().numpy()
            )

    acc = accuracy_score(
        y_true,
        y_pred
    )

    precision = precision_score(
        y_true,
        y_pred
    )

    recall = recall_score(
        y_true,
        y_pred
    )

    f1 = f1_score(
        y_true,
        y_pred
    )

    print("\n")
    print(f"Epoch {epoch+1}")
    print(f"Accuracy : {acc:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1 Score : {f1:.4f}")

    if f1 > best_f1:

        best_f1 = f1

        torch.save(
            model.state_dict(),
            MODEL_PATH
        )

        print("Best Model Saved!")

print("\nTraining Finished")
print(f"Best F1: {best_f1:.4f}")