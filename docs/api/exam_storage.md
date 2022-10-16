# Exam storage Endpoints

Exam storage is a simple NGINX server that serves data located in its filesystem
Thanks to that any application in the same network can directly access files
stored on the server. Due to the genericity of the service, common file-system
structure restrictions had to be introduced:

## General file-system structure

```bash
/ # root directory
└── <subject_id>/<exam_id>  # exam_path
        ├── answer_key.jpeg
        ├── answer_key.json
        ├── answers
        │   └── <exam_name>.json
        └── exams
            └── <exam_name>.jpeg # exam_name
```
