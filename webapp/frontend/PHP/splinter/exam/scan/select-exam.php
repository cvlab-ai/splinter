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
echo NavBar::showNavBar("scan");
$db = Database::connectToDb();

$userID = $_SESSION['userID'];

$sql = "SELECT id, name FROM exam WHERE user_id = $userID";
$data = pg_query($db, $sql);

?>

<div class="container text-center w-25 mt-5">
    <div class="mb-3">
        <label for="select" class="form-label"><h2>Wybór Egzaminu</h2></label>
        <p class='fw-light text-muted'>Wybierz egzamin i następnie przejdź dalej do wyboru pliku ze skanami egzaminów</p>
        <form method="post" action="<?=Config::APP_ROOT?>/exam/scan/select-file.php">
            <select id="select" class="form-select" name="exam">
                <?php
                while ($row = pg_fetch_row($data)) {
                    $examID = $row[0];
                    $examName = $row[1];
                    echo "<option value='$examID'>$examName</option>";
                }
                ?>
            </select>
            <input type="submit" class="btn btn-sm btn-primary btn-block mt-3" value="Wybór Plików" name="submit-btn">
        </form>
        <p class='fw-light text-muted mt-3'>Lub stwórz nowy egzamin</p>
        <?php
            echo "<a class='btn btn-sm btn-success btn-block' href='".Config::APP_ROOT."/exam/scan/add-exam.php'>Stwórz Egzamin</a>"
        ?>
    </div>
</div>
</body>
</html>
<?php
Database::disconnectDb($db);
?>
