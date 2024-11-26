import json
import os
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
from tqdm import tqdm

from src.controller import _check_image


def collect_data_paths(root_dir):
    data = []
    root_dir = Path(root_dir)
    directories = [p for p in root_dir.rglob('*') if p.is_dir()]

    for dirpath in tqdm(directories, desc='Collecting data paths'):
        required_files = {"log.txt", "orig.png"}
        files_in_dir = {file.name for file in dirpath.iterdir() if file.is_file()}

        if required_files.issubset(files_in_dir):
            log_file = dirpath / 'log.txt'
            img_file = dirpath / 'orig.png'

            data.append({
                "file_name": img_file.name,
                "log_path": str(log_file),
                "img_path": str(img_file),
                "dir_path": str(dirpath)
            })

    return data


def answer_string_to_list(answer_str):
    options = ['A', 'B', 'C', 'D']
    answer_list = [0, 0, 0, 0]
    for char in answer_str:
        if char in options:
            idx = options.index(char)
            answer_list[idx] = 1
    return answer_list


def parse_ground_truth(log_path):
    with open(log_path, 'r') as f:
        lines = f.readlines()

    ground_truth = {
        'exam_title': None,
        'student_name': None,
        'date': None,
        'key': None,
        'student_id_text': None,
        'student_id_boxes': None,
        'answers': {}
    }

    student_id_digits = []
    for line in lines:
        line = line.strip()
        if ': ' in line:
            key, value = line.split(': ', 1)
            key = key.strip()
            value = value.strip()
            if key == 'title':
                ground_truth['exam_title'] = value
            elif key == 'name':
                ground_truth['student_name'] = value
            elif key == 'date':
                ground_truth['date'] = value
            elif key == 'key':
                ground_truth['key'] = value
            elif key.startswith('id '):
                if len(value) == 1:
                    student_id_digits.append(value)
            elif key.startswith('question '):
                q_num = key[9:]
                ground_truth['answers'][q_num.lstrip('0')] = value

    ground_truth['student_id_text'] = ''.join(student_id_digits)
    ground_truth['student_id_boxes'] = ground_truth['student_id_text']
    return ground_truth


def compare_results(inference_result, ground_truth):
    comparison = {}

    # Compare fields
    comparison['student_id_text'] = (inference_result.get('student_id_boxes') == ground_truth.get('student_id_text'))
    comparison['exam_title'] = (inference_result.get('exam_title') == ground_truth.get('exam_title'))
    comparison['date'] = (inference_result.get('date') == ground_truth.get('date'))

    # Compare exam key
    gt_exam_key = answer_string_to_list(ground_truth.get('key')) if ground_truth.get('key') else [0, 0, 0, 0]
    comparison['exam_key'] = (inference_result.get('exam_key') == gt_exam_key)

    # Compare answers
    total_questions = len(ground_truth['answers'])
    correct_answers = 0
    for q_num_str, gt_answer_str in ground_truth['answers'].items():
        gt_answer_list = answer_string_to_list(gt_answer_str)
        inf_answer_list = inference_result['answers'].get(q_num_str)
        if inf_answer_list and inf_answer_list == gt_answer_list:
            correct_answers += 1

    comparison['total_questions'] = total_questions
    comparison['correct_answers'] = correct_answers
    comparison['overall_accuracy'] = correct_answers / total_questions if total_questions > 0 else 0

    return comparison


def load_existing_results(results_dir):
    existing_results = {}
    json_files = list(Path(results_dir).glob('*.json'))

    for json_file in json_files:
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            dir_path = data.get('dir_path')
            if dir_path:
                existing_results[dir_path] = (data, json_file)
        except Exception as e:
            print(f"Error loading {json_file}: {e}")

    return existing_results


def get_json_file_path(dir_path, results_dir):
    dir_name = Path(dir_path).name
    parent_dir_name = Path(dir_path).parent.name
    json_file_name = f"{parent_dir_name}_{dir_name}.json"
    json_file_path = Path(results_dir) / json_file_name
    return json_file_path


