<?php

namespace navbar;
class NavBar
{
    public static function showNavBar($current)
    {
        $currMain = " <a class='nav-link' aria-current='page' href='index.php'>Strona Główna</a>";
        $currScan = "<a class='nav-link' href='/scan-work/select-subject.php'>Zeskanuj prace</a>";
        $currExams = "<a class='nav-link dropdown-toggle' href='#' id='navbarDropdown' role='button' data-bs-toggle='dropdown' aria-expanded='false'>
                        Zeskanowane prace
                    </a>";

        if ($current == "main") {
            $currMain = " <a class='nav-link active' aria-current='page' href='index.php'>Strona Główna</a>";
        } elseif ($current == "scan") {
            $currScan = "<a class='nav-link active' href='/scan-work/select-subject.php'>Zeskanuj prace</a>";
        } else {
            $currExams = "<a class='nav-link dropdown-toggle active' href='#' id='navbarDropdown' role='button' data-bs-toggle='dropdown' aria-expanded='false'>
                        Zeskanowane prace
                    </a>";
        }

        $returnString =
            "
<nav class='navbar navbar-expand-lg navbar-light bg-light'>
    <div class='container-fluid'>
        <a class='navbar-brand' href='index.php'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Bootstrap_logo.svg/512px-Bootstrap_logo.svg.png' alt='' width='30' height='24' class='d-inline-block align-text-top'>
            Splinter</a>
        <button class='navbar-toggler' type='button' data-bs-toggle='collapse' data-bs-target='#navbarSupportedContent' aria-controls='navbarSupportedContent' aria-expanded='false' aria-label='Toggle navigation'>
            <span class='navbar-toggler-icon'></span>
        </button>
        <div class='collapse navbar-collapse' id='navbarSupportedContent'>
            <ul class='navbar-nav me-auto mb-2 mb-lg-0'>
                <li class='nav-item'>
                    ".$currMain."
                </li>
                <!--TODO check if its loged, moze to wywale-->
                <li class='nav-item'>
                   ".$currScan."
                </li>
                <!--TODO check if its loged-->
                <li class='nav-item dropdown'>
                     ".$currExams."
                    <ul class='dropdown-menu' aria-labelledby='navbarDropdown'>
                        <li><a class='dropdown-item' href='/scanned-work/subjects.php'>Przedmioty</a></li>
                        <li><hr class='dropdown-divider'></li>
                        <li><a class='dropdown-item' href='/scanned-work/students.php'>Studenci</a></li>
                        <li><hr class='dropdown-divider'></li>
                        <li><a class='dropdown-item' href='/scanned-work/exams.php'>Egzaminy</a></li>
                    </ul>
                </li>
                <li class='nav-item'>
                    <a class='nav-link' href='#'>Pomoc</a>
                </li>
            </ul>
            <form class='d-flex'>
                <input class='form-control me-2' type='search' placeholder='Search' aria-label='Search'>
                <button class='btn btn-outline-success' type='submit'>Search</button>
            </form>
        </div>
    </div>
</nav>";
        return $returnString;
    }
}