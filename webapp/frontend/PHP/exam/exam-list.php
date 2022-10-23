<?php
session_start();

use database\Database;
use navbar\NavBar;

require("../classes/NavBar.php");
require("../classes/Database.php");
?>
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Frontend</title>
    <base href="/">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" type="image/x-icon" href="favicon.ico">

    <script src="../css/bootstrap/js/bootstrap.bundle.min.js"></script>
    <link rel="stylesheet" href="../css/bootstrap/bootstrap.min.css">
    <link rel="stylesheet" href="../css/style.css">
</head>

<body>
<?php
echo NavBar::showNavBar("main");
?>

<div class="container text-center w-25 mt-5">
    <h2>Lista egzaminów</h2>
    <hr>
    <!--TODO mała rozdzielczość-->
    <ul class="list-group">
        <?php

        $db = Database::connectToDb();

        $userID = $_SESSION['userID'];

        $sql = "SELECT id, name, date FROM exam WHERE user_id = $userID";
        $data = pg_query($db, $sql);

        while ($row = pg_fetch_row($data)) {
            $examID = $row[0];
            $examName = $row[1];
            $examDate = $row[2];
            echo "<a style='text-decoration: none;' href='/exam/exam-detail.php?examID=$examID' class='mt-2 mb-2'>
                 <li class='list-group-item d-flex rounded justify-content-between align-items-center list-group-item-action'>" . $examName .
                "<span class='badge bg-secondary rounded-pill'>Data Egzaminu: $examDate</span></li></a>";
        }

        Database::disconnectDb($db);
        ?>
    </ul>
</div>


</body>
</html>
