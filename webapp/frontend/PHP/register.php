<?php
$host = "host = localhost";
$port = "port = 5432";
$dbname = "dbname = splinter";
$credentials = "user = postgres password=1234";
$db = pg_connect("$host $port $dbname $credentials");
if(isset($_POST['submit'])&&!empty($_POST['submit'])){

    $sql = "insert into public.user(name,email,password)values('".$_POST['name']."','".$_POST['email']."','".md5($_POST['pwd'])."')";
    $ret = pg_query($db, $sql);
    if($ret){

        echo "Data saved Successfully";
    }else{

        echo "Soething Went Wrong";
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <title>PHP PostgreSQL Registration & Login Example </title>
    <meta name="keywords" content="PHP,PostgreSQL,Insert,Login">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
</head>
<body>
<div class="container">
    <h2>Register Here </h2>
    <form method="post">

        <div class="form-group">
            <label for="name">Name:</label>
            <input type="text" class="form-control" id="name" placeholder="Enter name" name="name" requuired>
        </div>

        <div class="form-group">
            <label for="email">Email:</label>
            <input type="email" class="form-control" id="email" placeholder="Enter email" name="email">
        </div>

        <div class="form-group">
            <label for="pwd">Password:</label>
            <input type="password" class="form-control" id="pwd" placeholder="Enter password" name="pwd">
        </div>

        <input type="submit" name="submit" class="btn btn-primary" value="Submit">
    </form>
</div>
</body>
</html>