<?php
session_start();

require_once("classes/Config.php");
Config::header()
?>
<body>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p"
        crossorigin="anonymous"></script>

<?php

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
            $senderHostname = getenv('EMAIL_SENDER_HOSTNAME');
            $appExternalURL = getenv('APP_EXTERNAL_URL');
            $to      = $_POST['email'];
            $subject = 'Rejstracja - PG';
            $message = 'Aby potwierdzić konto użytkownika wejdź w podany adres: '."<a href='".$appExternalURL."/process-register.php?email=".$email."&registerKey=".implode($pass)."'>Potwierdź rejstracje!</a>";

            $headers = "From: ".$senderHostname."\r\n";
            $headers .= "MIME-Version: 1.0\r\n";
            $headers .= "Content-type: text/html\r\n";
            $headers .= "X-Mailer: PHP/" . phpversion();

            
            file_put_contents('php://stdout', "Sending registration email:\nTo: ".$to."\nSubject: ".$subject."\nMessage: ".$message."\nHeaders: ".$headers);
            mail($to, $subject, $message, $headers);

            header("Refresh:0; url=".Config::APP_ROOT."/register.php?registered=true");
        }else{
            echo "Something Went Wrong";
        }
    }
}
?>
<div class="container text-center w-25 mt-5">
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
            <label for="email" class="form-label required">Email:</label>
            <input type="email" class="form-control" id="email" placeholder="Podaj email" name="email" required="required">
        </div>

        <div class="form-group">
            <label for="pwd" class="form-label required">Hasło:</label>
            <input type="password" class="form-control" id="pwd" placeholder="Podaj hasło" name="pwd" required="required">
        </div>
        <br>
        <input type="submit" name="submit" class="btn btn-primary" value="Zarejestruj się!">
    </form>
</div>
</body>
</html>
