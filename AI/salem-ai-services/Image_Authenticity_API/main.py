from fastapi import FastAPI, UploadFile, File
from PIL import Image
from torchvision import transforms
import torch
import timm
import io

app = FastAPI(
    title="Image Authenticity Service"
)

# =========================
# CONFIG
# =========================

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "best_model.pth"

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

CLASS_NAMES = [
    "authentic",
    "spam"
]

IMAGE_SIZE = 224

# =========================
# LOAD MODEL
# =========================

model = timm.create_model(
    "efficientnet_b0",
    pretrained=False,
    num_classes=2
)

model.load_state_dict(
    torch.load(
        MODEL_PATH,
        map_location=DEVICE
    )
)

model.to(DEVICE)
model.eval()

transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor()
])

# =========================
# ROUTES
# =========================

@app.get("/")
def home():
    return {
        "service": "Image Authenticity Service",
        "status": "running"
    }

@app.post("/predict")
async def predict(
    file: UploadFile = File(...)
):

    image_bytes = await file.read()

    image = Image.open(
        io.BytesIO(image_bytes)
    ).convert("RGB")

    image = transform(image)

    image = image.unsqueeze(0)

    image = image.to(DEVICE)

    with torch.no_grad():

        outputs = model(image)

        probs = torch.softmax(
            outputs,
            dim=1
        )

        confidence, pred = torch.max(
            probs,
            dim=1
        )

    prediction = CLASS_NAMES[
        pred.item()
    ]

    confidence = round(
        confidence.item() * 100,
        2
    )

    return {
        "prediction": prediction,
        "confidence": confidence
    }