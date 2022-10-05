<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Frontend</title>
    <base href="/">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" type="image/x-icon" href="favicon.ico">
    <link rel="stylesheet" href="../../css/style.css">

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet"
          integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
    <script type="text/javascript">
        function popupWindow(examId, fileId, isResultFile) {
            console.log(isResultFile)
            var answer = window.confirm("Usunąć plik?");
            if (answer) {
                alert("Usunięto!")
                if (isResultFile) {
                    window.location.replace("/scanned-work/exam-details/edit-exam/delete-exam.php?id=" + examId + "&fileId=" + fileId+"&result=true")
                } else {
                    window.location.replace("/scanned-work/exam-details/edit-exam/delete-exam.php?id=" + examId + "&fileId=" + fileId+"&result=false")
                }

            }
        }


    </script>
</head>

<body>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p"
        crossorigin="anonymous"></script>

<?php

use navbar\NavBar;

require("../../classes/NavBar.php");
echo NavBar::showNavBar("");
?>

<div class="container text-center w-25 mt-5">
    <?php
    session_start();
    $host = "host = splinter_db";
    $port = "port = 5432";
    $dbname = "dbname = splinter";
    $credentials = "user = postgres password=1234";

    $db = pg_connect("$host $port $dbname $credentials");
    if (!$db) {
        echo "Error : Unable to open database\n";
    }

    $exam_id = $_GET['id'];
    $email = $_SESSION['email'];
    $sql = "SELECT * from exam_files WHERE exam_id = $exam_id";

    $ret = pg_query($db, $sql);
    if (!$ret) {
        echo pg_last_error($db);
        exit;
    }
    ?>


    <div class="container mt-5">
        <h2>Pliki Do Pobrania</h2>
        <hr>
        <ul class="list-group">
            <?php
            while ($row = pg_fetch_row($ret)) {
                $params = $row[0] . "," . $exam_id.",false";
                echo "<div><a class='btn btn-lg btn-primary btn-block m-3' href='/scan-work/$row[2]'>$row[1]</a><a class='btn btn-lg btn-danger btn-block m-1' onclick='popupWindow($params)'>Usuń Plik</a></div><hr>";
            }

            $sql = "SELECT * from exam_result_files WHERE exam_id = $exam_id";

            $ret = pg_query($db, $sql);
            if (!$ret) {
                echo pg_last_error($db);
                exit;
            }

            while ($row = pg_fetch_row($ret)) {
                $params = $row[0] . "," . $exam_id.",true";
                echo "<div><a class='btn btn-lg btn-primary btn-block m-3' href='/scan-work/$row[2]'>$row[1]</a><a class='btn btn-lg btn-danger btn-block m-1' onclick='popupWindow($params)'>Usuń Plik</a></div><hr>";
            }
            pg_close($db);
            ?>
        </ul>
    </div>
</body>
</html>
