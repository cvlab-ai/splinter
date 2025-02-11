import shutil
from pathlib import Path

k_folds_dir = Path("k_folds_newer_mnist")
prefixes = ["american", "euro", "mnist"]

for fold_dir in k_folds_dir.iterdir():
    if not fold_dir.is_dir() or not fold_dir.name.startswith("fold_"):
        continue

    source_test_dir = fold_dir / "test"
    test_tmp_dir = fold_dir / "test_tmp"
    test_tmp2_dir = fold_dir / "test_tmp2"

    if test_tmp_dir.exists():
        shutil.rmtree(test_tmp_dir)
    if test_tmp2_dir.exists():
        shutil.rmtree(test_tmp2_dir)

    shutil.copytree(source_test_dir, test_tmp_dir)

    for prefix in prefixes:
        prefix_dir = test_tmp2_dir / prefix
        prefix_dir.mkdir(parents=True, exist_ok=True)

        for label_dir in test_tmp_dir.iterdir():
            if not label_dir.is_dir():
                continue

            label = label_dir.name
            new_label_dir = prefix_dir / label
            new_label_dir.mkdir(parents=True, exist_ok=True)

            for file in label_dir.glob(f"{prefix}*"):
                shutil.copy(file, new_label_dir / file.name)

    all_dir = test_tmp2_dir / "all"
    all_dir.mkdir(parents=True, exist_ok=True)

    for label_dir in test_tmp_dir.iterdir():
        if not label_dir.is_dir():
            continue

        label = label_dir.name
        new_label_dir = all_dir / label
        new_label_dir.mkdir(parents=True, exist_ok=True)

        for file in label_dir.glob("*"):
            shutil.copy(file, new_label_dir / file.name)

print("Data preparation completed.")
