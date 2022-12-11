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
use database\Database;

require("classes/Database.php");
require("classes/NavBar.php");

echo NavBar::showNavBar("main");

$emailErr = false;

$db = Database::connectToDb();

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

    if ((!filter_var($email, FILTER_VALIDATE_EMAIL) || !preg_match("/^.+@(pg.edu.pl|eti.pg.edu.pl)$/",$email)) || pg_num_rows($ret) != 0)  {
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
        $sql = "insert into public.user(email,password, register_key, registered)values('".$_POST['email']."','".md5($_POST['pwd'])."','".implode($pass)."',false)";

        $ret = pg_query($db, $sql);
        if($ret){
            $emailServer = getenv('EMAIL_SERVER_ADDR');
            $to      = $_POST['email'];
            $subject = 'Rejstracja - PG';
            $message = 'Aby potwierdzić konto użytkownika wejdź w podany adres: '."<a href='http://www.sprawdzarka.pg.edu.pl/process-register.php?email=".$email."&registerKey=".implode($pass)."'>Potwierdź rejstracje!</a>";
            $headers = 'From: '.$emailServer."\r\n".
                'Reply-To: '.$emailServer."\r\n".
                'X-Mailer: PHP/'.phpversion();
            var_dump($message);
            mail($to, $subject, $message, $headers);
            header("Refresh:0; url=register.php?registered=true");
        }else{
            echo "Something Went Wrong";
        }
    }
}
?>
<div class="container">
    <?php
    if ($registered){
        echo '<div class="alert alert-success" role="alert"> Zarejstrowano! Sprawdź e-mail!</div>';
    }
    ?>
    <h2>Rejstracja</h2>
    <form method="post">

        <div class="form-group">
            <?php
                if ($emailErr){
                    echo '<div class="alert alert-danger" role="alert"> Nieprawidłowy adres email</div>';
                }
            ?>
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
