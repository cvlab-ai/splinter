import os
import pandas as pd
import matplotlib.pyplot as plt

base_path = './Mnist_stan_26_12 - done'

figs_path = os.path.join(base_path, 'figs_test')

os.makedirs(figs_path, exist_ok=True)

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
    for label in range(10):
        plt.figure(figsize=(10, 6))

        print(f"F1-Scores for Class {label} (Type {test_type}): {f1_scores_by_class[label]}")
        print(f"Trainings (Type {test_type}): {trainings_by_type[test_type]}")

        plt.scatter(f1_scores_by_class[label], trainings_by_type[test_type], color='blue',
                    label=f'F1-Score for Class {label}')
        plt.xlim(0.2, 1.1)
        plt.xlabel('F1-Score', fontsize=12)
        plt.ylabel('Training Number', fontsize=12)
        plt.title(f'F1-Score vs Training Number (Class {label}, Type {test_type})', fontsize=14)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend()

        plt.ylim(min(trainings_by_type[test_type]), max(trainings_by_type[test_type]))
        plt.gca().invert_yaxis()

        plt.savefig(f'{figs_path}/class_{label}_f1_score_vs_training_{test_type}.png')
        plt.close()

for test_type, average_f1_scores in average_f1_scores_by_type.items():
    plt.figure(figsize=(10, 6))
    plt.scatter(average_f1_scores, trainings_by_type[test_type], color='green', label=f'Average F1-Score ({test_type})')
    plt.xlabel('F1-Score', fontsize=12)
    plt.ylabel('Training Number', fontsize=12)
    plt.title(f'Average F1-Score vs Training Number (Type {test_type})', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.xlim(0.2, 1.1)
    plt.ylim(min(trainings_by_type[test_type]), max(trainings_by_type[test_type]))
    plt.gca().invert_yaxis()

    plt.savefig(f'{figs_path}/average_f1_score_vs_training_{test_type}.png')
    plt.close()
