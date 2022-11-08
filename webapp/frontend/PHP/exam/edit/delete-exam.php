<?php
session_start();

use curl\Curl;
use database\Database;

require("../../classes/Curl.php");
require("../../classes/Database.php");

$examID = $_GET['examID'];
$db = Database::connectToDb();

$sql = "DELETE FROM exam WHERE id = $examID";
$res = pg_query($db, $sql);
if (!$res) {
    echo pg_last_error($db);
    exit;
}

Database::disconnectDb($db);
Curl::deleteExam($examID);
?>