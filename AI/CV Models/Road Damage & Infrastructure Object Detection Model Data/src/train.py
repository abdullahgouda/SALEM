import copy
import time

import timm
import torch
import torch.nn as nn
import torch.optim as optim

from src.config import (
    DEVICE,
    EPOCHS,
    LEARNING_RATE,
    NUM_CLASSES,
    MODEL_DIR,
    PATIENCE,
)

from src.dataset import (
    train_loader,
    val_loader,
)

# =========================
# MODEL
# =========================

model = timm.create_model(
    "efficientnet_b0",
    pretrained=True,
    num_classes=NUM_CLASSES
)

model = model.to(DEVICE)
print(f"Using Device: {DEVICE}")
print(f"Classes: {NUM_CLASSES}")

# =========================
# LOSS & OPTIMIZER
# =========================

criterion = nn.CrossEntropyLoss()

optimizer = optim.AdamW(
    model.parameters(),
    lr=LEARNING_RATE
)

scheduler = optim.lr_scheduler.ReduceLROnPlateau(
    optimizer,
    mode="max",
    factor=0.5,
    patience=2
)

# =========================
# TRAINING
# =========================

best_val_acc = 0.0
best_weights = copy.deepcopy(model.state_dict())

early_stop_counter = 0

start_time = time.time()

for epoch in range(EPOCHS):

    print(f"\nEpoch [{epoch+1}/{EPOCHS}]")
    print("-" * 40)

    # =====================
    # TRAIN
    # =====================

    model.train()

    train_loss = 0.0
    train_correct = 0
    train_total = 0

    for images, labels in train_loader:

        images = images.to(DEVICE)
        labels = labels.to(DEVICE)

        optimizer.zero_grad()

        outputs = model(images)

        loss = criterion(outputs, labels)

        loss.backward()

        optimizer.step()

        train_loss += loss.item()

        _, preds = torch.max(outputs, 1)

        train_correct += (preds == labels).sum().item()
        train_total += labels.size(0)

    train_acc = train_correct / train_total

    # =====================
    # VALIDATION
    # =====================

    model.eval()

    val_loss = 0.0
    val_correct = 0
    val_total = 0

    with torch.no_grad():

        for images, labels in val_loader:

            images = images.to(DEVICE)
            labels = labels.to(DEVICE)

            outputs = model(images)

            loss = criterion(outputs, labels)

            val_loss += loss.item()

            _, preds = torch.max(outputs, 1)

            val_correct += (preds == labels).sum().item()
            val_total += labels.size(0)

    val_acc = val_correct / val_total

    scheduler.step(val_acc)

    print(
        f"Train Loss: {train_loss:.4f} | "
        f"Train Acc: {train_acc:.4f}"
    )

    print(
        f"Val Loss: {val_loss:.4f} | "
        f"Val Acc: {val_acc:.4f}"
    )

    # =====================
    # SAVE BEST MODEL
    # =====================

    if val_acc > best_val_acc:

        best_val_acc = val_acc

        best_weights = copy.deepcopy(
            model.state_dict()
        )

        torch.save(
            best_weights,
            MODEL_DIR / "best_model.pth"
        )

        print("✅ Best model saved")

        early_stop_counter = 0

    else:

        early_stop_counter += 1

    # =====================
    # EARLY STOPPING
    # =====================

    if early_stop_counter >= PATIENCE:

        print("\n🛑 Early Stopping Triggered")
        break

# =========================
# FINISH
# =========================

total_time = time.time() - start_time

print("\nTraining Finished")
print(f"Best Validation Accuracy: {best_val_acc:.4f}")
print(f"Training Time: {total_time/60:.2f} min")