<?php
session_start();

use database\Database;
use navbar\NavBar;
use curl\Curl;

require("../../classes/NavBar.php");
NavBar::userIsLogged(2);
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

    <link rel="stylesheet" href="../../css/bootstrap.min.css">
    <link rel="stylesheet" href="../../css/style.css">
    <script src="../../css/js/bootstrap.bundle.min.js"></script>
</head>

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
        <label for="select" class="form-label"><h2>Egzamin</h2></label>
        <form method="post" action="/exam/scan/select-file.php">
            <select id="select" class="form-select" name="exam">
                <?php
                while ($row = pg_fetch_row($data)) {
                    $examID = $row[0];
                    $examName = $row[1];
                    echo "<option value='$examID'>$examName</option>";
                }
                ?>
            </select>
            <input type="submit" class="btn btn-sm btn-primary btn-block mt-3" value="Dalej" name="submit-btn">
            <?php
            echo "<a class='btn btn-sm btn-success btn-block mt-3' href='/exam/scan/add-exam.php'>Dodaj Egzamin</a>"
            ?>
        </form>
    </div>
</div>
</body>
</html>
<?php
Database::disconnectDb($db);
?>