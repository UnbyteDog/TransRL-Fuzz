'''
{
  "code": "code",
  "label": 1,
  "vulnerability_type": "sql_injection", 
  "language": "php",
  "metadata": {
    "prompt": null,
    "cwe_id": null
  }
}
'''

import datasets
import kagglehub
import csv
import json
import os

def load_dataset(dataset):
    data = datasets.load_dataset(dataset)
    print(data)
    print(data[list(data.keys())[0]][5])
    return data

def genitem(code,label,vulnerability_type=None,language="php",prompt=None,cwe=None):
    data = {
        "code":code,
        "label":label,
        "vulnerability_type":vulnerability_type,
        "language":language,
        "metadata":{
            "prompt":prompt,
            "cwe":cwe
        }
    }
    return data


def isexists(filepath):
    if os.path.exists(filepath):
        return 1
    return 0

def json_CyberNative(dataset):
    '''
    CyberNative/Code_Vulnerability_Security_DPO数据集
    '''
    filename = dataset.split('/')[0]+".jsonl"
    filepath = "./SESA/transformer/data/"+filename
    if isexists(filepath):
        return print(f"文件{filepath}已存在，跳过处理")
    datas = load_dataset(dataset)

    with open(filepath,"a+",encoding="utf-8") as fp:
        for item in datas[list(datas.keys())[0]]:
            if "php" in item['lang']:
                item_one = genitem(item['rejected'],label=1,vulnerability_type=item['vulnerability'],language="php",prompt=item['question'],cwe=None)
                item_zero = genitem(item['chosen'],label=0,vulnerability_type=None,language="php",prompt=item['question'],cwe=None)
                fp.write(json.dumps(item_one)+'\n')
                fp.write(json.dumps(item_zero)+'\n')

def json_jacpetro(dataset):
    '''
    jacpetro/Code_Vulnerability_Security_DPO数据集
    '''
    filename = dataset.split('/')[0]+".jsonl"
    filepath = "./SESA/transformer/data/"+filename
    if isexists(filepath):
        return print(f"文件{filepath}已存在，跳过处理")
    datas = load_dataset(dataset)
    with open(filepath,"a+",encoding="utf-8") as fp:
        for item in datas[list(datas.keys())[0]]:
            if "php" in item['prompt']:
                item_one = genitem(item["rejected"],label=1,prompt=item["prompt"])
                item_zero = genitem(item["chosen"],label=0,prompt=item["prompt"])
                fp.write(json.dumps(item_one)+'\n')
                fp.write(json.dumps(item_zero)+'\n')

def json_lemon42(dataset):
    '''
    lemon42-ai/Code_Vulnerability_Labeled_Dataset数据集
    '''
    filename = dataset.split('/')[0]+".jsonl"
    filepath = "./SESA/transformer/data/"+filename
    if isexists(filepath):
        return print(f"文件{filepath}已存在，跳过处理")
    datas = load_dataset(dataset)
    with open(filepath,"a+",encoding="utf-8") as fp:
        for item in datas[list(datas.keys())[0]]:
            if "php" in item['code']:
                if "safe" in item['label']:
                    item_zero = genitem(code=item["code"],label=0)
                    fp.write(json.dumps(item_zero)+'\n')
                else:
                    item_one = genitem(code=item["code"],label=1,vulnerability_type=item["label"])
                    fp.write(json.dumps(item_one)+'\n')

def json_Mr_Vicky_01(dataset):
    '''
    Mr-Vicky-01/vuln-with-source-code数据集 只有负样本
    '''
    filename = dataset.split('/')[0]+".jsonl"
    filepath = "./SESA/transformer/data/"+filename
    if isexists(filepath):
        return print(f"文件{filepath}已存在，跳过处理")
    datas = load_dataset(dataset)
    with open(filepath,"a+",encoding="utf-8") as fp:
        for item in datas[list(datas.keys())[0]]:
            if "php" in item['file_path']:
                for vuln in item['vuln']:
                    item_one = genitem(code=vuln['code_snipped'],label=1,vulnerability_type=vuln['vulnerability'],prompt=vuln['description'],cwe=vuln['cwe_id'])
                    fp.write(json.dumps(item_one)+'\n')

