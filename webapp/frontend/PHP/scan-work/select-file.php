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
require ("../classes/NavBar.php");
echo NavBar::showNavBar("scan");

$host = "host = localhost";
$port = "port = 5432";
$dbname = "dbname = splinter";
$credentials = "user = postgres password=1234";

$db = pg_connect("$host $port $dbname $credentials");
if (!$db) {
    echo "Error : Unable to open database\n";
}
if (isset($_POST["submit-btn"])) {
    $subject_id = $_POST['subject'];
    $exam_id = $_POST['exam'];
} else {
    $subject_id = 0;
    $exam_id = 0;
}
/*TODO pobierz usera*/
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
$sql =" SELECT * from exam WHERE user_id = $userId AND subject_id = $subject_id";

$ret = pg_query($db, $sql);
if (!$ret) {
    echo pg_last_error($db);
    exit;
}
pg_close($db);
?>

<div class="container text-center w-25 mt-5">
    <div class="mb-3">
        <form method="post" action="/scan-work/scan.php" enctype="multipart/form-data">
            <?php echo "<input hidden name='subject' value='$subject_id'> <input hidden name='exam' value='$exam_id'>"?>
            <label for="files" class="form-label">Wybierz plik ze skanami prac:</label>
            <input class="form-control" accept="application/pdf" type="file" id="files" name="files[]" multiple><br><br>
            <input class="btn btn-sm btn-primary btn-block mt-3" type="submit" value="Sprawdź Prace" name="submit-btn">
        </form>
    </div>
</div>


</div>
</body>
</html>