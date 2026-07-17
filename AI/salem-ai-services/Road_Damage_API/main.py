from io import BytesIO

import timm
import torch

from PIL import Image

from fastapi import FastAPI, UploadFile, File
from torchvision import transforms


from Road_Damage_API.config import (
    DEVICE,
    NUM_CLASSES,
    CLASS_NAMES,
    MODEL_DIR,
    IMAGE_SIZE
)

# =========================
# APP
# =========================

app = FastAPI(
    title="Incident Type Classification Service"
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
# ROUTES
# =========================

@app.get("/")
def root():
    return {
        "service": "Incident Type Classification",
        "status": "running"
    }


@app.post("/predict")
async def predict(
    image: UploadFile = File(...)
):

    contents = await image.read()

    image = Image.open(
        BytesIO(contents)
    ).convert("RGB")

    image = transform(image)

    image = image.unsqueeze(0)

    image = image.to(DEVICE)

    with torch.no_grad():

        outputs = model(image)

        probabilities = torch.softmax(
            outputs,
            dim=1
        )

        confidence, predicted = torch.max(
            probabilities,
            dim=1
        )

    prediction = CLASS_NAMES[
        predicted.item()
    ]

    return {
        "prediction": prediction,
        "confidence": round(
            confidence.item() * 100,
            2
        )
    }