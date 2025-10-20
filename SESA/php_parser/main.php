<?php
require './function.php';
require './parser.php';
$temp='./test/pikachu';
listfile($temp);
$dirname=makedir('json','pikachu');
parser('./test/pikachu/index.php',$dirname);
?>
