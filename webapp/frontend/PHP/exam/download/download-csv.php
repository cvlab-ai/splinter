<?php
session_start();
use navbar\NavBar;
require("../../classes/NavBar.php");
NavBar::userIsLogged(2);

$examID = $_GET['examID'];

$exam_storage_user = "splinter";
$exam_storage_password = "1234";

$ch = curl_init();
$userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36';
curl_setopt($ch, CURLOPT_HEADER, 0);
curl_setopt($ch, CURLOPT_VERBOSE, 0);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_USERPWD, $exam_storage_user . ":" . $exam_storage_password);
curl_setopt($ch, CURLOPT_URL, 'http://splinter_exam_storage/splinter/'.$examID.'/scores.csv');
curl_setopt($ch, CURLOPT_USERAGENT, $userAgent);
$output = curl_exec($ch);
curl_close($ch);

header('Content-Disposition: attachment; filename="scores.csv";');
header('Content-Type: application/csv; charset=UTF-8');
echo $output;
?>