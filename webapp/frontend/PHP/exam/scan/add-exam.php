<?php
session_start();

use database\Database;
use navbar\NavBar;

require("../../classes/NavBar.php");
NavBar::userIsLogged(2);
require("../../classes/Database.php");
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
echo NavBar::showNavBar("main");

$db = Database::connectToDb();

if (isset($_POST['submit-subject']) && !empty($_POST['submit-subject'])) {
    $name = $_POST['subject-name'];
    $desc = $_POST['subject-desc'];
    $date = $_POST['subject-date'];
    $userID = $_SESSION['userID'];

    $queryFields = "(name, user_id";
    $queryValues = "('$name',$userID";

    if (isset($_POST['subject-desc']) && $desc !== "") {
        $queryFields .= ",description";
        $queryValues .= ",'$desc'";
    }

    if (isset($_POST['subject-date']) && $date !== "") {
        $queryFields .= ",date";
        $queryValues .= ",'$date'";
    }
    $queryFields .= ")";
    $queryValues .= ")";

    $query = "INSERT INTO exam $queryFields VALUES $queryValues";

    $res = pg_query($db, $query);
    if (!$res) {
        echo pg_last_error($db);
        exit;
    }

    header("Refresh:0; url=/exam/scan/select-exam.php");
}


Database::disconnectDb($db);
?>

<div class="container text-center w-25 mt-5">
    <div class="mb-3">
        <label for="select" class="form-label">Dodaj Egzamin</label>
        <hr>
        <form method="post">
            <label for="subject-name" class="form-label required">Nazwa Egzaminu</label>
            <input type="text" name="subject-name" id="subject-name" placeholder="Nazwa Egzaminu"
                   class="form-control" required='required'>
            <hr>
            <label for="subject-desc" class="form-label">Opis Egzaminu</label>
            <textarea name="subject-desc" id="subject-desc" placeholder="Opis Egzaminu"
                      class="form-control"></textarea>
            <hr>
            <label for="subject-date" class="form-label">Data Egzaminu</h2></label>
            <input class="form-control" type="date" id="subject-date" name="subject-date">
            <hr>
            <input type="submit" class="btn btn-sm btn-primary btn-block mt-3" value="Dodaj Egzamin"
                   name="submit-subject">
        </form>
    </div>
</div>
</body>
</html>
