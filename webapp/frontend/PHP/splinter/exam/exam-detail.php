<?php
session_start();

require("../classes/NavBar.php");
require("../classes/Database.php");
require("../classes/Curl.php");
require_once("../classes/Config.php");
NavBar::userIsLogged(1);
Config::header();
?>
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
    echo "<a class='btn btn-sm btn-primary btn-block m-3' href='".Config::APP_ROOT."/exam/download/download-exam.php?examID=$examID'>Pliki Do Pobrania</a>";
    echo "<a class='btn btn-sm btn-success btn-block m-3' href='".Config::APP_ROOT."/exam/download/download-csv.php?examID=$examID'>Importuj do CSV</a>";
    echo "<a class='btn btn-sm btn-warning btn-block m-3' href='".Config::APP_ROOT."/exam/edit/edit-exam.php?examID=$examID'>Edytuj Odpowiedzi</a>";
    echo "<a class='btn btn-sm btn-danger btn-block m-3' href='".Config::APP_ROOT."/exam/edit/delete-exam.php?examID=$examID'>Usuń Egzamin</a>";
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
            echo "<a style='color: white !important;' href='".Config::APP_ROOT."/exam/show-file.php?id=$examID&student=$studentIndx' class='badge bg-success rounded-pill'>Zobacz Pracę</a>";
            echo "<a style='color: white !important;' href='".Config::APP_ROOT."/exam/edit/edit-file.php?examID=$examID&index=$studentIndx' class='badge bg-warning rounded-pill'>Edytuj Pracę</a>";
            echo "<a style='color: white !important;' href='".Config::APP_ROOT."/exam/edit/delete-file.php?examID=$examID&studentIndex=$studentIndx' class='badge bg-danger rounded-pill'>Usuń Pracę</a>";

            echo "</li>";
        }
        Database::disconnectDb($db);
        ?>
    </ul>
</div>
</body>
</html>
