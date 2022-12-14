<?php
session_start();

use navbar\NavBar;

require("../../classes/NavBar.php");
NavBar::userIsLogged(2);
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
$examID = $_GET['examID'];
?>

<div class="container text-center w-25 mt-5">
    <div class="mb-3">
        <form method="post" action="/exam/edit/scan-edited-answers.php" enctype="multipart/form-data">
            <?php
            echo "<input hidden name='examID' value='$examID'>"
            ?>
            <label for="files" class="form-label">Wybierz plik ze skanem pracy:</label>
            <input class="form-control" accept="application/pdf" type="file" id="files" name="files" ><br><br>
            <hr>

            <input class="btn btn-sm btn-primary btn-block mt-3" type="submit" value="Zamień Prace" name="submit-btn">
        </form>
    </div>
</div>
</body>
</html>
