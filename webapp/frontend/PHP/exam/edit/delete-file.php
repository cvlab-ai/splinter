<?php
session_start();
use curl\Curl;
require("../../classes/Curl.php");

$examID = $_GET['examID'];
$studentIndex = $_GET['studentIndex'];

Curl::deleteStudent($examID, $studentIndex);
?>