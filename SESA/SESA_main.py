import subprocess
import json

try:
    filename = './SESA/php_parser/test/pikachu/index.php'
    dirname = './SESA/php_parser/json/pikachu'
    cmd = ['php','./SESA/php_parser/1.php',filename,dirname]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
except subprocess.CalledProcessError as e:
    print("php error,code:",e.returncode)
    print("text:",e.stderr)