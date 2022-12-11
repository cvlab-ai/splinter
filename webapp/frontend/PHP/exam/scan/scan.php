<?php
session_start();

use database\Database;
use navbar\NavBar;
use curl\Curl;

require("../../classes/NavBar.php");
NavBar::userIsLogged(2);
require("../../classes/Database.php");
require("../../classes/Curl.php");
?>
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Frontend</title>
    <base href="/">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" type="image/x-icon" href="favicon.ico">
    <link rel="stylesheet" href="../../css/style.css">

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet"
          integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3"
          crossorigin="anonymous">
</head>

<body>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p"
        crossorigin="anonymous"></script>
<?php
echo NavBar::showNavBar("scan");

$examID = $_POST['exam'];

//check-exam: examId

// check-pdf sprawdza jeden exam, examId, nazwa pliku, bez forca zignoruje

// generate-exam-keys: examId
$exam_storage_user =  getenv('POSTGRES_DB');
$exam_storage_password = getenv('POSTGRES_PASSWORD');

for ($i = 0; $i < count($_FILES['result']['name']); $i++) {
    // read file details
    $file_name = $_FILES['result']['name'][$i];
    if(empty($file_name)){
        continue;
    }
    $file_size = $_FILES['result']['size'][$i];
    $file_tmp = $_FILES['result']['tmp_name'][$i];
    $file_type = $_FILES['result']['type'][$i];
    $array = explode('.', $_FILES['result']['name'][$i]);
    $file_ext = strtolower(end($array));

    move_uploaded_file($file_tmp, $file_name);

    $filePath = $examID . "/answers_keys/" . basename($file_name);

    // Upload file to exam storage
    $c = curl_init();
    curl_setopt($c, CURLOPT_URL, "http://splinter_exam_storage/splinter/" . $filePath);
    curl_setopt($c, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($c, CURLOPT_PUT, true);
    curl_setopt($c, CURLOPT_INFILESIZE, filesize($file_name));
    curl_setopt($c, CURLOPT_BINARYTRANSFER, TRUE);
    curl_setopt($c, CURLOPT_USERPWD, $exam_storage_user . ":" . $exam_storage_password);
    $fp = fopen($file_name, "r");

    curl_setopt($c, CURLOPT_INFILE, $fp);
    curl_exec($c);
    curl_close($c);
    fclose($fp);
    unlink($file_name);

    // send curl to generate correct answers
    $ch = curl_init();

    curl_setopt($ch, CURLOPT_URL, "http://splinter_inference_engine:8000/generate-exam-keys");
    curl_setopt($ch, CURLOPT_USERPWD, $exam_storage_user . ":" . $exam_storage_password);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, '{ "examId": "' .  $examID . '", "force":true }');
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));

    $result = curl_exec($ch);
    curl_close($ch);
}

for ($i = 0; $i < count($_FILES['files']['name']); $i++) {
    $file_name = $_FILES['files']['name'][$i];
    if(empty($file_name)){
        continue;
    }
    $file_size = $_FILES['files']['size'][$i];
    $file_tmp = $_FILES['files']['tmp_name'][$i];
    $file_type = $_FILES['files']['type'][$i];

    $array = explode('.', $_FILES['files']['name'][$i]);

    $file_ext = strtolower(end($array));

    move_uploaded_file($file_tmp, $file_name);
    $filePath = $examID . "/pdfs/" . basename($file_name);

    // Upload file to exam storage
    $c = curl_init();
    curl_setopt($c, CURLOPT_URL, "http://splinter_exam_storage/splinter/" . $filePath);
    curl_setopt($c, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($c, CURLOPT_PUT, true);
    curl_setopt($c, CURLOPT_INFILESIZE, filesize($file_name));
    curl_setopt($c, CURLOPT_BINARYTRANSFER, TRUE);
    $fp = fopen($file_name, "r");
    curl_setopt($c, CURLOPT_INFILE, $fp);
    curl_setopt($c, CURLOPT_USERPWD, $exam_storage_user . ":" . $exam_storage_password);
    curl_exec($c);
    curl_close($c);
    fclose($fp);

    // send curl to read correct answers
    $ch = curl_init();

    curl_setopt($ch, CURLOPT_URL, "http://splinter_inference_engine:8000/check-exam");
    curl_setopt($ch, CURLOPT_USERPWD, $exam_storage_user . ":" . $exam_storage_password);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, '{ "examId": "' . $examID .'", "force":true }');
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));

    $result = curl_exec($ch);
    curl_close($ch);
}

header("Refresh:0; url=/exam/exam-list.php");
?>
