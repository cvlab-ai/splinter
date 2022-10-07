<?php
session_start();
?>
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
</head>

<body>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p"
        crossorigin="anonymous"></script>
<?php
use navbar\NavBar;
use database\Database;
require ("../../classes/NavBar.php");
require ("../../classes/Database.php");

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

    $exam_id = $_GET['id'];

    $email = $_SESSION['email'];
    $userId = Database::getUserIDByEmail($db, $email);
    $sql = "SELECT * from EXAM WHERE user_id = $userId AND exam.id = $exam_id";


    $ret = pg_query($db, $sql);
    if (!$ret) {
        echo pg_last_error($db);
        exit;
    }
    $row = pg_fetch_row($ret);
    ?>


    <div class="container text-center mt-5">
        <h2><?php echo $row[1] ?></h2>
        <?php
        echo "<a class='btn btn-sm btn-primary btn-block m-3' href='/scanned-work/exam-details/exam-details-files.php?id=$exam_id'>Pliki Do Pobrania</a>"
        ?>
        <a class="btn btn-sm btn-warning btn-block m-3" routerLink="/editExam/{{examId}}">Edytuj odpowiedzi</a>
        <hr>
        <ul class="list-group">
            <?php
            $sql = "SELECT * from exam_result WHERE exam_id = $exam_id";
            $ret = pg_query($db, $sql);
            if (!$ret) {
                echo pg_last_error($db);
                exit;
            }
            while ($row = pg_fetch_row($ret)) {
                echo "<a style='text-decoration: none;' href='/scanned-work/exam-details/student-exams.php?student=$row[4]' class='mt-2 mb-2'>
                        <li class='list-group-item rounded d-flex justify-content-between align-items-center list-group-item-action'>
                        <b>Student: $row[4]</b>";
                if ($row[3] <= $row[2]) {
                    echo "<span class='badge bg-success rounded-pill'>Wynik: $row[3] / $row[2]</span>";
                } else {
                    echo "<span class='badge bg-danger rounded-pill'>Wynik: $row[3] / $row[2]</span>";
                }
                echo "</li></a>";
            }
            pg_close($db);
            ?>
        </ul>
    </div>
</body>
</html>
