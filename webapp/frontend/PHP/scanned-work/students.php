<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Frontend</title>
    <base href="/">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" type="image/x-icon" href="favicon.ico">
    <link rel="stylesheet" href="../css/style.css">

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet"
          integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
</head>

<body>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p"
        crossorigin="anonymous"></script>
<?php
session_start();

use navbar\NavBar;
require("../classes/NavBar.php");
echo NavBar::showNavBar("");
?>
<div class="container text-center w-25 mt-5">
<?php


$host = "host = localhost";
$port = "port = 5432";
$dbname = "dbname = splinter";
$credentials = "user = postgres password=1234";

$db = pg_connect("$host $port $dbname $credentials");
if (!$db) {
    echo "Error : Unable to open database\n";
}
$email = $_SESSION['email'];
$query = "SELECT id FROM public.user WHERE public.user.email = '$email'";
$ret = pg_query($db, $query);
if (!$ret) {
    echo pg_last_error($db);
    exit;
}
$userId = 0;
while ($row = pg_fetch_row($ret)) {
    $userId = $row[0];
}
$query = "SELECT DISTINCT student, COUNT(student)FROM exam_result LEFT JOIN EXAM E on E.id = EXAM_RESULT.exam_id WHERE e.user_id = $userId
group by student;";

$ret = pg_query($db, $query);
if (!$ret) {
    echo pg_last_error($db);
    exit;
}
// TODO odnośnik href
echo "<div class='container text-center mt-5'><h2>Lista studentów</h2><ul class='list-group'>";
while ($row = pg_fetch_row($ret)) {
    echo "<a href='/scanned-work/exam-details/student-exams.php?student=$row[0]' class='mt-2 mb-2' style='text-decoration: none;'>
            <li class='list-group-item rounded d-flex justify-content-between align-items-center list-group-item-action'>
                <b>Student: $row[0]</b>
                <span class='badge bg-success rounded-pill'>Liczba Prac: $row[1]</span>
            </li>
         </a>";
}
echo "</div></ul>"
?>
</div>

</body>
</html>
