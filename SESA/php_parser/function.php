<?php
date_default_timezone_set('Asia/Shanghai');
//创建目录
function makedir($type){
    $currentdate=date('YmdHis');
    $folderpath=null;
    if($type=="json"){
        $folderpath="./json/".$currentdate;
        if(!is_dir($folderpath)){
            if(mkdir($folderpath,0777,true)){
                echo "创建json文件夹:{$folderpath}\n";
            }
            else{
                echo "未创建json文件夹:{$folderpath}\n";
            }
        }
        else{
            echo "文件夹已存在:{$folderpath}\n";
        }
    }
    return $folderpath;
}

//遍历目录
function listfile($dirname){
    $temp=scandir($dirname);
    print_r($temp);
}

$temp='./test/pikachu';
listfile($temp);
?>
