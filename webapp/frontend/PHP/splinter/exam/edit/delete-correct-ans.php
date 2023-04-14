<?php
session_start();

require("../../classes/NavBar.php");
require("../../classes/Curl.php");
NavBar::userIsLogged(2);

$examID = $_GET['examID'];
$fileName = $_GET['name'];

Curl::deleteExamFile($examID, $fileName);
?>
