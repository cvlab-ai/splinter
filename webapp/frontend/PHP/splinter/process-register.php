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
require("classes/NavBar.php");
require("classes/Database.php");
echo NavBar::showNavBar("main");

if (isset($_GET['email']) && !empty($_GET['email'])) {
    $db = Database::connectToDb();

    $user_register_key = $_GET['registerKey'];
    $email = $_GET['email'];

    $sql = "select id, register_key from public.user where email = '$email' AND register_key = '$user_register_key'";
    $data = pg_query($db, $sql);
    $login_check = pg_num_rows($data);
    $row = pg_fetch_row($data);

    $registerConfirmed = false;
    if ($row[1] == $user_register_key) {
        $sql = "UPDATE public.user SET registered = true where email = '$email'";
        $ret = pg_query($db, $sql);
        if($ret){
            echo "Data saved Successfully";
            $registerConfirmed = true;
        }else{
            echo "Something Went Wrong";
        }
    }
    if ($login_check > 0) {
        $_SESSION['email'] = $_POST['email'];
        $_SESSION['userID'] = $row[0];

        $_POST['isLog'] = true;
        $_POST['registerConfirmed'] = $registerConfirmed;

        header("Refresh:0; url=".Config::APP_ROOT."/index.php");
    } else {
        echo '<script>alert("Nieprawodłowe dane")</script>';
    }

    Database::disconnectDb($db);
}
?>


</body>
</html>
