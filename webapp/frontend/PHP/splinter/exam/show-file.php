<?php
session_start();

require ("../classes/NavBar.php");
require ("../classes/Curl.php");
require_once ("../classes/Config.php");
NavBar::userIsLogged(1);

$examID = $_GET["id"];

$exam_storage_user =  getenv('EX_STORE_SPLINTER_USER');
$exam_storage_password = getenv('EX_STORE_SPLINTER_PASS');

$index = 0;

$answersUrlParam = "answers";

if (isset($_GET['student'])) {
    $index = $_GET["student"];
    $numOfAnswers = (Curl::getNumOfAnswers($examID,$index) / 2);
    if ($numOfAnswers > 0) {
        $answersUrlParam = "answers_".$numOfAnswers;
    }
} else {
    $numOfAnswers = (count(Curl::getExams($examID)) / 2);
    $answersUrlParam= str_replace(".json", "",$_GET['name']);
}




if (isset($_GET['student'])) { // show exam answer if student not set
    $url = Config::EXAM_STORAGE_URL.$examID."/students/".$index."/".$answersUrlParam.".jpg";
} else {
    $url = Config::EXAM_STORAGE_URL.$examID."/answers_keys/".$answersUrlParam.".jpg";
}

$ch = curl_init();
$userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36';
curl_setopt($ch, CURLOPT_HEADER, 0);
curl_setopt($ch, CURLOPT_VERBOSE, 0);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_USERPWD, $exam_storage_user . ":" . $exam_storage_password);
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_USERAGENT, $userAgent);
$output = curl_exec($ch);
curl_close($ch);

header('Content-type: image/jpeg');
echo $output;
?>
