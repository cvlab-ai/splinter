<?php
session_start();

require("../../classes/NavBar.php");
require("../../classes/Database.php");
require("../../classes/Curl.php");
require_once("../../classes/Config.php");
NavBar::userIsLogged(2);
Config::header();
?>
<body>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p"
        crossorigin="anonymous"></script>
<?php
echo NavBar::showNavBar("scan");

$examID = $_POST['exam'];

$scanned=true;
//check-exam: examId

// check-pdf sprawdza jeden exam, examId, nazwa pliku, bez forca zignoruje

if (isset($_POST['webdav-results'])) {
    // send webdav answers keys
    for ($i = 0; $i < count($_POST['webdav-results']); $i++) {
        $fileName = $_POST['webdav-results'][$i];
        if(empty($fileName)){
            continue;
        }
        $filePath = $examID . "/answers_keys/" . basename($fileName);

        $scanned =  Curl::getWebdavFileAndUploadSplinter($fileName, $filePath);

        Curl::generateExamAnswersKeys($examID, false);
    }
}

if (isset($_POST['webdav-files'])) {
    // send webdav student work
    for ($i = 0; $i < count($_POST['webdav-files']); $i++) {
        $fileName = $_POST['webdav-files'][$i];
        if(empty($fileName)){
            continue;
        }
        $filePath = $examID . "/pdfs/" . basename($fileName);

        $scanned = Curl::getWebdavFileAndUploadSplinter($fileName, $filePath);

        Curl::generateStudentAnswers($examID);
    }
}

// send answers key
for ($i = 0; $i < count($_FILES['result']['name']); $i++) {
    // read file details
    $fileName = $_FILES['result']['name'][$i];
    if(empty($fileName)){
        continue;
    }
    $file_size = $_FILES['result']['size'][$i];
    $file_tmp = $_FILES['result']['tmp_name'][$i];
    $file_type = $_FILES['result']['type'][$i];
    $array = explode('.', $_FILES['result']['name'][$i]);
    $file_ext = strtolower(end($array));

    move_uploaded_file($file_tmp, $fileName);

    $filePath = $examID . "/answers_keys/" . basename($fileName);

    $scanned = Curl::sendFileToSplinter($fileName, $filePath);

    Curl::generateExamAnswersKeys($examID, false);
}

// send student work
for ($i = 0; $i < count($_FILES['files']['name']); $i++) {
    $fileName = $_FILES['files']['name'][$i];
    if(empty($fileName)){
        continue;
    }
    $file_size = $_FILES['files']['size'][$i];
    $file_tmp = $_FILES['files']['tmp_name'][$i];
    $file_type = $_FILES['files']['type'][$i];

    $array = explode('.', $_FILES['files']['name'][$i]);

    $file_ext = strtolower(end($array));

    move_uploaded_file($file_tmp, $fileName);
    $filePath = $examID . "/pdfs/" . basename($fileName);

    $scanned = Curl::sendFileToSplinter($fileName, $filePath);

    Curl::generateStudentAnswers($examID);
}

header("Refresh:0; url=".Config::APP_ROOT."/exam/exam-detail.php?examID=".$examID."&scanned=".$scanned);
?>
