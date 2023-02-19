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
        crossorigin="anonymous">
</script>
<?php
echo NavBar::showNavBar("scan");

$userID = $_SESSION['userID'];

if (isset($_POST["submit-btn"])) {
    $examID = $_POST['exam'];
} elseif (isset($_SESSION["exam"])) {
    $examID = $_SESSION["exam"];
    $_SESSION["exam"] = "";
} else {
    header("Location: select-exam.php");
}

?>

<div class="container text-center w-25 mt-5">
    <h4>Wybierz plik ze skanem poprawnych odpowiedzi lub skanem egzaminów</h4>
    <p class='fw-light text-muted'>Nie jest wymaganie przesłanie poprwanych odpowiedzi i egzaminów NA RAZ.</p>
    <div class="mb-3">
        <form method="post" action="<?=Config::APP_ROOT?>/exam/scan/scan.php" enctype="multipart/form-data">
            <?php
            echo "<input hidden name='exam' value='$examID'>"
            ?>
            <label for="result" class="form-label">Wybierz skan z wzorcowymi poprawnymi odpowiedziemi:</label>
            <p class='fw-light text-muted'>Możesz wybrać kilka plików jednocześnie.</p>
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
            <label for="files" class="form-label">Wybierz plik ze skanami egzaminów:</label>
            <p class='fw-light text-muted'>Możesz wybrać kilka plików jednocześnie.</p>
            <input class="form-control" accept="application/pdf" type="file" id="files" name="files[]" multiple><br><br>
            <?php
            $files = Curl::showWebDavFiles();
            if (count($files) > 0) {
                echo '<label for="webdav-files" class="form-label">Lub wybierz plik z webdav:</label>';
                echo '<p class="fw-light text-muted">Możesz wybrać kilka plików jednocześnie.</p>';
                echo '<select class="form-select" name="webdav-files[]" id="webdav-files" multiple>';

                foreach ($files as $file) {
                    echo '<option value="' . $file['name'] . '">' . $file['name'] . '</option>';
                }
                echo '</select><br><br>';
            }
            ?>
            <hr>
            <div id="progress" class="loader" style="display: none"></div>
            <p id="infoDownload" style="display: none" class='fw-light text-muted'>Trwa wysyłanie plików. Prosze czekać...</p>
            <input class="btn btn-sm btn-primary btn-block mt-3" id="wyslij" type="submit" value="Wyślij Pliki" name="submit-btn">
        </form>
        <label class="form-label mt-3">Pobierz wzorcowy arkusz:</label>
        <p id="infoDownloadTemplate" class='fw-light text-muted'>Wybierz jaki format pliku wzorca chcesz pobrać: PDF czy PNG.</p>
        <a href="<?=Config::APP_ROOT?>/files/template.pdf" download>
            <input class="btn btn-sm btn-primary btn-block" id="getExamplePDF" type="submit" value="Pobierz PDF" name="submit-btn">
        </a>
        
        <a href="<?=Config::APP_ROOT?>/files/template.png" download>
            <input class="btn btn-sm btn-primary btn-block" id="getExamplePNG" type="submit" value="Pobierz PNG" name="submit-btn">
        </a>
    </div>
</div>
<script> 
document.getElementById("wyslij").onclick = function () {
    document.getElementById("wyslij").style.display = "none";
    document.getElementById("infoDownload").style.display = "";
};
</script>
</body>
</html>
