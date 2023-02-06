<?php
session_start();

require("../../classes/NavBar.php");
require("../../classes/Curl.php");
require_once("../../classes/Config.php");
NavBar::userIsLogged(2);
Config::header();
?>
<body>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p"
        crossorigin="anonymous"></script>
<?php
echo NavBar::showNavBar("scan");

$userID = $_SESSION['userID'];

if (isset($_POST["submit-btn"])) {
    $examID = $_POST['exam'];
} else {
    header("Location: select-exam.php");
}

?>

<div class="container text-center w-25 mt-5">
    <div class="mb-3">
        <form method="post" action="<?=Config::APP_ROOT?>/exam/scan/scan.php" enctype="multipart/form-data">
            <?php
            echo "<input hidden name='exam' value='$examID'>"
            ?>
            <label for="files" class="form-label">Wybierz plik ze skanami prac:</label>
            <input class="form-control" accept="application/pdf" type="file" id="files" name="files[]" multiple><br><br>
            <?php
            $files = Curl::showWebDavFiles();
            if (count($files) > 0) {
                echo '<label for="webdav-files" class="form-label">Lub wybierz plik z webdav:</label>';
                echo '<select class="form-select" name="webdav-files[]" id="webdav-files" multiple>';

                foreach ($files as $file) {
                    echo '<option value="' . $file['name'] . '">' . $file['name'] . '</option>';
                }
                echo '</select><br><br>';
            }
            ?>

            <hr>
            <label for="result" class="form-label">Wybierz plik z odpowiedziami:</label>
            <input class="form-control" accept="application/pdf" type="file" id="result" name="result[]"
                   multiple><br><br>
            <?php
            $files = Curl::showWebDavFiles();
            if (count($files) > 0) {
                echo '<label for="webdav-results" class="form-label">Lub wybierz plik z webdav:</label>';
                echo '<select class="form-select" name="webdav-results[]" id="webdav-results" multiple>';
                foreach ($files as $file) {
                    echo '<option value="' . $file['name'] . '">' . $file['name'] . '</option>';
                }
                echo '</select><br><br>';
            }
            ?>


            <hr>

            <input class="btn btn-sm btn-primary btn-block mt-3" type="submit" value="Sprawdź Prace" name="submit-btn">
        </form>
    </div>
</div>
</body>
</html>
