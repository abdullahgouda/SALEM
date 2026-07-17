import os
import shutil
import random

random.seed(42)

SOURCE_DIR = "dataset_v1"
OUTPUT_DIR = "dataset_split"

TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
TEST_RATIO = 0.15


def get_all_images(folder):
    return [
        f for f in os.listdir(folder)
        if f.lower().endswith(
            (".jpg", ".jpeg", ".png", ".webp", ".bmp")
        )
    ]


def split_and_copy(class_name):
    source_folder = os.path.join(SOURCE_DIR, class_name)

    images = get_all_images(source_folder)

    random.shuffle(images)

    total = len(images)

    train_end = int(total * TRAIN_RATIO)
    val_end = train_end + int(total * VAL_RATIO)

    train_images = images[:train_end]
    val_images = images[train_end:val_end]
    test_images = images[val_end:]

    splits = {
        "train": train_images,
        "val": val_images,
        "test": test_images
    }

    for split_name, image_list in splits.items():

        dest_folder = os.path.join(
            OUTPUT_DIR,
            split_name,
            class_name
        )

        os.makedirs(dest_folder, exist_ok=True)

        for image in image_list:
            shutil.copy2(
                os.path.join(source_folder, image),
                os.path.join(dest_folder, image)
            )

    print(
        f"✓ {class_name} | "
        f"Train={len(train_images)} | "
        f"Val={len(val_images)} | "
        f"Test={len(test_images)}"
    )


if os.path.exists(OUTPUT_DIR):
    shutil.rmtree(OUTPUT_DIR)

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Creating Train / Val / Test Split...\n")

split_and_copy("authentic")
split_and_copy("spam")

print("\nDataset Split Created Successfully!")