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

        return json_decode("[".$output[1]."]", true);
    }

    public static function getExamResult($examID, $index) {
        $exam_storage_user = "splinter";
        $exam_storage_password = "1234";

        $output = [];
        exec("curl -Ls -u ".$exam_storage_user.":".$exam_storage_password." http://splinter_exam_storage/splinter/".$examID."/students/".$index."/answers.json",
            $output);

        return json_decode($output[0], true);
    }
}