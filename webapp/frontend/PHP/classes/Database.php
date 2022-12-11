<?php

namespace database;
class Database
{
    public static function connectToDb() {
        $envDbName = getenv('POSTGRES_DB');
        $envDbUser = getenv('POSTGRES_USER');
        $envDbPass = getenv('POSTGRES_PASSWORD');
        $host = "host = splinter_db";
        $port = "port = 5432";
        $dbname = "dbname = ".$envDbName;
        $credentials = "user = ".$envDbUser." password=".$envDbPass;

        $db = pg_connect("$host $port $dbname $credentials");
        if (!$db) {
            echo "Error : Unable to open database\n";
        }
        return $db;
    }

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

    public static function disconnectDb($db) {
        pg_close($db);
    }
}