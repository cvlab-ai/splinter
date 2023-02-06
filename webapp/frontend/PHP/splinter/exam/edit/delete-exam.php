<?php
session_start();

require("../../classes/NavBar.php");
require("../../classes/Curl.php");
require("../../classes/Database.php");
NavBar::userIsLogged(2);

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
