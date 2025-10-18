<?php
date_default_timezone_set('Asia/Shanghai');
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
?>