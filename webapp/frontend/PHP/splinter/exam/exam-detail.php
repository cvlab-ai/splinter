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
echo NavBar::showNavBar("exam");

if (isset($_GET['scanned'])) {
    if ($_GET['scanned']== 1) {
        echo '<script language="javascript">';
        echo 'alert("Pomyślnie zeskanowano plik/i!")';
        echo '</script>';
    } else {
        echo '<script language="javascript">';
        echo 'alert("Nie udało się zeskanować pliku/ów")';
        echo '</script>';
    }
}

$db = Database::connectToDb();

echo '<div class="container text-center w-25 mt-5">';

$examID = $_GET['examID'];
$userID = $_SESSION['userID'];
$_SESSION['exam'] = $examID;
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
    <h3>Nazwa Egzaminu <?php echo $examName ?></h3>
    <p class='fw-light text-muted'>Tutaj możesz sprawdzić zeskanowane egzaminy i klucze odpowiedzić</p>
    <?php
    echo "<a class='btn btn-sm btn-primary btn-block m-2' href='".Config::APP_ROOT."/exam/download/download-exam.php?examID=$examID'>Pobierz pliki egzaminu</a></br>";
    echo "<a class='btn btn-sm btn-success btn-block m-2' href='".Config::APP_ROOT."/exam/download/download-csv.php?examID=$examID'>Eksportuj wyniki egzaminu do CSV</a></br>";
    echo "<a class='btn btn-sm btn-warning btn-block m-2' href='".Config::APP_ROOT."/exam/edit/edit-exam.php?examID=$examID'>Edytuj Odpowiedzi</a></br>";
    ?>
    <a class="btn btn-sm btn-danger btn-block m-2" href="<?=Config::APP_ROOT ?>/exam/edit/delete-exam.php?examID=<?=$examID ?>" onClick="return confirm('Czy na pewno chcesz usunąć egzamin?');">Usuń Egzamin <?=$examName ?> </a>
    
    <p class='fw-light text-muted'>Możesz też usuwać/edytować pliki lub pobrać wyniki do pliku CSV.</p>
    <hr>
    <h4>Zeskanowane odpowiedzi studentów</h4>
    <p class='fw-light text-muted'>Poniżej znajdziesz zeskanowane prace studentów.</p>
    
    <p class='fw-light text-muted'>Ponowne wgranie prac studentów spowoduje ponowne sprawdzenie i nadpisanie wyniku.</p>

    <a class="btn btn-sm btn-success btn-block m-2" href="<?=Config::APP_ROOT ?>/exam/scan/select-file.php">Dodaj skan egzaminu</a></br>
    <ul class="list-group">
        <?php
        $students = Curl::searchExamPathForStudents($examID);
        if ($students == null) {
            echo "<li class='list-group-item'>";
            echo '<h4>Brak zeskanowanych prac!</h4>';
            echo "</li>";
        } else {
            foreach ($students as &$student) {
                $studentIndx = $student["name"];
                $examResult = Curl::getExamResult($examID, $studentIndx);
                echo "<li class='list-group-item'>";
                echo "<b>Student: $studentIndx</b></br>";
                echo "<a style='color: white !important;' href='".Config::APP_ROOT."/exam/show-file.php?id=$examID&student=$studentIndx' class='badge bg-success rounded-pill m-1'>Zobacz pracę</a>";
                echo "<a style='color: white !important;' href='".Config::APP_ROOT."/exam/edit/delete-file.php?examID=$examID&studentIndex=$studentIndx' class='badge bg-danger rounded-pill m-1' onClick='return confirm(\"Czy na pewno chcesz usunąć pracę?\");'>Usuń pracę</a>";
                echo "</li>";
            }
        }

        Database::disconnectDb($db);
        ?>
    </ul>
</div>
</body>
</html>
