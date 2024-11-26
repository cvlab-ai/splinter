import json
import os
from pathlib import Path

from PIL import Image
from tqdm import tqdm

from src.controller import _check_image


def collect_data_paths(root_dir):
    root_dir = Path(root_dir)
    data = []

    directories = [p for p in root_dir.rglob('*') if p.is_dir()]
    for dirpath in tqdm(directories, desc='Processing directories'):
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


def save_metadata_to_catalog(results, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for idx, result in enumerate(results):
        result_file = output_dir / f"result_{idx + 1}.json"
        with open(result_file, 'w') as f:
            json.dump(result, f, indent=4)

        print(f"Saved result to {result_file}")


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
                else:
                    pass
            elif key.startswith('question '):
                q_num = key[9:]
                ground_truth['answers'][q_num.lstrip('0')] = value
            else:
                ground_truth[key] = value
    ground_truth['student_id_text'] = ''.join(student_id_digits)
    ground_truth['student_id_boxes'] = ground_truth['student_id_text']
    return ground_truth


def compare_results(inference_result, ground_truth):
    comparison = {}
    comparison['student_id_text'] = (inference_result['student_id_text'] == ground_truth['student_id_text'])
    comparison['exam_title'] = (inference_result['exam_title'] == ground_truth['exam_title'])
    comparison['date'] = (inference_result['date'] == ground_truth['date'])
    gt_exam_key = answer_string_to_list(ground_truth['key']) if ground_truth['key'] else [0, 0, 0, 0]
    comparison['exam_key'] = (inference_result['exam_key'] == gt_exam_key)
    total_questions = len(ground_truth['answers'])
    correct_answers = 0
    per_question_accuracy = {}
    for q_num_str, gt_answer_str in ground_truth['answers'].items():
        gt_answer_list = answer_string_to_list(gt_answer_str)
        inf_answer_list = inference_result['answers'].get(q_num_str)
        if inf_answer_list is None:
            per_question_accuracy[q_num_str] = False
        else:
            is_correct = (inf_answer_list == gt_answer_list)
            per_question_accuracy[q_num_str] = is_correct
            if is_correct:
                correct_answers += 1
    comparison['per_question_accuracy'] = per_question_accuracy
    comparison['overall_accuracy'] = correct_answers / total_questions if total_questions > 0 else 0
    return comparison


def load_existing_results(results_dir):
    existing_results = {}
    json_files = list(Path(results_dir).glob('result_*.json'))
    for json_file in json_files:
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            dir_path = data.get('dir_path')
            if dir_path:
                existing_results[dir_path] = data
        except Exception as e:
            print(f"Error loading {json_file}: {e}")
            continue
    return existing_results


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

    idx = 0

    for entry in tqdm(data, desc='Processing entries'):
        dir_path = entry['dir_path']
        img_path = entry['img_path']
        log_path = entry['log_path']

        if dir_path in existing_results:
            entry_data = existing_results[dir_path]
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
                idx += 1
                result_file = Path(results_dir) / f"result_{idx}.json"
                with open(result_file, 'w') as f:
                    json.dump(entry_data, f, indent=4)
                existing_results[dir_path] = entry_data
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

        output_file = Path(output_dir) / f"result_{idx}.json"
        with open(output_file, 'w') as f:
            json.dump(entry_data, f, indent=4)

    average_accuracy = total_accuracy / num_entries if num_entries > 0 else 0
    print(f"Average accuracy over all entries: {average_accuracy * 100:.2f}%")

    if errors:
        with open('data/errors.txt', 'w') as f:
            for error in errors:
                f.write(f"{error}\n")

        print(f"Errors saved to data/errors.txt")
