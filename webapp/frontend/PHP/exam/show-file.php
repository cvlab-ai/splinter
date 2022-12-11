<?php
session_start();

use navbar\Navbar;
require ("../classes/NavBar.php");
NavBar::userIsLogged(1);

use curl\Curl;
require ("../classes/Curl.php");

$examID = $_GET["id"];

$exam_storage_user = "splinter";
$exam_storage_password = "1234";

$index = 0;

$answersUrlParam = "answers";

if (isset($_GET['student'])) {
    $index = $_GET["student"];
    $numOfAnswers = (Curl::getNumOfAnswers($examID,$index) / 2) - 1;
    if ($numOfAnswers > 0) {
        $answersUrlParam = "answers_".$numOfAnswers;
    }
} else {
    $numOfAnswers = (count(Curl::getExams($examID)) / 2) - 1;
    $answersUrlParam= str_replace(".json", "",$_GET['name']);
}




if (isset($_GET['student'])) {
    $url ='http://splinter_exam_storage/splinter/'.$examID."/students/".$index."/".$answersUrlParam.".jpg";
} else {
    $url ='http://splinter_exam_storage/splinter/'.$examID."/answers_keys/".$answersUrlParam.".jpg";
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