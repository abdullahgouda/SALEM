import torch
import timm
from PIL import Image
from torchvision import transforms
from sklearn.metrics.pairwise import cosine_similarity
from transformers import CLIPProcessor, CLIPModel

from src.config import (
    DEVICE,
    NUM_CLASSES,
    CLASS_NAMES,
    MODEL_DIR,
    IMAGE_SIZE
)

# =====================
# LOAD CLASSIFIER
# =====================

classifier = timm.create_model(
    "efficientnet_b0",
    pretrained=False,
    num_classes=NUM_CLASSES
)

classifier.load_state_dict(
    torch.load(
        MODEL_DIR / "best_model.pth",
        map_location=DEVICE
    )
)

classifier = classifier.to(DEVICE)
classifier.eval()

# =====================
# LOAD CLIP
# =====================

clip_model = CLIPModel.from_pretrained(
    "openai/clip-vit-base-patch32"
)

clip_processor = CLIPProcessor.from_pretrained(
    "openai/clip-vit-base-patch32"
)

# =====================
# IMAGE TRANSFORM
# =====================

transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor()
])

# =====================
# CLASSIFY IMAGE
# =====================

def classify_image(image_path):

    image = Image.open(image_path).convert("RGB")

    image = transform(image)

    image = image.unsqueeze(0)

    image = image.to(DEVICE)

    with torch.no_grad():

        outputs = classifier(image)

        probs = torch.softmax(outputs, dim=1)

        confidence, predicted = torch.max(
            probs,
            dim=1
        )

    return (
        CLASS_NAMES[predicted.item()],
        confidence.item()
    )

# =====================
# CLIP SIMILARITY
# =====================

def clip_similarity(before_path, after_path):

    before = Image.open(before_path).convert("RGB")
    after = Image.open(after_path).convert("RGB")

    inputs = clip_processor(
        images=[before, after],
        return_tensors="pt"
    )

    with torch.no_grad():

        features = clip_model.get_image_features(
            pixel_values=inputs["pixel_values"]
        )

    similarity = cosine_similarity(
        features[0].reshape(1, -1),
        features[1].reshape(1, -1)
    )[0][0]

    return similarity

# =====================
# IMPROVEMENT SCORE
# =====================

def calculate_improvement(
    before_conf,
    after_conf
):

    if before_conf == 0:
        return 0

    improvement = (
        (before_conf - after_conf)
        / before_conf
    ) * 100

    return max(0, round(improvement, 2))

# =====================
# STATUS
# =====================

def get_status(improvement):

    if improvement >= 80:
        return "Resolved"

    elif improvement >= 40:
        return "Partially Resolved"

    else:
        return "Not Resolved"

# =====================
# MAIN
# =====================

before_path = "test_images/beforee.png"
after_path = "test_images/afterrr.png"

# CLIP CHECK
sim = clip_similarity(
    before_path,
    after_path
)

# CLASSIFICATION
before_class, before_conf = classify_image(
    before_path
)

after_class, after_conf = classify_image(
    after_path
)

# IMPROVEMENT
improvement = calculate_improvement(
    before_conf,
    after_conf
)

status = get_status(
    improvement
)

# =====================
# RESULTS
# =====================

print("\n===================")
print("CLIP Similarity")
print("===================")
print(f"{sim*100:.2f}%")

print("\n===================")
print("Before Image")
print("===================")
print("Class:", before_class)
print(f"Confidence: {before_conf*100:.2f}%")

print("\n===================")
print("After Image")
print("===================")
print("Class:", after_class)
print(f"Confidence: {after_conf*100:.2f}%")

print("\n===================")
print("Resolution Analysis")
print("===================")
print(f"Improvement: {improvement:.2f}%")
print(f"Status: {status}")