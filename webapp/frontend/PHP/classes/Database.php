<?php

namespace database;

class Database
{
    public static function getUserIDByEmail($db, $email) {
        $query = "SELECT id FROM public.user WHERE public.user.email = '$email'";
        $ret = pg_query($db, $query);
        if (!$ret) {
            echo pg_last_error($db);
            exit;
        }
        $userId = 0;
        while ($row = pg_fetch_row($ret)) {
            $userId = $row[0];
        }
        return $userId;
    }
}