<?php

class Config
{
    const EXAM_STORAGE_URL = 'http://splinter-exam-storage:81/splinter-data/';
    const ZIP_URL = 'http://splinter-exam-storage:81/splinter-data/zip/';
    const UPLOADS_URL = 'http://splinter-exam-storage:80/splinter/uploads/';
    const INFERENCE_URL = 'http://splinter-inference-engine:8000/';
    const APP_ROOT = "/splinter";
    
    public static function header(){?>
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Splinter</title>
        <base href="<?=self::APP_ROOT?>">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="icon" type="image/x-icon" href="<?=self::APP_ROOT?>/favicon.ico">

        <link rel="stylesheet" href="<?=self::APP_ROOT?>/css/bootstrap.min.css">
        <link rel="stylesheet" href="<?=self::APP_ROOT?>/css/style.css">
        <script src="<?=self::APP_ROOT?>/css/js/bootstrap.bundle.min.js"></script>
    </head>
    <?php
    }
}
