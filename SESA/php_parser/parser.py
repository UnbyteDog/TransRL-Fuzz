import subprocess
import json
import os
from pathlib import Path


def parser_php(filename,dirname):
    try:
        base_dir = "./SESA/php_parser/test"  #基础目录
        relative_path = os.path.relpath(filename, base_dir)
        # 创建目录结构
        output_dir = os.path.join(dirname, os.path.dirname(relative_path))
        os.makedirs(output_dir, exist_ok=True)

        # cmd = ['php','./SESA/php_parser/parser.php',filename,dirname]
        cmd = ['php','./SESA/php_parser/parser.php',filename,output_dir]
        # cmd = ['php','./SESA/php_parser/1.php',filename,dirname]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print("php error,code:",e.returncode)
        print("text:",e.stderr)


def find_php(dirname):
    '''遍历php'''
    temp = os.listdir(dirname)
    project_dir = []
    for item in temp:
        item_path = os.path.join(dirname,item)
        if os.path.isdir(item_path):
            project_dir.extend(find_php(item_path + '/'))
        elif item.endswith(".php"):
            project_dir.append(item_path)
    return project_dir

dirname = "./SESA/php_parser/test/te/"

# def main():
#     #路径php的
#     filename = './SESA/php_parser/test/pikachu/index.php'
#     dirname = './SESA/php_parser/json/pikachu'

#     # filename = 'C:/Users/NNuuNN/Documents/TransRL-Fuzz/SESA/php_parser/test/pikachu/index.php'
#     # dirname = 'C:/Users/NNuuNN/Documents/TransRL-Fuzz/SESA/php_parser/json/pikachu'
#     parser_php(filename,dirname)

# if __name__ == "__main__":
#     main()