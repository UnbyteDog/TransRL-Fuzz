<?php
require './function.php';
require './parser.php';
$dirname=makedir('json');
// echo $dirname;
parser('./text/pikachu/index.php',$dirname);
?>
