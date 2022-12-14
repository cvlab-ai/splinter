<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Frontend</title>
    <base href="/">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" type="image/x-icon" href="favicon.ico">

    <link rel="stylesheet" href="css/bootstrap.min.css">
    <link rel="stylesheet" href="css/style.css">
    <script src="css/js/bootstrap.bundle.min.js"></script>
</head>

<body>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p"
        crossorigin="anonymous"></script>

<?php
session_start();

use database\Database;
use navbar\NavBar;

require("classes/NavBar.php");
require("classes/Database.php");

echo NavBar::showNavBar("main");

if (isset($_POST['submit']) && !empty($_POST['submit'])) {
    $db = Database::connectToDb();

    $hashpassword = md5($_POST['pwd']);
    $email = $_POST['email'];
    $sql = "select id, registered from public.user where email = '$email' and password = '$hashpassword' and registered = 'true'";
    $data = pg_query($db, $sql);
    $login_check = pg_num_rows($data);
    $row = pg_fetch_row($data);
    if ($login_check > 0 && $row[1]) {
        $_SESSION['email'] = $_POST['email'];
        $_SESSION['userID'] = $row[0];
        $_POST['isLog'] = true;
        header("Refresh:0; url=index.php");
    } else {
        echo '<script>alert("Nieprawodłowe dane")</script>';
    }

    Database::disconnectDb($db);
}
?>


</body>
</html>
