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

require("classes/NavBar.php");
echo NavBar::showNavBar("main");

if (isset($_POST['submit']) && !empty($_POST['submit'])) {
    $host = "host = splinter_db";
    $port = "port = 5432";
    $dbname = "dbname = splinter";
    $credentials = "user = postgres password=1234";

    $db = pg_connect("$host $port $dbname $credentials");
    if (!$db) {
        echo "Error : Unable to open database\n";
    }

    $hashpassword = md5($_POST['pwd']);
    $sql = "select * from public.user where email = '" . pg_escape_string($_POST['email']) . "' and password ='" . $hashpassword . "'";
    $data = pg_query($db, $sql);
    $login_check = pg_num_rows($data);
    if ($login_check > 0) {
        $_SESSION['email'] = $_POST['email'];
        $_POST['isLog'] = true;
        header("Refresh:0; url=index.php");
    } else {
        echo '<script>alert("Nieprawodłowe dane")</script>';
    }
    pg_close($db);
}

?>


</body>
</html>
