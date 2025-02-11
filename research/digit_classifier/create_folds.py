import os
import shutil
import random

final_folder = "finalv2"
output_folder = "k_folds_newer_mnist"

training_prefixes = ['mnist']

def create_kfold_datasets(final_folder, output_folder, training_prefixes):
    index_folders = [f for f in os.listdir(final_folder) if os.path.isdir(os.path.join(final_folder, f))]

    used_val_folders = []
    for fold_idx, test_index_folder in enumerate(index_folders):
        val_candidates = [folder for folder in index_folders if
                          folder != test_index_folder and folder not in used_val_folders]
        val_index_folder = random.choice(val_candidates)
        used_val_folders.append(val_index_folder)

        fold_output_path = os.path.join(output_folder, f"fold_{fold_idx + 1}_{test_index_folder}_{val_index_folder}")
        test_folder = os.path.join(fold_output_path, "test")
        train_folder = os.path.join(fold_output_path, "train")
        val_folder = os.path.join(fold_output_path, "val")

        os.makedirs(test_folder, exist_ok=True)
        os.makedirs(train_folder, exist_ok=True)
        os.makedirs(val_folder, exist_ok=True)

        for index_folder in index_folders:
            if index_folder != test_index_folder and index_folder != val_index_folder:
                label_folders = [os.path.join(final_folder, index_folder, str(label)) for label in range(10)]

                for label_folder in label_folders:
                    for image_name in os.listdir(label_folder):

                        if any(image_name.startswith(prefix) for prefix in training_prefixes):
                            src_image_path = os.path.join(label_folder, image_name)
                            dst_image_folder = os.path.join(train_folder, str(label_folder.split('/')[-1]))
                            os.makedirs(dst_image_folder, exist_ok=True)
                            shutil.copy(src_image_path, os.path.join(dst_image_folder, image_name))

        test_label_folders = [os.path.join(final_folder, test_index_folder, str(label)) for label in range(10)]
        for label_folder in test_label_folders:
            for image_name in os.listdir(label_folder):
                src_image_path = os.path.join(label_folder, image_name)
                dst_image_folder = os.path.join(test_folder, str(label_folder.split('/')[-1]))
                os.makedirs(dst_image_folder, exist_ok=True)
                shutil.copy(src_image_path, os.path.join(dst_image_folder, image_name))

        print(f"Stworzono fold {fold_idx + 1} z {test_index_folder} jako zbiór testowy.")

        val_label_folders = [os.path.join(final_folder, val_index_folder, str(label)) for label in range(10)]
        for label_folder in val_label_folders:
            for image_name in os.listdir(label_folder):
                if any(image_name.startswith(prefix) for prefix in training_prefixes):
                    src_image_path = os.path.join(label_folder, image_name)
                    dst_image_folder = os.path.join(val_folder, str(label_folder.split('/')[-1]))
                    os.makedirs(dst_image_folder, exist_ok=True)
                    shutil.copy(src_image_path, os.path.join(dst_image_folder, image_name))

        print(f"Stworzono fold {fold_idx + 1} z {val_label_folders} jako zbiór walidacyjny.")

create_kfold_datasets(final_folder, output_folder, training_prefixes)

print("Tworzenie K-fold datasets zakończone.")
