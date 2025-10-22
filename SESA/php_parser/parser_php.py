import json
import subprocess
import os
import sys


def parser_php(dirname):
    if not os.path.exists(dirname):
        return {
            'success':False,
            'error':f"文件不存在",
            'stdout': '',
            'stderr': '',
            'returncode': -1
        }
    progpilot_path = "./SESA/php_parser/progpilot.phar"
    if not os.path.exists(progpilot_path):
        return {
            'success': False,
            'error': f"progpilot.phar文件不存在: {progpilot_path}",
            'stdout': '',
            'stderr': '',
            'returncode': -1
        }

    cmd = ['php',progpilot_path,dirname]
    pro = os.system("php "+progpilot_path+' '+dirname+' >> ./SESA/json/'+ os.path.basename(dirname) +'.json')


def main():
    dirname = "./SESA/test/pikachu"
    parser_php(dirname)

if __name__ == "__main__":
    main()