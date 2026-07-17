from sklearn.metrics.pairwise import cosine_similarity
from models.clip_verifier import model, processor
import torch

def calculate_similarity(img1, img2):

    inputs = processor(
        images=[img1, img2],
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

    return float(similarity)