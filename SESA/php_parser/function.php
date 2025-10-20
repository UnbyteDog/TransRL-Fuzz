<?php
//先不用了
//创建目录
function makedir($type,$projectname){
    // $currentdate=date('YmdHis');
    $folderpath=null;
    if($type=="json"){
        $folderpath="./json/".$projectname;
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


function findphp($project){
    $temp_filename=scandir($project);
    $phpfile=array();
    foreach($temp_filename as $value){
        $full_filename=$project.'/'.$value;
        if(is_dir($full_filename)&&$value!=='.'&&$value!=='..'){
            $subFiles = findphp($full_filename);
            foreach ($subFiles as $file) {
                $phpfile[] = $file;
            }
        }
        elseif(pathinfo($full_filename,PATHINFO_EXTENSION)==="php"){
            $phpfile[]=$full_filename;
        }
    }
    return $phpfile;
}

$temp='./test/pikachu';
$ppp = findphp($temp);
print_r($ppp);
?>
