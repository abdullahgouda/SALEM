from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from sklearn.metrics.pairwise import cosine_similarity
import torch

print("Loading CLIP Model...")

model = CLIPModel.from_pretrained(
    "openai/clip-vit-base-patch32"
)

processor = CLIPProcessor.from_pretrained(
    "openai/clip-vit-base-patch32"
)

before = Image.open(
    "test_images/before.png"
).convert("RGB")

after = Image.open(
    "test_images/after.png"
).convert("RGB")

inputs = processor(
    images=[before, after],
    return_tensors="pt"
)

with torch.no_grad():
    features = model.get_image_features(
        pixel_values=inputs["pixel_values"]
    )

similarity = cosine_similarity(
    features[0].reshape(1, -1),
    features[1].reshape(1, -1)
)[0][0]

print(f"\nSimilarity Score: {similarity:.4f}")

if similarity > 0.8:
    print("✅ Same Location")
elif similarity > 0.6:
    print("⚠️ Probably Same Location")
else:
    print("❌ Different Location")