def generate_visualizations(results):
    overall_accuracies = []
    field_accuracies = {
        'student_id_text': [],
        'exam_title': [],
        'date': [],
        'exam_key': [],
    }
    total_questions_list = []
    correct_answers_list = []
    exam_titles = []
    exam_title_accuracies = {}

    for entry in results:
        comparison = entry.get('comparison', {})
        overall_accuracy = comparison.get('overall_accuracy', 0)
        overall_accuracies.append(overall_accuracy)

        total_questions = comparison.get('total_questions', 0)
        correct_answers = comparison.get('correct_answers', 0)
        total_questions_list.append(total_questions)
        correct_answers_list.append(correct_answers)

        exam_title = entry.get('ground_truth', {}).get('exam_title', 'Unknown')
        exam_titles.append(exam_title)

        if exam_title not in exam_title_accuracies:
            exam_title_accuracies[exam_title] = {'total': 0, 'correct': 0}
        exam_title_accuracies[exam_title]['total'] += total_questions
        exam_title_accuracies[exam_title]['correct'] += correct_answers

        for field in field_accuracies.keys():
            is_correct = comparison.get(field)
            if is_correct is not None:
                field_accuracies[field].append(int(is_correct))

    overall_df = pd.DataFrame({
        'Overall Accuracy': overall_accuracies,
        'Total Questions': total_questions_list,
        'Correct Answers': correct_answers_list,
        'Exam Title': exam_titles
    })

    overall_df.to_csv('./data/overall_results.csv', index=False)
    overall_df.to_excel('./data/overall_results.xlsx', index=False)
    print("Overall results saved to 'overall_results.csv' and 'overall_results.xlsx'")

    field_accuracy_df = pd.DataFrame(field_accuracies)
    field_accuracy_mean = field_accuracy_df.mean() * 100  # Convert to percentage

    plt.figure(figsize=(10, 6))
    bins = [i / 10 for i in range(0, 11)]
    sns.histplot(overall_df['Overall Accuracy'], bins=bins, kde=False, stat='count', discrete=False)
    plt.title('Distribution of Overall Accuracies')
    plt.xlabel('Overall Accuracy')
    plt.ylabel('Number of Entries')
    plt.xticks(bins)
    plt.savefig('overall_accuracy_distribution.png')
    plt.close()

    plt.figure(figsize=(8, 6))
    sns.barplot(x=field_accuracy_mean.index, y=field_accuracy_mean.values)
    plt.title('Field Accuracies')
    plt.xlabel('Field')
    plt.ylabel('Accuracy (%)')
    plt.ylim(0, 100)
    plt.tight_layout()
    plt.savefig('field_accuracies.png')
    plt.close()

    exam_titles_list = list(exam_title_accuracies.keys())
    exam_accuracies = []
    for title in exam_titles_list:
        correct = exam_title_accuracies[title]['correct']
        total = exam_title_accuracies[title]['total']
        accuracy = (correct / total) * 100 if total > 0 else 0
        exam_accuracies.append(accuracy)

    exam_accuracy_df = pd.DataFrame({
        'Exam Title': exam_titles_list,
        'Accuracy (%)': exam_accuracies
    }).sort_values(by='Accuracy (%)', ascending=False)

    exam_accuracy_df.to_csv('./data/exam_title_accuracies.csv', index=False)
    print("Exam title accuracies saved to 'exam_title_accuracies.csv'")

    plt.figure(figsize=(12, 6))
    sns.barplot(x='Exam Title', y='Accuracy (%)', data=exam_accuracy_df)
    plt.title('Accuracy per Exam Title')
    plt.xlabel('Exam Title')
    plt.ylabel('Accuracy (%)')
    plt.xticks(rotation=45, ha='right')
    plt.ylim(0, 100)
    plt.tight_layout()
    plt.savefig('exam_title_accuracies.png')
    plt.close()

    print("Visualizations saved as 'overall_accuracy_distribution.png', 'field_accuracies.png', and 'exam_title_accuracies.png'")


