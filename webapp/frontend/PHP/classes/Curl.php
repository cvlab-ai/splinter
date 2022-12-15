<?php

namespace curl;

class Curl
{
    public static function generateStudentAnswers($examID) {
        $exam_storage_user = getenv('EX_STORE_SPLINTER_USER');
        $exam_storage_password = getenv('EX_STORE_SPLINTER_PASS');

        $ch = curl_init();

        curl_setopt($ch, CURLOPT_URL, "http://splinter_inference_engine:8000/check-exam");
        curl_setopt($ch, CURLOPT_USERPWD, $exam_storage_user . ":" . $exam_storage_password);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, '{ "examId": "' . $examID .'", "force":true }');
        curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
        curl_exec($ch);
        curl_close($ch);
    }

    public static function generateExamAnswersKeys($examID) {

        $exam_storage_user =  getenv('EX_STORE_SPLINTER_USER');
        $exam_storage_password = getenv('EX_STORE_SPLINTER_PASS');
        var_dump("generating".$examID." ".$exam_storage_user." ".$exam_storage_password);
        $ch = curl_init();

        curl_setopt($ch, CURLOPT_URL, "http://splinter_inference_engine:8000/generate-exam-keys");
        curl_setopt($ch, CURLOPT_USERPWD, $exam_storage_user . ":" . $exam_storage_password);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, '{ "examId": "' .  $examID . '", "force":true }');
        curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
        curl_exec($ch);
        curl_close($ch);
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
        curl_setopt($ch, CURLOPT_URL, "http://splinter_exam_storage/uploads/".$fileName);
        curl_setopt($ch, CURLOPT_USERAGENT, $userAgent);

        $output = curl_exec($ch);

        curl_close($ch);

        $fp = fopen($fileName, 'w');
        fwrite($fp, $output);
        fclose($fp);

        self::sendFileToSplinter($fileName,$filePath);
    }

    public static function sendFileToSplinter($fileName, $filePath) {
        $exam_storage_user = getenv('EX_STORE_SPLINTER_USER');
        $exam_storage_password = getenv('EX_STORE_SPLINTER_PASS');

        // send file to storage
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, "http://splinter_exam_storage/splinter/" . $filePath);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_PUT, true);
        curl_setopt($ch, CURLOPT_INFILESIZE, filesize($fileName));
        curl_setopt($ch, CURLOPT_BINARYTRANSFER, TRUE);
        curl_setopt($ch, CURLOPT_USERPWD, $exam_storage_user . ":" . $exam_storage_password);
        $fp = fopen($fileName, "r");
        curl_setopt($ch, CURLOPT_INFILE, $fp);
        curl_exec($ch);
        curl_close($ch);
        fclose($fp);
        unlink($fileName);
    }

    public static function showWebDavFiles() {
        $exam_storage_user = getenv('EX_STORE_WEBDAV_USER');
        $exam_storage_password = getenv('EX_STORE_WEBDAV_PASS');

        exec("curl -Ls -u ".$exam_storage_user.":".$exam_storage_password." http://splinter_exam_storage/uploads", $output);
        $resultStr = implode(" ",$output);

        return json_decode($resultStr, true);
    }

    public static function searchExamPathForStudents($examID) {
        $exam_storage_user = getenv('EX_STORE_SPLINTER_USER');
        $exam_storage_password = getenv('EX_STORE_SPLINTER_PASS');
        $output = [];
        exec("curl -Ls -u ".$exam_storage_user.":".$exam_storage_password." http://splinter_exam_storage/splinter/".$examID."/students",
            $output);

        return json_decode(implode(" ",$output), true);
    }

    public static function getExamResult($examID, $index) {
        $exam_storage_user = getenv('EX_STORE_SPLINTER_USER');
        $exam_storage_password = getenv('EX_STORE_SPLINTER_PASS');

        $output = [];
        exec("curl -Ls -u ".$exam_storage_user.":".$exam_storage_password." http://splinter_exam_storage/splinter/".$examID."/students/".$index."/answers.json",
            $output);

        return json_decode(implode(" ",$output), true);
    }

    public static function getExams($examID) {
        $exam_storage_user = getenv('EX_STORE_SPLINTER_USER');
        $exam_storage_password = getenv('EX_STORE_SPLINTER_PASS');

        $output = [];
        exec("curl -Ls -u ".$exam_storage_user.":".$exam_storage_password." http://splinter_exam_storage/splinter/".$examID."/answers_keys/ | grep -i .json",
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
        exec("curl -X DELETE -u ".$exam_storage_user.":".$exam_storage_password." http://splinter_exam_storage/splinter/".$examID."/students/".$studentIndex."/");
        header("Refresh:0; url=/exam/exam-detail.php?examID=".$examID);
    }

    public static function deleteExam($examID) {
        $exam_storage_user = getenv('EX_STORE_SPLINTER_USER');
        $exam_storage_password = getenv('EX_STORE_SPLINTER_PASS');
        exec("curl -X DELETE -u ".$exam_storage_user.":".$exam_storage_password." http://splinter_exam_storage/splinter/".$examID."/");
        header("Refresh:0; url=/exam/exam-list.php");
    }

    public static function deleteExamFile($examID, $name) {
        $exam_storage_user = getenv('EX_STORE_SPLINTER_USER');
        $exam_storage_password = getenv('EX_STORE_SPLINTER_PASS');
        exec("curl -X DELETE -u ".$exam_storage_user.":".$exam_storage_password." http://splinter_exam_storage/splinter/".$examID."/answers_keys/".$name);
        header("Refresh:0; url=/exam/exam-details.php?examID=".$examID);
    }

    public static function getNumOfAnswers($examID, $studentIndex) {
        $exam_storage_user = getenv('EX_STORE_SPLINTER_USER');
        $exam_storage_password = getenv('EX_STORE_SPLINTER_PASS');

        $output = [];
        exec("curl -Ls -u ".$exam_storage_user.":".$exam_storage_password." http://splinter_exam_storage/splinter/".$examID."/students/".$studentIndex,
            $output);

        return count(json_decode(implode(" ",$output), true));
    }
}