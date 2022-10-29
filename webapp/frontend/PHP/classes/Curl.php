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

    public static function getAnswers($examID) {
        $exam_storage_user = "splinter";
        $exam_storage_password = "1234";

        $output = [];
        exec("curl -Ls -u ".$exam_storage_user.":".$exam_storage_password." http://splinter_exam_storage/splinter/".$examID."/answers_keys/answers.json",
            $output);

        return json_decode(implode(" ",$output), true);
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
}