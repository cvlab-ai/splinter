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
    <link rel="stylesheet" href="../../css/style.css">

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet"
          integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">

</head>

<body>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p"
        crossorigin="anonymous"></script>
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