<?php
session_start();

require("../../classes/NavBar.php");
require("../../classes/Curl.php");
NavBar::userIsLogged(2);

$examID = $_GET['examID'];
$studentIndex = $_GET['studentIndex'];

Curl::deleteStudent($examID, $studentIndex);
?>
