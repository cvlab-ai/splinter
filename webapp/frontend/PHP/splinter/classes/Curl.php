<?php

require_once("Config.php");

class Curl
{
    public static function generateStudentAnswers($examID) {
        $exam_storage_user = getenv('EX_STORE_SPLINTER_USER');
        $exam_storage_password = getenv('EX_STORE_SPLINTER_PASS');

        $ch = curl_init();

        curl_setopt($ch, CURLOPT_URL, Config::INFERENCE_URL."check-exam");
        curl_setopt($ch, CURLOPT_USERPWD, $exam_storage_user . ":" . $exam_storage_password);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, '{ "examId": "' . $examID .'", "force":true }');
        curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
        curl_exec($ch);
        curl_close($ch);
        $http_status = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        if ($http_status > 299 || $http_status < 200) {
            return false;
        }
        return true;
    }

    public static function generateExamAnswersKeys($examID, $force) {

        $exam_storage_user =  getenv('EX_STORE_SPLINTER_USER');
        $exam_storage_password = getenv('EX_STORE_SPLINTER_PASS');
        
        $ch = curl_init();

        curl_setopt($ch, CURLOPT_URL, Config::INFERENCE_URL."generate-exam-keys");
        curl_setopt($ch, CURLOPT_USERPWD, $exam_storage_user . ":" . $exam_storage_password);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, '{ "examId": "' .  $examID . '", "force":'.$force.' }');
        curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
        curl_exec($ch);
        curl_close($ch);
        
        $http_status = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        if ($http_status > 299 || $http_status < 200) {
            return false;
        }
        return true;
    }

    public static function getWebdavFileAndUploadSplinter($fileName, $filePath) {
        $exam_webdav_user =  getenv('EX_STORE_WEBDAV_USER');
        $exam_webdav_password = getenv('EX_STORE_WEBDAV_PASS');

        // download file from webdav
        $ch = curl_init();

        $userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36';

        curl_setopt($ch, CURLOPT_HEADER, 0);
        curl_setopt($ch, CURLOPT_VERBOSE, 0);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_USERPWD, $exam_webdav_user . ":" . $exam_webdav_password);
        curl_setopt($ch, CURLOPT_URL, Config::UPLOADS_URL.$fileName);
        curl_setopt($ch, CURLOPT_USERAGENT, $userAgent);

        $output = curl_exec($ch);

        curl_close($ch);

        $http_status = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        if ($http_status > 299 || $http_status < 200) {
            return false;
        }

        $fp = fopen($fileName, 'w');
        fwrite($fp, $output);
        fclose($fp);

        self::sendFileToSplinter($fileName,$filePath);
        self::deleteWebDavFile($fileName);
        return true;
    }

    public static function sendFileToSplinter($fileName, $filePath) {
        $exam_storage_user = getenv('EX_STORE_SPLINTER_USER');
        $exam_storage_password = getenv('EX_STORE_SPLINTER_PASS');

        // send file to storage
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, Config::EXAM_STORAGE_URL . $filePath);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_PUT, true);
        curl_setopt($ch, CURLOPT_INFILESIZE, filesize($fileName));
        curl_setopt($ch, CURLOPT_BINARYTRANSFER, TRUE);
        curl_setopt($ch, CURLOPT_USERPWD, $exam_storage_user . ":" . $exam_storage_password);
        $fp = fopen($fileName, "r");
        curl_setopt($ch, CURLOPT_INFILE, $fp);
        curl_exec($ch);
        curl_close($ch);
        $http_status = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        if ($http_status > 299 || $http_status < 200) {
            return false;
        }
        fclose($fp);
        unlink($fileName);
        return true;
    }

    public static function showWebDavFiles() {
        $exam_storage_user = getenv('EX_STORE_WEBDAV_USER');
        $exam_storage_password = getenv('EX_STORE_WEBDAV_PASS');

        exec("curl -Ls -u ".$exam_storage_user.":".$exam_storage_password." ".Config::UPLOADS_URL, $output, $res);
        $resultStr = implode(" ",$output);

        return json_decode($resultStr, true);
    }

    public static function searchExamPathForStudents($examID) {
        $exam_storage_user = getenv('EX_STORE_SPLINTER_USER');
        $exam_storage_password = getenv('EX_STORE_SPLINTER_PASS');
        $output = [];
        exec("curl -Ls -u ".$exam_storage_user.":".$exam_storage_password." ".Config::EXAM_STORAGE_URL.$examID."/students",
            $output);

        return json_decode(implode(" ",$output), true);
    }

    public static function getExamResult($examID, $index) {
        $exam_storage_user = getenv('EX_STORE_SPLINTER_USER');
        $exam_storage_password = getenv('EX_STORE_SPLINTER_PASS');

        $output = [];
        exec("curl -Ls -u ".$exam_storage_user.":".$exam_storage_password." ".Config::EXAM_STORAGE_URL.$examID."/students/".$index."/answers.json",
            $output);

        return json_decode(implode(" ",$output), true);
    }

    public static function getExams($examID) {
        $exam_storage_user = getenv('EX_STORE_SPLINTER_USER');
        $exam_storage_password = getenv('EX_STORE_SPLINTER_PASS');

        $output = [];
        exec("curl -Ls -u ".$exam_storage_user.":".$exam_storage_password." ".Config::EXAM_STORAGE_URL.$examID."/answers_keys/ | grep -i .json",
            $output);
        $resultStr = implode(" ",$output);
        if (substr($resultStr, -1) == ",") {
            $resultStr = substr($resultStr, 0 ,-1);
        }

        return json_decode("[".$resultStr."]", true);
    }

    public static function deleteStudent($examID, $studentIndex) {
        $exam_storage_user = getenv('EX_STORE_SPLINTER_USER');
        $exam_storage_password = getenv('EX_STORE_SPLINTER_PASS');
        exec("curl -X DELETE -u ".$exam_storage_user.":".$exam_storage_password." ".Config::EXAM_STORAGE_URL.$examID."/students/".$studentIndex."/");
        header("Refresh:0; url=".Config::APP_ROOT."/exam/exam-detail.php?examID=".$examID);
    }

    public static function deleteExam($examID) {
        $exam_storage_user = getenv('EX_STORE_SPLINTER_USER');
        $exam_storage_password = getenv('EX_STORE_SPLINTER_PASS');
        exec("curl -X DELETE -u ".$exam_storage_user.":".$exam_storage_password." ".Config::EXAM_STORAGE_URL.$examID."/");
        header("Refresh:0; url=".Config::APP_ROOT."/exam/exam-list.php");
    }

    public static function deleteWebDavFile($fileName) {
        $exam_webdav_user =  getenv('EX_STORE_WEBDAV_USER');
        $exam_webdav_password = getenv('EX_STORE_WEBDAV_PASS');
        exec("curl -X DELETE -u ".$exam_webdav_user.":".$exam_webdav_password." ".Config::UPLOADS_URL.$fileName);
        header("Refresh:0; url=".Config::APP_ROOT."/exam/exam-list.php");
    }

    public static function deleteExamFile($examID, $name) {
        $exam_storage_user = getenv('EX_STORE_SPLINTER_USER');
        $exam_storage_password = getenv('EX_STORE_SPLINTER_PASS');
        exec("curl -X DELETE -u ".$exam_storage_user.":".$exam_storage_password." ".Config::EXAM_STORAGE_URL.$examID."/answers_keys/".$name);
        header("Refresh:0; url=".Config::APP_ROOT."/exam/exam-detail.php?examID=".$examID);
    }

    public static function getNumOfAnswers($examID, $studentIndex) {
        $exam_storage_user = getenv('EX_STORE_SPLINTER_USER');
        $exam_storage_password = getenv('EX_STORE_SPLINTER_PASS');

        $output = [];
        exec("curl -Ls -u ".$exam_storage_user.":".$exam_storage_password." ".Config::EXAM_STORAGE_URL.$examID."/students/".$studentIndex,
            $output);

        return count(json_decode(implode(" ",$output), true));
    }
}
