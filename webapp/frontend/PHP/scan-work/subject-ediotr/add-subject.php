<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Frontend</title>
    <base href="/">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" type="image/x-icon" href="favicon.ico">

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet"
          integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">

</head>

<body>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p"
        crossorigin="anonymous"></script>
<?php
session_start();

use navbar\NavBar;

require("../../classes/NavBar.php");
echo NavBar::showNavBar("scan");
$host = "host = localhost";
$port = "port = 5432";
$dbname = "dbname = splinter";
$credentials = "user = postgres password=1234";

$db = pg_connect("$host $port $dbname $credentials");
if (!$db) {
    echo "Error : Unable to open database\n";
}

if (isset($_POST['submit-subject']) && !empty($_POST['submit-subject'])) {
    $email = $_SESSION['email'];
    $name = $_POST['subject-name'];
    $desc = $_POST['subject-desc'];
    $query = "SELECT id FROM public.user WHERE public.user.email = '$email'";
    $ret = pg_query($db, $query);
    if (!$ret) {
        echo pg_last_error($db);
        exit;
    }
    $userId = 0;
    while ($row = pg_fetch_row($ret)) {
        $userId = $row[0];
    }
    $query = "INSERT INTO subject (name, description, user_id) VALUES ('$name','$desc',$userId)";
    $res = pg_query($db, $query);
    if (!$res) {
        echo pg_last_error($db);
        exit;
    }
    // TODO redirect
    echo "DODANO";
}


pg_close($db);
?>

<div class="container text-center w-25 mt-5">
    <div class="mb-3">
        <label for="select" class="form-label"><h2>Dodaj Przedmiot</h2></label>
        <hr>
        <form method="post">
            <label for="subject-name" class="form-label"><h2>Nazwa Przedmiotu</h2></label>
            <input type="text" name="subject-name" id="subject-name" placeholder="Nazwa Przedmiotu"
                   class="form-control">
            <hr>
            <label for="subject-desc" class="form-label"><h2>Opis Przedmiotu</h2></label>
            <textarea name="subject-desc" id="subject-desc" placeholder="Opis Przedmiotu"
                      class="form-control"></textarea>
            <input type="submit" class="btn btn-sm btn-primary btn-block mt-3" value="Dodaj Przedmiot"
                   name="submit-subject">
        </form>
    </div>
</div>
</body>
</html>