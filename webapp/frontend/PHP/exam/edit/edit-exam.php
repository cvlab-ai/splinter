<?php
session_start();

use database\Database;
use navbar\NavBar;
use curl\Curl;

require("../../classes/NavBar.php");
require("../../classes/Database.php");
require("../../classes/Curl.php");
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
    <hr>
    <ul class="list-group">
        <?php
        $exams = Curl::getExams($examID);
        var_dump($exams);
        foreach ($exams as &$exam) {
            $name = $exam["name"];

            echo "<li class='list-group-item rounded d-flex justify-content-between align-items-center list-group-item-action'>";
            echo "<b>Egzamin: $name</b>";
            echo "<a style='color: white !important;' href='/exam/show-file.php?id=$examID&name=$name&isExam=true' class='badge bg-success rounded-pill'>Zobacz</a>";
            echo "<a style='color: white !important;' href='/exam/edit/edit-answers.php?examID=$examID&name=$name' class='badge bg-warning rounded-pill'>Edytuj</a>";
            echo "<a style='color: white !important;' href='/exam/edit/delete-file.php?examID=$examID&name=$name' class='badge bg-danger rounded-pill'>Usuń</a>";

            echo "</li>";
        }
        Database::disconnectDb($db);
        ?>
    </ul>
</div>
</body>
</html>
