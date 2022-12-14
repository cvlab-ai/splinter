<?php
session_start();
use curl\Curl;
use navbar\NavBar;
require("../../classes/NavBar.php");
NavBar::userIsLogged(2);
require("../../classes/Curl.php");

$examID = $_GET['examID'];
$studentIndex = $_GET['studentIndex'];

Curl::deleteStudent($examID, $studentIndex);
?>