<?php
session_start();

require("../../classes/NavBar.php");
require("../../classes/Database.php");
require("../../classes/Curl.php");
require_once("../../classes/Config.php");
NavBar::userIsLogged(2);
Config::header();
?>
<body>
<?php
echo NavBar::showNavBar("exam");

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
    <h2>Nazwa Egzaminu: <?php echo $examName ?></h2>
    <hr>
    <h4>Skany poprawynych odpowiedzi</h4>
    <p class='fw-light text-muted'>Tutaj znajdziesz zeskanowane klucze odpowiezi.</p>
    <p class='fw-light text-muted'>Pamiętaj, że zawsze brany pod uwagę jest ostatni zeskanowany plik.</p>
    <p class='fw-light text-muted'>W przypadku gdy mamy dw apliki o tej samej nazwie: answers_b_1 i answers_b_2, odpowiedzi są zczytywane z pliku o wyższym numerze.</p>
    <hr>
    <a class="btn btn-sm btn-success btn-block m-2" href="<?=Config::APP_ROOT ?>/exam/scan/select-file.php">Dodaj skan poprawnych odpowiedzi egzaminu</a></br>
    <ul class="list-group">
        <?php
        $exams = Curl::getExams($examID);
        
        if (count($exams) < 1) {
            echo "<li class='list-group-item'>";
            echo '<h4>Brak zeskanowanych odpowiedzi!</h4>';
            echo "</li>";
        } else {
            foreach ($exams as &$exam) {
                $name = $exam["name"];
    
                echo "<li class='list-group-item rounded d-flex justify-content-between align-items-center list-group-item-action'>";
                echo "<b>Egzamin: $name</b>";
                echo "<a style='color: white !important;' href='".Config::APP_ROOT."/exam/show-file.php?id=$examID&name=$name&isExam=true' class='badge bg-success rounded-pill'>Zobacz</a>";
                echo "<a style='color: white !important;' href='".Config::APP_ROOT."/exam/edit/edit-answers.php?examID=$examID&name=$name' class='badge bg-warning rounded-pill'>Edytuj</a>";
                echo "<a style='color: white !important;' href='".Config::APP_ROOT."/exam/edit/delete-correct-ans.php?examID=$examID&name=$name' class='badge bg-danger rounded-pill' onClick='return confirm(\"Czy na pewno chcesz usunąć odpwoiedzi egzaminu?\");'>Usuń</a>";
    
                echo "</li>";
            }
        }

        Database::disconnectDb($db);
        ?>
    </ul>
</div>
</body>
</html>
