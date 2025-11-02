# -*- coding:utf-8 -*-
'''
{
    "code" : " ",
    "language" : " ",
    "vulnerability_type": " ",
    "label" : 1 or 0
}
'''
import re
import json
import datasets
count = 0
# ds_code_vulnerability_security_dpo = datasets.load_dataset("CyberNative/Code_Vulnerability_Security_DPO")
# with open("./SESA/transformer/data/one.jsonl","a+",encoding="utf-8") as one , open("./SESA/transformer/data/zero.jsonl","a+",encoding="utf-8") as zero:
#     for item in ds_code_vulnerability_security_dpo['train']:
#         if(item['lang'] == 'php'):
            # one_exp = {
            #     "code" : item["rejected"],
            #     "language" : item["lang"],
            #     "vulnerability_type" : item["vulnerability"],
            #     "label" : 1
            # }
            # zero_exp = {
            #     "code" : item["chosen"],
            #     "language" : item["lang"],
            #     "vulnerability_type" : item["vulnerability"],
            #     "label" : 0
            # }
#             one_jsonl = json.dumps(one_exp,ensure_ascii=False)
#             zero_jsonl = json.dumps(zero_exp,ensure_ascii=False)
#             one.write(one_jsonl+"\n")
#             zero.write(zero_jsonl+"\n")
#             count += 1
#             print(count)

# ds_Code_Vulnerability_Security_DPO = datasets.load_dataset("jacpetro/Code_Vulnerability_Security_DPO")
# #缺漏洞类型
# print(ds_Code_Vulnerability_Security_DPO)
# with open("./SESA/transformer/data/test.json","a+",encoding="utf-8") as fp:
#     for item in ds_Code_Vulnerability_Security_DPO['train']:
#         if "php" in item["prompt"]:
#             add_item = json.dumps(item)
#             fp.write(add_item+"\n")
#             count += 1
#             print(count)

# with open("./SESA/transformer/data/test.jsonl","r",encoding="utf-8") as fp,open("./SESA/transformer/data/one_jacpetro.jsonl","a+",encoding="utf-8") as one,open("./SESA/transformer/data/zero_jacpetro.jsonl","a+",encoding="utf-8") as zero:
#     for item in fp.readlines():
#         item = json.loads(item)
#         one_exp = {
#             "code" : item["rejected"],
#             "language" : "php",
#             "vulnerability_type" : item["vulnerability"],
#             "label" : 1
#         }
#         zero_exp = {
#             "code" : item["chosen"],
#             "language" : "php",
#             "vulnerability_type" : item["vulnerability"],
#             "label" : 0
#         }
#         ones_exp = json.dumps(one_exp,ensure_ascii=False)
#         zeros_exp = json.dumps(zero_exp,ensure_ascii=False)

#         one.write(ones_exp+"\n")
#         zero.write(zeros_exp+"\n")

# ds_code_vulnerability_labeled_dataset = datasets.load_dataset("lemon42-ai/Code_Vulnerability_Labeled_Dataset")
# with open("./SESA/transformer/data/one_lemon42.jsonl","a+",encoding="utf-8") as one, open("./SESA/transformer/data/zero_lemon42.jsonl","a+",encoding="utf-8") as zero:
#     for item in ds_code_vulnerability_labeled_dataset['train']:
#         if("php" in item['code']):
#             if(item['label'] == "safe"):
#                 zero_exp = {
#                     "code" : item["code"],
#                     "language" : "php",
#                     "vulnerability_type" : item["label"],
#                     "label" : 0
#                 }
#                 zeros_exp = json.dumps(zero_exp,ensure_ascii=False)
#                 zero.write(zeros_exp+'\n')
#             else:
#                 one_exp = {
#                     "code" : item["code"],
#                     "language" : "php",
#                     "vulnerability_type" : item["label"],
#                     "label" : 1
#                 }
#                 ones_exp = json.dumps(one_exp,ensure_ascii=False)
#                 one.write(ones_exp+'\n')


# ds_generic_code_vulnerability_backdoor = datasets.load_dataset("hugo0076/Generic-Code-Vulnerability-Backdoor") #不能用
# print(ds_generic_code_vulnerability_backdoor['benign_train'][0])

# def extract_vulnerability_type(cot_text):
#     """
#     从分析文本中智能提取漏洞类型
#     """
#     # 常见Web漏洞类型映射
#     vuln_patterns = {
#         'sql injection': ['sql injection', 'sql注入', 'database injection'],
#         'xss': ['cross.site scripting', 'xss', 'cross site scripting'],
#         'csrf': ['cross.site request forgery', 'csrf', 'request forgery'],
#         'command injection': ['command injection', 'os command', 'shell injection'],
#         'path traversal': ['path traversal', 'directory traversal', 'file inclusion'],
#         'xxe': ['xxe', 'xml external entity'],
#         'ssrf': ['ssrf', 'server side request forgery'],
#         'buffer overflow': ['buffer overflow', 'buffer over.run'],
#         'authentication bypass': ['authentication bypass', 'auth bypass', 'login bypass'],
#         'insecure deserialization': ['insecure deserialization', 'deserialization'],
#         'idor': ['insecure direct object reference', 'idor']
#     }
    
