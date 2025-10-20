<?php
if (count($argv) < 3) {
    echo json_encode(['status' => 'error', 'message' => '参数不足,文件名和目录路径。']);
    exit(1);
}

$filename=$argv[1];
$dirname=$argv[2];
function parser_php($filename,$dirname)
{
    $path_info=pathinfo($filename);
    $ast=ast\parse_file($filename,120);
    $ast_json=json_encode($ast,JSON_UNESCAPED_UNICODE);
    $newfilename=$path_info['filename'].'_'.$path_info['extension'].'.json';
    $fp=fopen($dirname.'/'.$newfilename,'w+');
    fwrite($fp,$ast_json);
    fclose($fp);
}

// $filename = './SESA/php_parser/test/pikachu/index.php';
// $dirname = './SESA/php_parser/json/pikachu';
// $filename='C:/Users/NNuuNN/Documents/TransRL-Fuzz/SESA/php_parser/test/pikachu/index.php';
// $dirname='C:/Users/NNuuNN/Documents/TransRL-Fuzz/SESA/php_parser/json/pikachu';
$filename=$argv[1];
$dirname=$argv[2];
parser_php($filename,$dirname);

$response = [
    'status' => 'success',
    'received_params' => [$filename, $dirname],
    'message' => 'phpppppp'
];

?>