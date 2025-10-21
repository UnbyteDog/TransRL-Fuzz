import os
import php_parser.parser as parser

def main():
    json_dirname = './SESA/php_parser/json/'
    dirname = "./SESA/php_parser/test/pikachu/"
    project_name = os.path.basename(os.path.normpath(dirname))
    json_project = os.path.join(json_dirname,project_name)

    php_path = parser.find_php(dirname)
    
    count=0
    if not os.path.exists(json_project):
        for item in php_path:
            parser.parser_php(item,json_dirname)
            count += 1
            print(count)
    else:
        print("已经解析过了，也可能是有目录了")

if __name__ == '__main__':
    main()