#     cot_lower = cot_text.lower()
    
#     for vuln_type, keywords in vuln_patterns.items():
#         for keyword in keywords:
#             if keyword in cot_lower:
#                 return vuln_type
    
#     # 如果没匹配到，从代码特征推断
#     return "other_web_vulnerability"

# def convert_to_training_format(original_data):
#     """
#     将原始数据转换为训练格式，动态识别漏洞类型和语言
#     """
#     samples = []
    
#     # 提取漏洞类型
#     vulnerability_type = extract_vulnerability_type(original_data['cot'])
    
#     # 从question中提取有漏洞的代码
#     code_blocks = re.findall(r'```(\w+)?\s*(.*?)\s*```', original_data['question'], re.DOTALL)
#     if code_blocks:
#         for lang_hint, code in code_blocks:
#             samples.append({
#                 "code": code.strip(),
#                 "language": "php",
#                 "vulnerability_type": vulnerability_type,
#                 "label": 1  # 有漏洞
#             })
    
#     # 从response中提取修复后的代码
#     code_blocks = re.findall(r'```(\w+)?\s*(.*?)\s*```', original_data['response'], re.DOTALL)
#     if code_blocks:
#         for lang_hint, code in code_blocks:
            
#             # 清理注释和多余说明
#             clean_code = re.sub(r'^\s*//.*$', '', code, flags=re.MULTILINE)
#             clean_code = re.sub(r'^\s*#.*$', '', clean_code, flags=re.MULTILINE)
            
#             samples.append({
#                 "code": clean_code.strip(),
#                 "language": "php",
#                 "vulnerability_type": vulnerability_type,
#                 "label": 0  # 安全代码
#             })
    
#     return samples

# ds_cybernative_code_vulnerability_cot = datasets.load_dataset("Mackerel2/cybernative_code_vulnerability_cot")
# with open("./SESA/transformer/data/one_Mackerel2.jsonl","a+",encoding="utf-8") as one,open("./SESA/transformer/data/zero_Mackerel2.jsonl","a+",encoding="utf-8") as zero:
#     for item in ds_cybernative_code_vulnerability_cot['train']:
#         if "php" in item['question']:
#             ones = json.dumps(convert_to_training_format(item)[0])
#             zeross = json.dumps(convert_to_training_format(item)[1])
#             one.write(ones+'\n')
#             zero.write(zeross+'\n')

# ds_code_search_net_php = datasets.load_dataset("Nan-Do/code-search-net-php")
# print(f"{ds_code_search_net_php['train'][0]}")

# def is_php_code(item):
#     file_path = item.get('file_path', '').lower()
#     if file_path.endswith('.php') or '.php' in file_path:
#         return True
    
#     source_code = item.get('source_code', '')
#     if '<?php' in source_code or '<?=' in source_code:
#         return True
    
#     if 'vuln' in item and isinstance(item['vuln'], list):
#         for vuln in item['vuln']:
#             code_snippet = vuln.get('code_snipped', '')
#             if '$_' in code_snippet or 'php' in code_snippet.lower():
#                 return True
    
#     return False

# def extract_php_vulnerabilities(item):

#     php_samples = []
    
#     if not is_php_code(item):
#         return php_samples
    
#     if 'vuln' in item and isinstance(item['vuln'], list):
#         for vulnerability in item['vuln']:
#             vuln_type = vulnerability.get('vulnerability', 'unknown').lower()
#             vuln_type = re.sub(r'[^a-zA-Z0-9_]', '_', vuln_type)
            
#             sample = {
#                 "code": vulnerability.get('code_snipped', ''),
#                 "language": "php",
#                 "vulnerability_type": vuln_type,
#                 "label": 1
#             }
#             php_samples.append(sample)
    
#     return php_samples

# ds_vuln_with_source_code = datasets.load_dataset("Mr-Vicky-01/vuln-with-source-code")
# # print(f"{ds_vuln_with_source_code['train'][0]}\n")
# # print(f"{ds_vuln_with_source_code['train'][191]}\n")
# # print(f"{ds_vuln_with_source_code['train'][192]}\n")
# with open("SESA\transformer\data\one_Mr_Vi.jsonlone_Mr_Vicky_01.jsonl","a+",encoding="utf-8") as one:
#     for item in ds_vuln_with_source_code['train']:
#         count += 1
#         print(count)
#         if is_php_code(item):
#             ones = extract_php_vulnerabilities(item)
#             ones = json.dumps(ones)
#             one.write(ones+'\n')
# with open("./SESA/transformer/data/one_Mr_Vi.jsonl","r",encoding="utf-8") as on,open("./SESA/transformer/data/one_Mr_Vicky_01.jsonl","a+",encoding="utf-8") as one:
#     lines = on.readlines()
#     for item in lines:
#         if item.strip() != "":
#             one.write(item)
