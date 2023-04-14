<?php
session_start();

require("../classes/NavBar.php");
require("../classes/Database.php");
require_once("../classes/Config.php");
NavBar::userIsLogged(1);
Config::header();
?>
<body>
<?php
echo NavBar::showNavBar("exam");
?>

<div class="container text-center w-25 mt-5">
    <h2>Lista egzaminów</h2>
    <p class='fw-light text-muted'>Wybierz egzamin, który chcesz obejrzeć.</p>
    <hr>
    <!--TODO mała rozdzielczość-->
    <ul class="list-group">
        <?php

        $db = Database::connectToDb();

        $userID = $_SESSION['userID'];

        $sql = "SELECT id, name, date FROM exam WHERE user_id = $userID";
        $data = pg_query($db, $sql);

        while ($row = pg_fetch_row($data)) {
            $examID = $row[0];
            $examName = $row[1];
            $examDate = $row[2];
            echo "<a style='text-decoration: none;' href='".Config::APP_ROOT."/exam/exam-detail.php?examID=$examID' class='mt-2 mb-2'>
                 <li class='list-group-item d-flex rounded justify-content-between align-items-center list-group-item-action'>" . $examName .
                "<span class='badge bg-secondary rounded-pill'>Data Egzaminu: $examDate</span></li></a>";
        }

        Database::disconnectDb($db);
        ?>
    </ul>
</div>


</body>
</html>
