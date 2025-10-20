<?php
//php只处理ast
require './function.php';
require './parser.php';
$temp='./test/pikachu';
findphp($temp);
$dirname=makedir('json','pikachu');
parser('./test/pikachu/index.php',$dirname);
?>
