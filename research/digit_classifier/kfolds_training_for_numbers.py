import datetime
import shutil
from pathlib import Path
import torch
import numpy as np
import pandas as pd
from ultralytics import YOLO
import glob, os

project = "kfold_demo_mnist"
kfold_base_path = Path('k_folds_newer_mnist')

prefixes = ["american", "euro", "mnist","all"]
fold_dirs = sorted([f for f in kfold_base_path.iterdir() if f.is_dir()])

for folder in fold_dirs:
    print(folder)

results = []

for i, fold_dir in enumerate(fold_dirs):
    torch.cuda.set_per_process_memory_fraction(0.8, device=0)
    model = YOLO('yolo11x-cls.pt')
    

    model.train(data=fold_dir, project=project, epochs=1000, imgsz=128, patience=15, batch=0.8, 
                plots=True, verbose=True, degrees=0.0, translate=0.0, shear=0.0, 
                fliplr=0.0, mosaic=0.0, scale=0.0, erasing=0.0)

   
    for prefix in prefixes:
        test_tmp2_dir = fold_dir / "test_tmp2" / prefix
        test_dir = fold_dir / "test"
        
        if test_dir.exists():
            shutil.rmtree(test_dir) 
        shutil.copytree(test_tmp2_dir, test_dir)  

        metrics = model.val(imgsz=128, split='test')
        result = model.metrics
        results.append(result)

        confusion_matrix = metrics.confusion_matrix
        npy_path = Path(project) / f"confusion_matrix_fold_{i}_{prefix}.npy"
        np.save(npy_path, confusion_matrix)

        confusion_matrix = np.load(npy_path, allow_pickle=True).item()
        matrix = confusion_matrix.matrix
        df_cm = pd.DataFrame(matrix, index=range(len(matrix)), columns=range(len(matrix)))
        print(f"Confusion Matrix DataFrame for {prefix}:")
        print(df_cm)

        precision = []
        recall = []
        f1_score = []

        for j in range(len(matrix)):
            tp = matrix[j, j]  # True positives
            fp = matrix[:, j].sum() - tp  # False positives
            fn = matrix[j, :].sum() - tp  # False negatives
            tn = matrix.sum() - (tp + fp + fn)  # True negatives

            prec = tp / (tp + fp) if tp + fp > 0 else 0
            rec = tp / (tp + fn) if tp + fn > 0 else 0
            f1 = 2 * (prec * rec) / (prec + rec) if (prec + rec) > 0 else 0

            precision.append(prec)
            recall.append(rec)
            f1_score.append(f1)

        metrics_df = pd.DataFrame({
            'Class': range(len(matrix)),
            'Precision': precision,
            'Recall': recall,
            'F1-Score': f1_score
        })

        print(metrics_df)

        metrics_df.to_csv(Path(project) / f'metrics_fold_{i}_{prefix}.csv', index=False)
        print(f"Metrics for {prefix} saved.")

    del model
    torch.cuda.empty_cache()
    torch.cuda.synchronize()

print("Data preparation and model training completed.")
