<?php
session_start();
?>
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Frontend</title>
    <base href="/">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" type="image/x-icon" href="favicon.ico">
    <link rel="stylesheet" href="../css/style.css">

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet"
          integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
</head>

<body>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p"
        crossorigin="anonymous"></script>
<?php
use navbar\NavBar;
require ("../classes/NavBar.php");
echo NavBar::showNavBar("");
?>


<div class="container text-center w-25 mt-5">
    <h2>Lista egzaminów</h2>
    <hr>
    <!--TODO mała rozdzielczość-->
    <ul class="list-group">
        <?php
        $host = "host = splinter_db";
        $port = "port = 5432";
        $dbname = "dbname = splinter";
        $credentials = "user = postgres password=1234";

        $db = pg_connect("$host $port $dbname $credentials");
        if (!$db) {
            echo "Error : Unable to open database\n";
        }

        $email = $_SESSION['email'];
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
        $sql = "SELECT * from EXAM WHERE user_id = $userId OR position('$email' in owners) > 0";

        $ret = pg_query($db, $sql);
        if (!$ret) {
            echo pg_last_error($db);
            exit;
        }
        // TODO Data zapisania
        // TODO odnośnik href
        while ($row = pg_fetch_row($ret)) {
            echo "<a style='text-decoration: none;' href='/scanned-work/exam-details/exam-details.php?id=$row[0]' class='mt-2 mb-2'>
                 <li class='list-group-item d-flex rounded justify-content-between align-items-center list-group-item-action'>" . $row[1] .
                "<span class='badge bg-secondary rounded-pill'>Data Egzaminu: $row[6]</span></li></a>";
        }

        pg_close($db);
        ?>
    </ul>
</div>


</body>
</html>
