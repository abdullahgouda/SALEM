from pathlib import Path
from PIL import Image
import imagehash

RAW_DATASET = Path("dataset/raw")

VALID_EXTS = {".jpg", ".jpeg", ".png", ".webp"}

for class_dir in RAW_DATASET.iterdir():

    if not class_dir.is_dir():
        continue

    print(f"\nChecking: {class_dir.name}")

    hashes = {}

    removed = 0

    for img_path in class_dir.rglob("*"):

        if img_path.suffix.lower() not in VALID_EXTS:
            continue

        try:

            img = Image.open(img_path)

            h = str(imagehash.phash(img))

            if h in hashes:

                img_path.unlink()

                removed += 1

            else:

                hashes[h] = img_path

        except Exception:

            try:
                img_path.unlink()
                removed += 1
            except:
                pass

    print(
        f"Removed {removed} duplicate/corrupted images"
    )

print("\nDataset Cleaned Successfully")