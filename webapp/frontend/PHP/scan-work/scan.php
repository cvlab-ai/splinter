<?php
session_start();
?>
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Frontend</title>
    <base href="/">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" type="image/x-icon" href="favicon.ico">
    <link rel="stylesheet" href="../css/style.css">

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet"
          integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
</head>

<body>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p"
        crossorigin="anonymous"></script>

<?php

use navbar\NavBar;

require("../classes/NavBar.php");
echo NavBar::showNavBar("scan");

$host = "host = splinter_db";
$port = "port = 5432";
$dbname = "dbname = splinter";
$credentials = "user = postgres password=1234";

$db = pg_connect("$host $port $dbname $credentials");
if (!$db) {
    echo "Error : Unable to open database\n";
}

if (isset($_POST["submit-btn"])) {
    $subject_id = $_POST['subject'];
    $exam_id = $_POST['exam'];
    //$files = $_POST['files'];

    for ($i = 0; $i < count($_FILES['result']['name']); $i++) {
        $file_name = $_FILES['result']['name'][$i];
        $file_size = $_FILES['result']['size'][$i];
        $file_tmp = $_FILES['result']['tmp_name'][$i];
        $file_type = $_FILES['result']['type'][$i];
        $array = explode('.', $_FILES['result']['name'][$i]);
        $file_ext = strtolower(end($array));

        move_uploaded_file($file_tmp, "answer_key.jpg");
        $email = $_SESSION['email'];
        $filePath = $subject_id . "/" . $exam_id . "/" . basename("answer_key.jpg");

        // Upload file to exam storage
        $c = curl_init();
        curl_setopt($c, CURLOPT_URL, "http://splinter_exam_storage/" . $filePath);
        curl_setopt($c, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($c, CURLOPT_PUT, true);
        curl_setopt($c, CURLOPT_INFILESIZE, filesize("answer_key.jpg"));
        curl_setopt($c, CURLOPT_BINARYTRANSFER, TRUE);
        $fp = fopen("answer_key.jpg", "r");
        curl_setopt($c, CURLOPT_INFILE, $fp);
        curl_exec($c);
        curl_close($c);
        fclose($fp);
        unlink($file_name);

        $query = "INSERT INTO exam_result_files (file_name, file_path, exam_id) VALUES ('answer_key.jpg','$filePath', $exam_id)";
        $res = pg_query($db, $query);
        if (!$res) {
            echo pg_last_error($db);
            exit;
        }

        // send curl to read correct answers
        $ch = curl_init();

        curl_setopt($ch, CURLOPT_URL, "http://splinter_inference_engine:8000/generate-exam-key");
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, '{ "exam_path": "/' . $subject_id . '/' . $exam_id . '/" }');
        curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));

        $result = curl_exec($ch);
        curl_close($ch);
    }

    for ($i = 0; $i < count($_FILES['files']['name']); $i++) {
        $file_name = $_FILES['files']['name'][$i];
        $file_size = $_FILES['files']['size'][$i];
        $file_tmp = $_FILES['files']['tmp_name'][$i];
        $file_type = $_FILES['files']['type'][$i];
        $array = explode('.', $_FILES['files']['name'][$i]);
        $file_ext = strtolower(end($array));

        move_uploaded_file($file_tmp, $file_name);
        $filePath = $subject_id . "/" . $exam_id . "/exams/" . basename($file_name);
        // Upload file to exam storage
        $c = curl_init();
        curl_setopt($c, CURLOPT_URL, "http://splinter_exam_storage/" . $filePath);
        curl_setopt($c, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($c, CURLOPT_PUT, true);
        curl_setopt($c, CURLOPT_INFILESIZE, filesize($file_name));
        curl_setopt($c, CURLOPT_BINARYTRANSFER, TRUE);
        $fp = fopen($file_name, "r");
        curl_setopt($c, CURLOPT_INFILE, $fp);
        curl_exec($c);
        curl_close($c);
        fclose($fp);
        unlink($file_name);

        $query = "INSERT INTO exam_files (file_name, file_path, exam_id, students_work) VALUES ('$file_name','$filePath', $exam_id, true)";
        $res = pg_query($db, $query);
        if (!$res) {
            echo pg_last_error($db);
            exit;
        }


        // send curl to read correct answers
        $ch = curl_init();

        curl_setopt($ch, CURLOPT_URL, "http://splinter_inference_engine:8000/check-exam");
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, '{ "exam_path": "/' . $subject_id . '/' . $exam_id . '/", "exam_name": "'.$file_name.'" }');
        curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));

        $result = curl_exec($ch);
        curl_close($ch);

        // create a new cURL resource
        $ch = curl_init();

        // set URL and other appropriate options
        curl_setopt($ch, CURLOPT_URL, 'http://splinter_exam_storage/'.$subject_id . "/" . $exam_id ."/answers/".explode(".jpg",$file_name)[0].".json");
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_HEADER, 0);

        // grab URL and pass it to the browser
        $out = curl_exec($ch);

        // close cURL resource, and free up system resources
        curl_close($ch);


        $fp = fopen(explode(".jpg",$file_name)[0].'.json', 'w');
        fwrite($fp, $out);
        fclose($fp);

        $strJsonFileContents = file_get_contents(explode(".jpg",$file_name)[0].'.json');
        $array = json_decode($strJsonFileContents, true);

        $studentIndex = $array["index"];

        $answerArray = $array["answers"];

        $answersNumber = count($answerArray);
        $points = 0;

        for ($j = 1; $j <= $answersNumber; $j++) {
            for ($z = 0; $z < count($answerArray[$j]); $z++) {
                if ($answerArray[$j][$z] == 1) {
                    $points++;
                }
            }
        }

        $sql = "INSERT INTO exam_result (max_score, score, student, exam_id)  VALUES ('40','$points','$studentIndex',$exam_id)";
        $ret = pg_query($db, $sql);
    }
}

pg_close($db);
header("Refresh:0; url=/scanned-work/exams.php");
?>


</body>
</html>
