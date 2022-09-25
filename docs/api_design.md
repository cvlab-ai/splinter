# API Design

This docuement is a note from team design session and describes planned
communication between web application (backend) and internal logic
services(inference_engine + exam_storage).

## Web Application requests to Exam Storage

```py
send_exam_image(exam_name, exam_path, binary_exam) -> bool_received, non-overwritting
send_exam_key(exam_path) -> bool_received, overwritting
check_exam_exists(exam_name, exam_path) -> b_size
request_exam_answers(exam_name, exam_path) -> json-like tree or 400
enforce_answer_change(exam_path, exam_name, question_id, correct_value) -> status or 400
delete_exam(exam_path, exam_name) -> status
```

## Web Application requests to Inference Engine

```py
check_exams(exam_path) -> count
check_exam(exam_path, exam_name) -> status
generate_exam_key(exam_path) -> status
```

## Inference Engine requests to Exam Storage

```py
get_exams_names(exam_path) -> relative_paths
get_exam_image(exam_path, exam_name) -> binary_exam or 400
get_answer_key_image(exam_path) -> binary_answer_key or 400
set_answer_key_json(exam_path, json_value) -> status
set_exam_answers_json(exam_path, exam_name, json_value) -> status
```

## Exam Storage filesystem structure

```bash
splinter/ # root directory
└── KSS/first_term  # exam_path
        ├── answer_key.jpeg
        ├── answer_key.json
        ├── answers
        │   └── 123456.json
        └── exams
            └── 123456.jpeg # exam_name
```
