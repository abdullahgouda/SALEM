from pathlib import Path
from sklearn.model_selection import train_test_split
import shutil

SOURCE_DIR = Path("dataset/selected")
OUTPUT_DIR = Path("dataset/classification")

TRAIN_RATIO = 0.7
VAL_RATIO = 0.2
TEST_RATIO = 0.1

classes = [d for d in SOURCE_DIR.iterdir() if d.is_dir()]

for cls in classes:
    images = list(cls.glob("*"))

    train_imgs, temp_imgs = train_test_split(
        images,
        test_size=(VAL_RATIO + TEST_RATIO),
        random_state=42
    )

    val_imgs, test_imgs = train_test_split(
        temp_imgs,
        test_size=TEST_RATIO / (VAL_RATIO + TEST_RATIO),
        random_state=42
    )

    for split_name, split_imgs in {
        "train": train_imgs,
        "val": val_imgs,
        "test": test_imgs,
    }.items():

        dst = OUTPUT_DIR / split_name / cls.name
        dst.mkdir(parents=True, exist_ok=True)

        for img in split_imgs:
            shutil.copy2(img, dst / img.name)

    print(f"{cls.name} done")

print("Dataset split completed!")