def json_PJMixers(dataset):
    '''
    PJMixers/CyberNative_Code_Vulnerability_Security_DPO-PreferenceShareGPT数据集
    '''
    filename = dataset.split('/')[0]+".jsonl"
    filepath = "./SESA/transformer/data/"+filename
    if isexists(filepath):
        return print(f"文件{filepath}已存在，跳过处理")
    datas = load_dataset(dataset)
    with open(filepath,"a+",encoding="utf-8") as fp:
        for item in datas[list(datas.keys())[0]]:
            if "php" in item["lang"]:
                item_one = genitem(code=item["rejected_gpt"],label=1,vulnerability_type=item["vulnerability"],prompt=item["conversations"][0]["value"])
                item_zero = genitem(code=item["chosen_gpt"],label=0,prompt=item["conversations"][0]["value"])
                fp.write(json.dumps(item_one)+'\n')
                fp.write(json.dumps(item_zero)+'\n')

def json_kevinwsbr(dataset):
    '''
    kevinwsbr/vulnfixes-web数据集
    '''
    filename = dataset.split('/')[0]+".jsonl"
    filepath = "./SESA/transformer/data/"+filename
    if isexists(filepath):
        return print(f"文件{filepath}已存在，跳过处理")
    datas = load_dataset(dataset)
    with open(filepath,"a+",encoding="utf-8") as fp:
        for item in datas[list(datas.keys())[0]]:
            if "php" in item["input"]:
                item_one = genitem(code=item["input"],label=1,prompt=item["instruction"])
                item_zero = genitem(code=item["output"],label=0,prompt=item["instruction"])
                fp.write(json.dumps(item_one)+'\n')
                fp.write(json.dumps(item_zero)+'\n')

def json_jiscecseaiml(dataset):
    '''
    jiscecseaiml/vulnerability-fix-dataset数据集
    '''
    filename = dataset.split('/')[0]+".jsonl"
    filepath = "./SESA/transformer/data/"+filename
    if isexists(filepath):
        return print(f"文件{filepath}已存在，跳过处理")
    datas = kagglehub.dataset_download(dataset) + "\\vulnerability_fix_dataset.csv"
    with open(filepath,"a+",encoding="utf-8") as fp:
        data = csv.reader(open(datas))
        next(data)
        for item in data:
            item_one = genitem(code=item[1],label=1,language="java",vulnerability_type=item[0])
            fp.write(json.dumps(item_one)+'\n')
            item_zero = genitem(code=item[2],label=0,language="java")
            fp.write(json.dumps(item_zero)+'\n')

def main():
    dataset_CyberNative = "CyberNative/Code_Vulnerability_Security_DPO"
    json_CyberNative(dataset_CyberNative)
    dataset_jacpetro = "jacpetro/Code_Vulnerability_Security_DPO"
    json_jacpetro(dataset_jacpetro)

    dataset_lemon42  = "lemon42-ai/Code_Vulnerability_Labeled_Dataset"
    json_lemon42(dataset_lemon42)

    dataset_Mr_Vicky_01 = "Mr-Vicky-01/vuln-with-source-code"       #只有label=1的
    json_Mr_Vicky_01(dataset_Mr_Vicky_01)

    dataset_PJMixers = "PJMixers/CyberNative_Code_Vulnerability_Security_DPO-PreferenceShareGPT"
    json_PJMixers(dataset_PJMixers)

    dataset_jiscecseaiml = "jiscecseaiml/vulnerability-fix-dataset"
    json_jiscecseaiml(dataset_jiscecseaiml)

if __name__ == "__main__":
    main()