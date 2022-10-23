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

if (isset($_POST["submit-btn"])) {
    $examID = $_POST['exam'];
} else {
    // TODO redirect
}

?>

<div class="container text-center w-25 mt-5">
    <div class="mb-3">
        <form method="post" action="/exam/scan/scan.php" enctype="multipart/form-data">
            <?php
            echo "<input hidden name='exam' value='$examID'>"
            ?>
            <label for="files" class="form-label">Wybierz plik ze skanami prac:</label>
            <input class="form-control" accept="application/pdf" type="file" id="files" name="files[]" multiple><br><br>
            <hr>
            <label for="result" class="form-label">Wybierz plik z odpowiedziami:</label>
            <input class="form-control" accept="application/pdf" type="file" id="result" name="result[]" multiple><br><br>
            <input class="btn btn-sm btn-primary btn-block mt-3" type="submit" value="Sprawdź Prace" name="submit-btn">
        </form>
    </div>
</div>
</body>
</html>
<?php
Database::disconnectDb($db);
?>