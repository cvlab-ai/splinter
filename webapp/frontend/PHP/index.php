<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Frontend</title>
    <base href="/">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" type="image/x-icon" href="favicon.ico">

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
</head>

<body>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>

<?php
session_start();
use navbar\NavBar;
require ("classes/NavBar.php");
echo NavBar::showNavBar("main");

if (isset($_SESSION['email'])) {
    echo "Witaj ".$_SESSION['email'];
} else {
    echo" 
    <div class='container text-center w-25 mt-5'>
  <form class='form-signin' method='post' action='login.php'>
    <img class='mb-4' src='https://getbootstrap.com/docs/4.0/assets/brand/bootstrap-solid.svg' alt='' width='72' height='72'>
    <h1 class='h3 mb-3 font-weight-normal'>Zaloguj się</h1>
    <label for='inputEmail' class='sr-only'>Adres e-mail PG:</label>
    <!--TODO Only PG mail ^-->
    
    <input type='email' id='inputEmail' class='form-control' placeholder='Email' required='' autofocus='' name='email'>
    
    <label for='inputPassword' class='sr-only'>Hasło</label>
    <input type=password id='inputPassword' class='form-control' placeholder='Hasło' required='' name='pwd'>
    <div class='checkbox mb-3'>
      <label>
        <input type='checkbox' value='remember-me'> Zapamiętaj mnie
    </label>
    </div>
    <input class='btn btn-lg btn-primary btn-block' type='submit' value='Zaloguj Się' name='submit'>
    <br>
    <a routerLink='/register'>Zarejestruj się</a>
    <p class='mt-5 mb-3 text-muted'>© Politechnika Gdańska 2022</p>
  </form>
</div>";
}

?>


</body>
</html>
