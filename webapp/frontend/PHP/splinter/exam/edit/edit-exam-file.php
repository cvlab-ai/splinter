<?php
session_start();

require("../../classes/NavBar.php");
require_once("../../classes/Config.php");
NavBar::userIsLogged(2);
Config::header();
?>
<body>
<?php
echo NavBar::showNavBar("scan");
$name = $_GET['name'];

$examID = $_GET['examID'];
?>

<div class="container text-center w-25 mt-5">
    <div class="mb-3">
        <form method="post" action="<?=Config::APP_ROOT?>/exam/edit/scan-edited-file.php" enctype="multipart/form-data">
            <?php
            echo "<input hidden name='name' value='$name'>";
            echo "<input hidden name='examID' value='$examID'>";
            ?>
            <label for="files" class="form-label">Wybierz plik ze skanem pracy:</label>
            <input class="form-control" accept="application/pdf" type="file" id="files" name="files" ><br><br>
            <hr>

            <input class="btn btn-sm btn-primary btn-block mt-3" type="submit" value="Zamień Prace" name="submit-btn">
        </form>
    </div>
</div>
</body>
</html>
