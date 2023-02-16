<?php
session_start();

require_once("classes/Config.php");
Config::header()
?>
<body>
<?php
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
        header("Refresh:0; url=".Config::APP_ROOT."/index.php");
    } else {
        echo '<script>alert("Nieprawodłowe dane")</script>';
    }

    Database::disconnectDb($db);
}

if (isset($_SESSION['email'])) {
    echo "
<div class='container text-center w-25 mt-5'>
    <h2>Sprawdzarka Egzaminów</h2>
    <p class='fw-light text-muted'>Tutaj możesz wybrać i zeskanować egzamin lub przejrzeć istniejące już egzaminy.</p>

    <p class='fw-light text-muted mt-5'>1) Wybierz lub stwórz egzamin a następnie dodaj zeskanowane pliki aby sprawdzić egzamin.</p>
    <a class='btn btn-primary btn-lg timeTr' href='".Config::APP_ROOT."/exam/scan/select-exam.php'>Skanowanie Egzaminu</a>

    <p class='fw-light text-muted mt-3'>Lub</p>
    <p class='fw-light text-muted'>2) Przeglądaj wcześniej dodane egzamini wraz z ich zawartością.</p>
    <a class='btn btn-primary btn-lg timeTr' href='".Config::APP_ROOT."/exam/exam-list.php'>Przeglądaj Egzaminy</a>
</div>
";
} else {
    echo " 
    <div class='container text-center w-25 mt-5'>
  <form class='form-signin' method='post'>
    <img class='mb-4' src='https://getbootstrap.com/docs/4.0/assets/brand/bootstrap-solid.svg' alt='' width='72' height='72'>
    <h1 class='h3 mb-3 font-weight-normal'>Zaloguj się</h1>
    <label for='inputEmail' class='sr-only'>Adres e-mail PG:</label>
    <!--TODO Only PG mail ^-->
    
    <input type='email' id='inputEmail' class='form-control' placeholder='Email'required='required' autofocus='' name='email'>
    
    <label for='inputPassword' class='sr-only'>Hasło</label>
    <input type=password id='inputPassword' class='form-control' placeholder='Hasło' required='required' name='pwd'>
    <br>
    <input class='btn btn-lg btn-primary btn-block' type='submit' value='Zaloguj Się' name='submit'>
    <br>
    <a class='btn btn-secondary btn-sm mt-2' href='".Config::APP_ROOT."/register.php'>Zarejestruj się</a>
    <p class='mt-5 mb-3 text-muted'>© Politechnika Gdańska 2022</p>
  </form>
</div>";
}
?>
</body>
</html>
