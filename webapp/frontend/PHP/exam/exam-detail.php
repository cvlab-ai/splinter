<?php
session_start();

use database\Database;
use navbar\NavBar;
use curl\Curl;

require("../classes/NavBar.php");
NavBar::userIsLogged(1);
require("../classes/Database.php");
require("../classes/Curl.php");
?>
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Frontend</title>
    <base href="/">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" type="image/x-icon" href="favicon.ico">

    <link rel="stylesheet" href="../css/bootstrap.min.css">
    <link rel="stylesheet" href="../css/style.css">
    <script src="../css/js/bootstrap.bundle.min.js"></script>
</head>

<body>
<?php
echo NavBar::showNavBar("main");

$db = Database::connectToDb();

echo '<div class="container text-center w-25 mt-5">';

$examID = $_GET['examID'];
$userID = $_SESSION['userID'];

$sql = "SELECT * FROM exam WHERE user_id = $userID AND id = $examID";

$ret = pg_query($db, $sql);
if (!$ret) {
    echo pg_last_error($db);
    exit;
}

$row = pg_fetch_row($ret);

$examName = $row[1];
?>

<div class="container text-center mt-5">
    <h2><?php echo $examName ?></h2>
    <?php
    echo "<a class='btn btn-sm btn-primary btn-block m-3' href='/exam/download/download-exam.php?examID=$examID'>Pliki Do Pobrania</a>";
    echo "<a class='btn btn-sm btn-success btn-block m-3' href='/exam/download/download-csv.php?examID=$examID'>Importuj do CSV</a>";
    echo "<a class='btn btn-sm btn-warning btn-block m-3' href='/exam/edit/edit-exam.php?examID=$examID'>Edytuj Odpowiedzi</a>";
    echo "<a class='btn btn-sm btn-danger btn-block m-3' href='/exam/edit/delete-exam.php?examID=$examID'>Usuń Egzamin</a>";
    ?>
    <hr>
    <ul class="list-group">
        <?php
        $students = Curl::searchExamPathForStudents($examID);

        foreach ($students as &$student) {
            $studentIndx = $student["name"];
            $examResult = Curl::getExamResult($examID, $studentIndx);
            echo "<li class='list-group-item rounded d-flex justify-content-between align-items-center list-group-item-action'>";
            echo "<b>Student:$studentIndx</b>";
            echo "<a style='color: white !important;' href='/exam/show-file.php?id=$examID&student=$studentIndx' class='badge bg-success rounded-pill'>Zobacz Pracę</a>";
            echo "<a style='color: white !important;' href='/exam/edit/edit-file.php?examID=$examID&index=$studentIndx' class='badge bg-warning rounded-pill'>Edytuj Pracę</a>";
            echo "<a style='color: white !important;' href='/exam/edit/delete-file.php?examID=$examID&studentIndex=$studentIndx' class='badge bg-danger rounded-pill'>Usuń Pracę</a>";

            echo "</li>";
        }
        Database::disconnectDb($db);
        ?>
    </ul>
</div>
</body>
</html>
