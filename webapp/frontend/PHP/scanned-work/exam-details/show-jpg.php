<?php
session_start();
$host = "host = splinter_db";
$port = "port = 5432";
$dbname = "dbname = splinter";
$credentials = "user = postgres password=1234";
$db = pg_connect("$host $port $dbname $credentials");
if (!$db) {
    echo "Error : Unable to open database\n";
}

$fileId = $_GET['id'];
$isResult = $_GET['result'];

if ($isResult == "true") {
    $sql = "SELECT file_path from exam_result_files WHERE id = $fileId";
    $fileId .= "-result";
} else {
    $sql = "SELECT file_path from exam_files WHERE id = $fileId";
}


$ret = pg_query($db, $sql);
if (!$ret) {
    echo pg_last_error($db);
    exit;
}
$row = pg_fetch_row($ret);

// create a new cURL resource
$ch = curl_init();

// set URL and other appropriate options
curl_setopt($ch, CURLOPT_URL, 'http://splinter_exam_storage/'.$row[0]);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_HEADER, 0);

// grab URL and pass it to the browser
$out = curl_exec($ch);

// close cURL resource, and free up system resources
curl_close($ch);


$fp = fopen($fileId.'.jpg', 'w');
fwrite($fp, $out);
fclose($fp);

echo "<img src=/scanned-work/exam-details/$fileId.jpg>";
?>