<?php
$emailErr = false;

$host = "host = splinter_db";
$port = "port = 5432";
$dbname = "dbname = splinter";
$credentials = "user = postgres password=1234";
$db = pg_connect("$host $port $dbname $credentials");

if(isset($_GET['registered'])){
    $registered = true;
} else {
    $registered = false;
}

if(isset($_POST['submit'])&&!empty($_POST['submit'])){
    $email = $_POST["email"];
    $saveUser = true;

    $sql = "SELECT id FROM public.user where email = '$email'";
    $ret = pg_query($db, $sql);

    if ((!filter_var($email, FILTER_VALIDATE_EMAIL) && !preg_match("/^.+@(pg.edu.pl|eti.pg.edu.pl)$/",$email)) || pg_num_rows($ret) != 0)  {
        $emailErr = true;
        $saveUser = false;
    }

    $alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890';
    $pass = array();
    $alphaLength = strlen($alphabet) - 1;
    for ($i = 0; $i < 8; $i++) {
        $n = rand(0, $alphaLength);
        $pass[] = $alphabet[$n];
    }

    if ($saveUser) {
        $sql = "insert into public.user(name,email,password, register_key, registered)values('".$_POST['name']."','".$_POST['email']."','".md5($_POST['pwd'])."','".implode($pass)."',false)";

        $ret = pg_query($db, $sql);
        if($ret){
            header("Refresh:0; url=register.php?registered=true");
        }else{
            echo "Something Went Wrong";
        }
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
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
<div class="container">
    <?php
    var_dump($registered);
    if ($registered){
        echo '<div class="alert alert-success" role="alert"> Zarejstrowano! Sprawdź e-mail!</div>';
    }
    ?>
    <h2>Register Here</h2>
    <form method="post">

        <div class="form-group">
            <?php
                if ($emailErr){
                    echo '<div class="alert alert-danger" role="alert"> Nieprawidłowy adres email</div>';
                }
            ?>
            <label for="name">Name:</label>
            <input type="text" class="form-control" id="name" placeholder="Enter name" name="name" required>
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
