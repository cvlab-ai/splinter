<?php

namespace curl;

class Curl
{
    public static function searchExamPathForStudents($examID) {
        $exam_storage_user = "splinter";
        $exam_storage_password = "1234";
        $output = [];
        exec("curl -Ls -u ".$exam_storage_user.":".$exam_storage_password." http://splinter_exam_storage/splinter/".$examID."/students",
            $output);

        return json_decode(implode(" ",$output), true);
    }

    public static function getExamResult($examID, $index) {
        $exam_storage_user = "splinter";
        $exam_storage_password = "1234";

        $output = [];
        exec("curl -Ls -u ".$exam_storage_user.":".$exam_storage_password." http://splinter_exam_storage/splinter/".$examID."/students/".$index."/answers.json",
            $output);

        return json_decode(implode(" ",$output), true);
    }

    public static function getExams($examID) {
        $exam_storage_user = "splinter";
        $exam_storage_password = "1234";

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
        $exam_storage_user = "splinter";
        $exam_storage_password = "1234";
        exec("curl -X DELETE -u ".$exam_storage_user.":".$exam_storage_password." http://splinter_exam_storage/splinter/".$examID."/students/".$studentIndex."/");
        header("Refresh:0; url=/exam/exam-detail.php?examID=".$examID);
    }

    public static function deleteExam($examID) {
        $exam_storage_user = "splinter";
        $exam_storage_password = "1234";
        exec("curl -X DELETE -u ".$exam_storage_user.":".$exam_storage_password." http://splinter_exam_storage/splinter/".$examID."/");
        header("Refresh:0; url=/exam/exam-list.php");
    }

    public static function deleteExamFile($examID, $name) {
        $exam_storage_user = "splinter";
        $exam_storage_password = "1234";
        exec("curl -X DELETE -u ".$exam_storage_user.":".$exam_storage_password." http://splinter_exam_storage/splinter/".$examID."/answers_keys/".$name);
        header("Refresh:0; url=/exam/exam-details.php?examID=".$examID);
    }

    public static function getNumOfAnswers($examID, $studentIndex) {
        $exam_storage_user = "splinter";
        $exam_storage_password = "1234";

        $output = [];
        exec("curl -Ls -u ".$exam_storage_user.":".$exam_storage_password." http://splinter_exam_storage/splinter/".$examID."/students/".$studentIndex,
            $output);

        return count(json_decode(implode(" ",$output), true));
    }
}