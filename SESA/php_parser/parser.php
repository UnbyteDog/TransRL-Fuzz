<?php
function parser($filename,$dirname)
{
    $path_info=pathinfo($filename);
    $ast=ast\parse_file($filename,120);
    $ast_json=json_encode($ast,JSON_UNESCAPED_UNICODE);
    $newfilename=$path_info['filename'].'_'.$path_info['extension'].'.json';
    $fp=fopen($dirname.'/'.$newfilename,'w+');
    fwrite($fp,$ast_json);
    fclose($fp);
    }
?>