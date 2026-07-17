from pathlib import Path
import random
import shutil

random.seed(42)

SOURCE = Path("dataset/raw")
DEST = Path("dataset/selected")

TARGETS = {
    "Concrete_Collapse": 1000,
    "Electrical_Pole": 1000,
    "Fallen_Tree": 1000,
    "Fire": 931,
    "Garbage": 1000,
    "Road_Damage": 1000,
}

DEST.mkdir(parents=True, exist_ok=True)

for class_name, target_count in TARGETS.items():

    src_dir = SOURCE / class_name
    dst_dir = DEST / class_name

    dst_dir.mkdir(parents=True, exist_ok=True)

    images = [
        f for f in src_dir.iterdir()
        if f.is_file()
    ]

    if len(images) <= target_count:
        selected = images
    else:
        selected = random.sample(
            images,
            target_count
        )

    for idx, img in enumerate(selected):

        new_name = f"{idx}{img.suffix}"

        shutil.copy2(
            img,
            dst_dir / new_name
        )

    print(
        f"{class_name}: {len(selected)} copied"
    )

print("\nDone!")