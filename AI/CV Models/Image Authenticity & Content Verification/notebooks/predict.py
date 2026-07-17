import torch
import timm

from PIL import Image
from torchvision import transforms

# =========================
# CONFIG
# =========================

MODEL_PATH = "saved_model/best_model.pth"

IMAGE_SIZE = 224

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

CLASS_NAMES = [
    "authentic",
    "spam"
]

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

# =========================
# TRANSFORM
# =========================

transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor()
])

# =========================
# PREDICT FUNCTION
# =========================

def predict_image(image_path):

    image = Image.open(image_path).convert("RGB")

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

    confidence = confidence.item() * 100

    return prediction, confidence


# =========================
# TEST
# =========================

if __name__ == "__main__":

    image_path = "D:/SALEM_Ai/CV Models/Image Authenticity & Content Verification/temp_uploads/000000007247.jpg"

    prediction, confidence = predict_image(
        image_path
    )

    print("\nPrediction :", prediction)
    print(
        f"Confidence : {confidence:.2f}%"
    )