def save_incorrect_entries(results):
    incorrect_entries = []
    for entry in results:
        comparison = entry.get('comparison', {})
        overall_accuracy = comparison.get('overall_accuracy', 0)
        if overall_accuracy < 1.0:
            dir_path = entry['dir_path']
            json_file_path = entry['json_file_path']
            incorrect_entries.append({
                'dir_path': dir_path,
                'json_file': str(json_file_path),
                'overall_accuracy': overall_accuracy,
                'student_id_text_correct': comparison.get('student_id_text'),
                'exam_title_correct': comparison.get('exam_title'),
                'date_correct': comparison.get('date'),
                'exam_key_correct': comparison.get('exam_key'),
                'correct_answers': comparison.get('correct_answers'),
                'total_questions': comparison.get('total_questions')
            })

    incorrect_entries_df = pd.DataFrame(incorrect_entries)
    incorrect_entries_df.to_csv('./data/incorrect_entries.csv', index=False)
    incorrect_entries_df.to_excel('./data/incorrect_entries.xlsx', index=False)
    print("Incorrect entries saved to 'incorrect_entries.csv' and 'incorrect_entries.xlsx'")


if __name__ == "__main__":
    root_dir = "./data/exams-anon"
    results_dir = "./data/results"
    output_dir = "./data/results_with_comparison"
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(results_dir, exist_ok=True)

    data = collect_data_paths(root_dir)
    print(f"Collected data paths for {len(data)} directories.")

    existing_results = load_existing_results(results_dir)
    print(f"Loaded existing results for {len(existing_results)} entries.")

    errors = []
    total_accuracy = 0
    num_entries = 0

    results = []

    for entry in tqdm(data, desc='Processing entries'):
        dir_path = entry['dir_path']
        img_path = entry['img_path']
        log_path = entry['log_path']

        json_file_path = get_json_file_path(dir_path, results_dir)

        if dir_path in existing_results:
            entry_data, _ = existing_results[dir_path]
            inference_result = entry_data.get('inference_engine_result')
            if not inference_result:
                errors.append(f"No inference result in existing data for {dir_path}")
                continue
        else:
            image = Image.open(img_path)
            try:
                result, _ = _check_image(image)
                inference_result = result.dict()
                entry_data = {
                    "file_name": entry['file_name'],
                    "log_path": log_path,
                    "img_path": img_path,
                    "dir_path": dir_path,
                    "inference_engine_result": inference_result
                }
                with open(json_file_path, 'w') as f:
                    json.dump(entry_data, f, indent=4)
                existing_results[dir_path] = (entry_data, json_file_path)
            except Exception as e:
                print(f"Error while processing {img_path}: {e}")
                errors.append(f"Error while processing {img_path}: {e}")
                continue

        ground_truth = parse_ground_truth(log_path)
        entry_data['ground_truth'] = ground_truth

        comparison = compare_results(inference_result, ground_truth)
        entry_data['comparison'] = comparison

        total_accuracy += comparison['overall_accuracy']
        num_entries += 1

        output_json_file_path = get_json_file_path(dir_path, output_dir)
        with open(output_json_file_path, 'w') as f:
            json.dump(entry_data, f, indent=4)

        entry_data['json_file_path'] = output_json_file_path

        results.append(entry_data)

    average_accuracy = total_accuracy / num_entries if num_entries > 0 else 0
    print(f"Average accuracy over all entries: {average_accuracy * 100:.2f}%")

    if errors:
        with open('./data/errors.txt', 'w') as f:
            for error in errors:
                f.write(f"{error}\n")
        print("Errors saved to './data/errors.txt'")

    generate_visualizations(results)
    save_incorrect_entries(results)
