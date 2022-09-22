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
    $files = $_POST['files'];
    for ($i = 0; $i < count($_FILES['files']['name']); $i++) {
        $file_name = $_FILES['files']['name'][$i];
        $file_size =$_FILES['files']['size'][$i];
        $file_tmp =$_FILES['files']['tmp_name'][$i];
        $file_type=$_FILES['files']['type'][$i];
        $array = explode('.', $_FILES['files']['name'][$i]);
        $file_ext=strtolower(end($array));

        move_uploaded_file($file_tmp,$file_name);
        $email = $_SESSION['email'];
        $filePath = "scanned-files/$email/$file_name";
        $fileDirectory = "scanned-files/$email/";
        if (!file_exists($fileDirectory)) {
            mkdir($fileDirectory, 0777, true);
        }
        rename($file_name, $filePath);

        $query = "INSERT INTO exam_files (file_name, file_path, exam_id) VALUES ('$file_name','$filePath', $exam_id)";
        $res = pg_query($db, $query);
        if (!$res) {
            echo pg_last_error($db);
            exit;
        }
    }

}
pg_close($db);

?>


</body>
</html>
