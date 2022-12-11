<?php
session_start();

use navbar\Navbar;
require("../../classes/NavBar.php");
NavBar::userIsLogged(2);

// generate-exam-keys: examId
$exam_storage_user = "splinter";
$exam_storage_password = "1234";

$examID = $_POST['examID'];
$index = $_POST['index'];

$file_name = $_FILES['files']['name'];
$file_size = $_FILES['files']['size'];
$file_tmp = $_FILES['files']['tmp_name'];
$file_type = $_FILES['files']['type'];

$array = explode('.', $_FILES['files']['name']);

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

curl_setopt($ch, CURLOPT_URL, "http://splinter_inference_engine:8000/check-pdf");
curl_setopt($ch, CURLOPT_USERPWD, $exam_storage_user . ":" . $exam_storage_password);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, '{ "examId": "' . $examID . '", "file_name": "'.$file_name.'", "force": true }');
curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));

$result = curl_exec($ch);
curl_close($ch);


header("Refresh:0; url=/exam/exam-detail.php?examID=".$examID);
?>
