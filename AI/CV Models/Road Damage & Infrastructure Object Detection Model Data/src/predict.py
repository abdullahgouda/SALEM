import torch
import timm
from PIL import Image
from torchvision import transforms

from src.config import (
    DEVICE,
    NUM_CLASSES,
    CLASS_NAMES,
    MODEL_DIR,
    IMAGE_SIZE
)

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
# IMAGE TRANSFORM
# =========================

transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor()
])

# =========================
# IMAGE PATH
# =========================

image_path = input("Enter image path: ")

image = Image.open(image_path).convert("RGB")

image = transform(image)

image = image.unsqueeze(0)

image = image.to(DEVICE)

# =========================
# PREDICTION
# =========================

with torch.no_grad():

    outputs = model(image)

    probabilities = torch.softmax(outputs, dim=1)

    confidence, predicted = torch.max(
        probabilities,
        dim=1
    )

predicted_class = CLASS_NAMES[
    predicted.item()
]

print("\nPrediction:", predicted_class)

print(
    "Confidence:",
    f"{confidence.item()*100:.2f}%"
)