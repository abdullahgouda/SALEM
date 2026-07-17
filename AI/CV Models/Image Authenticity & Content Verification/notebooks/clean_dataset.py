from PIL import Image
from pathlib import Path

root = Path("dataset_split")

bad_files = []

for img_path in root.rglob("*.*"):
    try:
        img = Image.open(img_path)
        img.verify()
    except Exception:
        bad_files.append(img_path)

print(f"Bad Files Found: {len(bad_files)}")

for f in bad_files:
    print(f)