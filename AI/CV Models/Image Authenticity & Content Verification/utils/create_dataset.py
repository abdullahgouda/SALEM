import os
import random
import shutil

from matplotlib import image

random.seed(42)

BASE_DIR = "dataset"

OUTPUT_DIR = "dataset_v1"

AUTHENTIC_COUNTS = {
    "Fire": 987,
    "Garbage": 1500,
    "road": 1500,
    "electrical poles": 1500,
    "fallen trees": 1500,
    "concrete": 1500,
}

SPAM_COUNTS = {
    "Animal": 1000,
    "Food": 1000,
    "Furniture": 1000,
    "Person": 1000,
}


def sample_and_copy(source_folder, destination_folder, num_images):
    os.makedirs(destination_folder, exist_ok=True)

    images = [
        f for f in os.listdir(source_folder)
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
    ]

    if len(images) < num_images:
        raise ValueError(
            f"{source_folder} contains only {len(images)} images "
            f"but {num_images} requested."
        )

    selected_images = random.sample(images, num_images)

    for image in selected_images:
        src_path = os.path.join(source_folder, image)

        file_ext = os.path.splitext(image)[1]

        new_name = f"{random.randint(100000,999999)}{file_ext}"

        dst_path = os.path.join(destination_folder, new_name)

        shutil.copy2(src_path, dst_path)

    print(f"✓ {os.path.basename(source_folder)} -> {num_images}")


print("Creating Authentic Dataset...")

for category, count in AUTHENTIC_COUNTS.items():
    src = os.path.join(BASE_DIR, "authentic", category)
    dst = os.path.join(OUTPUT_DIR, "authentic", category)

    sample_and_copy(src, dst, count)

print("\nCreating Spam Dataset...")

for category, count in SPAM_COUNTS.items():
    src = os.path.join(BASE_DIR, "spam", category)
    dst = os.path.join(OUTPUT_DIR, "spam", category)

    sample_and_copy(src, dst, count)

print("\nDataset V1 Created Successfully!")