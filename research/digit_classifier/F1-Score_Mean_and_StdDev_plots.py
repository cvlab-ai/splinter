import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

base_path = './Euro_stan_29_12 - done'
files = [f for f in os.listdir(base_path) if f.startswith('metrics_fold_') and f.endswith('.csv')]

f1_scores_by_type_and_class = {}
average_f1_scores_by_type = {}
trainings_by_type = {}

for file in files:
    try:
        parts = file.split('_')
        training_number = int(parts[2])
        test_type = parts[3].split('.')[0]

        if test_type not in f1_scores_by_type_and_class:
            f1_scores_by_type_and_class[test_type] = {i: [] for i in range(10)}
            average_f1_scores_by_type[test_type] = []
            trainings_by_type[test_type] = []

        data = pd.read_csv(os.path.join(base_path, file))

        for label in range(10):
            f1_scores_by_type_and_class[test_type][label].append(
                data.loc[data['Class'] == label, 'F1-Score'].values[0]
            )

        avg_f1_score = data['F1-Score'].dropna().mean()
        average_f1_scores_by_type[test_type].append(avg_f1_score)
        trainings_by_type[test_type].append(training_number)

    except Exception as e:
        print(f"Error processing file {file}: {e}")

for test_type, f1_scores_by_class in f1_scores_by_type_and_class.items():
    class_means = []
    class_stddevs = []

    for label in range(10):
        mean_score = np.mean(f1_scores_by_class[label])
        stddev_score = np.std(f1_scores_by_class[label])
        class_means.append(mean_score)
        class_stddevs.append(stddev_score)
    print(f"Average F1-Scores for Type {test_type}: {class_means}")

    plt.figure(figsize=(12, 6))
    plt.errorbar(
        range(10),
        class_means,
        yerr=class_stddevs,
        fmt='o',
        ecolor='red',
        capsize=5,
        label=f'F1-Score Mean and StdDev ({test_type})'
    )
    plt.xlabel('Class', fontsize=12)
    plt.ylabel('F1-Score', fontsize=12)
    plt.title(f'F1-Score Mean and Standard Deviation per Class ({test_type})', fontsize=14)
    plt.ylim(0, 1.1)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()

    figs_path = os.path.join(base_path, 'figs_test')
    os.makedirs(figs_path, exist_ok=True)

    plt.savefig(f'{figs_path}/f1_score_mean_stddev_per_class_{test_type}.png')
    plt.close()
