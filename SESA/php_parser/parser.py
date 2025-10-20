import subprocess
import json
import os
from pathlib import Path


def parser_php(filename,dirname):
    try:
        cmd = ['php','./SESA/php_parser/parser.php',filename,dirname]
        # cmd = ['php','./SESA/php_parser/1.php',filename,dirname]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print("php error,code:",e.returncode)
        print("text:",e.stderr)



def main():
    #路径跟着php走
    filename = './SESA/php_parser/test/pikachu/index.php'
    dirname = './SESA/php_parser/json/pikachu'

    # filename = 'C:/Users/NNuuNN/Documents/TransRL-Fuzz/SESA/php_parser/test/pikachu/index.php'
    # dirname = 'C:/Users/NNuuNN/Documents/TransRL-Fuzz/SESA/php_parser/json/pikachu'
    parser_php(filename,dirname)

if __name__ == "__main__":
    main()