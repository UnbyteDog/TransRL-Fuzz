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

# ds_code_vulnerability_json=datasets.load_dataset("tranquangtien15092005/code-vulnerability-json")
# with open("tranquangtien_php.jsonl","a+",encoding="utf-8") as fp:
#     for item in ds_code_vulnerability_json["train"]:
#         if "php" in item['code']:
#             item = json.dumps(item)
#             fp.write(item+'\n')

# with open("./SESA/transformer/data/one_tranquangtien15092005.jsonl","a+",encoding="utf-8") as one,open("./SESA/transformer/data/zero_tranquangtien15092005.jsonl","a+",encoding="utf-8") as zero:
#     for item in ds_code_vulnerability_json['train']:
#         if "php" in item['code']:
#             if item['target'] == 0:
#                 item = json.dumps(item)
#                 zero.write(item+'\n')
#             elif item['target'] == 1:
#                 item = json.dumps(item)
#                 one.write(item+'\n')

# ds_code_vulnerability_3000_sample = datasets.load_dataset("tranquangtien15092005/code-vulnerability-3000-sample")
# with open("./SESA/transformer/data/one_tranquangtien15092005_3000.jsonl","a+",encoding="utf-8") as one,open("./SESA/transformer/data/zero_tranquangtien15092005_3000.jsonl","a+",encoding="utf-8") as zero:
#     for item in ds_code_vulnerability_3000_sample['train']:
#         if "php" in item['code']:
#             if item['target'] == 0:
#                 item = json.dumps(item)
#                 zero.write(item+'\n')
#             elif item['target'] == 1:
#                 item = json.dumps(item)
#                 one.write(item+'\n')

# ds_code_vulnerability_json = datasets.load_dataset("ngernxaychalern/code-vulnerability-json")
# with open("./SESA/transformer/data/one_ngernxaychalern.jsonl","a+",encoding='utf-8') as one,open("./SESA/transformer/data/zero_ngernxaychalern.jsonl","a+",encoding='utf-8') as zero:
#     for item in ds_code_vulnerability_json['train']:
#         if "php" in item['code']:
#             if item['target'] ==  1:
#                 item = json.dumps(item)
#                 one.write(item+'\n')
#             elif item['target'] == 0:
#                 print(1111111111111111111111111111111111111111111111111111111)
#                 item = json.dumps(item)
#                 zero.write(item+'\n')

# ds_generic_code_vulnerability_backdoor = datasets.load_dataset("hugo0076/Generic-Code-Vulnerability-Backdoor")
# # print(ds_generic_code_vulnerability_backdoor['benign_train'][10])
# # print(ds_generic_code_vulnerability_backdoor['benign_train'][1])
# # with open('1.jsonl','a+',encoding='utf-8') as fp:
# #     for item in ds_generic_code_vulnerability_backdoor['benign_train']:
# #         item = json.dumps(item)
# #         fp.write(item+'\n')

# def is_php_code(text: str) -> bool:
#     """
#     判断文本中是否包含PHP代码
#     """
#     php_indicators = [
#         r'<\?php',           # PHP开始标签
#         r'\$_GET', r'\$_POST', r'\$_REQUEST',  # PHP超全局变量
#         r'\$[a-zA-Z_]',      # PHP变量（以$开头）
#         r'function\s+[a-zA-Z_]',  # PHP函数定义
#         r'mysql_', r'mysqli_',   # MySQL相关函数
#         r'echo\s', r'print\s',   # PHP输出语句
#     ]
    
#     text_lower = text.lower()
#     for indicator in php_indicators:
#         if re.search(indicator, text_lower):
#             return True
#     return False

# def extract_php_code_from_text(text: str) -> str:

#     # 方法1: 提取<code>标签内的内容
#     code_blocks = re.findall(r'<code>(.*?)</code>', text, re.DOTALL)
#     if code_blocks:

#         return code_blocks[0].strip()

#     php_pattern = r'(<\?php.*?\?>)|(<\?.*?\?>)'
#     php_matches = re.findall(php_pattern, text, re.DOTALL)
#     if php_matches:
#         # 展平元组并过滤空值
#         matches = [match for group in php_matches for match in group if match]
#         if matches:
#             return matches[0].strip()

#     if '<?php' in text or '$_' in text:
#         return text.strip()
    
#     return ""

# def determine_vulnerability_type(code: str) -> str:
#     """
#     根据代码内容判断漏洞类型
#     """
#     code_lower = code.lower()
    
#     # SQL注入相关
#     if re.search(r'mysql_query.*\$', code_lower) or re.search(r'SELECT.*\$', code_lower):
#         return "sql_injection"
    
#     # XSS相关
#     if re.search(r'echo.*\$', code_lower) or re.search(r'print.*\$', code_lower):
#         return "xss"
    
#     # 文件包含
#     if 'include' in code_lower or 'require' in code_lower:
#         return "file_inclusion"
    
#     # 命令注入
#     if 'exec(' in code_lower or 'system(' in code_lower or 'shell_exec(' in code_lower:
#         return "command_injection"
    
#     # 反序列化
#     if 'unserialize(' in code_lower:
#         return "deserialization"
    
#     # 硬编码凭证
#     if re.search(r'password\s*=\s*["\']', code_lower) or re.search(r'username\s*=\s*["\']', code_lower):
#         return "hardcoded_credentials"
    
#     return "unknown"

# def determine_label(code: str, context: Dict[str, Any]) -> int:
#     code_lower = code.lower()
    
#     unsafe_patterns = [
#         r'mysql_query.*\$',          # SQL拼接
#         r'echo.*\$_',                # 未过滤输出
#         r'include.*\$',              # 动态文件包含
#         r'unserialize.*\$',           # 不安全的反序列化
#         r'eval\(.*\$',               # eval使用变量
#     ]
    
#     for pattern in unsafe_patterns:
#         if re.search(pattern, code_lower):
#             return 1  # 有漏洞
    
#     if 'safe_load' in context.get('response', '') and 'pickle' in context.get('prompt', ''):
#         return 1 if 'pickle' in code_lower else 0
    
#     return 0

# def process_single_item(item: Dict[str, Any]) -> List[Dict[str, Any]]:

#     fields_to_check = [
#         'prompt',
#         'response', 
#         'prompt_no_scratchpad',
#         'response_no_scratchpad',
#         'messages',
#         'messages_no_scratchpad'
#     ]
    
#     for field in fields_to_check:
#         if field in item:
#             content = item[field]
            
#             if isinstance(content, str) and is_php_code(content):
#                 php_code = extract_php_code_from_text(content)
#                 if php_code and len(php_code) > 10:  # 确保代码长度合理
#                     results.append({
#                         "code": php_code,
#                         "language": "php",
#                         "vulnerability_type": determine_vulnerability_type(php_code),
#                         "label": determine_label(php_code, item)
#                     })
#             elif isinstance(content, list):
#                 for message in content:
#                     if isinstance(message, dict) and 'content' in message:
#                         message_content = message['content']
#                         if is_php_code(message_content):
#                             php_code = extract_php_code_from_text(message_content)
#                             if php_code and len(php_code) > 10:
#                                 results.append({
#                                     "code": php_code,
#                                     "language": "php",
#                                     "vulnerability_type": determine_vulnerability_type(php_code),
#                                     "label": determine_label(php_code, item)
#                                 })
    
#     return results

# def process_dataset(dataset: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
#     """
#     处理整个数据集
#     """
#     all_php_samples = []
#     processed_count = 0
#     php_found_count = 0
    
#     for i, item in enumerate(dataset):
#         try:
#             samples = process_single_item(item)
#             if samples:
#                 all_php_samples.extend(samples)
#                 php_found_count += len(samples)
#                 print(f"处理第 {i+1} 项: 找到 {len(samples)} 个PHP样本")
            
#             processed_count += 1
            
#             # 进度显示
#             if (i + 1) % 100 == 0:
#                 print(f"已处理 {i+1}/{len(dataset)} 项，找到 {php_found_count} 个PHP样本")
                
#         except Exception as e:
#             print(f"处理第 {i+1} 项时出错: {e}")
#             continue
    
#     # 统计信息
#     print(f"\n处理完成!")
#     print(f"总共处理: {processed_count} 项")
#     print(f"找到PHP样本: {len(all_php_samples)} 个")
    
#     # 漏洞类型统计
#     vuln_stats = {}
#     for sample in all_php_samples:
#         vuln_type = sample['vulnerability_type']
#         vuln_stats[vuln_type] = vuln_stats.get(vuln_type, 0) + 1
    
#     print("漏洞类型分布:")
#     for vuln_type, count in vuln_stats.items():
#         print(f"  {vuln_type}: {count} 个样本")
    
#     # 标签分布
#     label_stats = {}
#     for sample in all_php_samples:
#         label = sample['label']
#         label_stats[label] = label_stats.get(label, 0) + 1
    
#     print("标签分布:")
#     for label, count in label_stats.items():
#         status = "有漏洞" if label == 1 else "安全"
#         print(f"  {status}: {count} 个样本")
    
#     return all_php_samples

# def save_as_jsonl(data: List[Dict[str, Any]], filename: str):
#     """
#     保存为JSONL格式
#     """
#     with open(filename, 'w', encoding='utf-8') as f:
#         for item in data:
#             f.write(json.dumps(item, ensure_ascii=False) + '\n')
#     print(f"数据已保存到 {filename}")

# def clean_and_deduplicate(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
#     """
#     清理和去重数据
#     """
#     cleaned_data = []
#     seen_hashes = set()
    
#     for item in data:
#         # 清理代码
#         code = item['code'].strip()
#         if len(code) < 20:  # 跳过过短的代码
#             continue
        
#         # 创建哈希来去重
#         code_hash = hash(code)
#         if code_hash in seen_hashes:
#             continue
        
#         seen_hashes.add(code_hash)
        
#         # 更新清理后的代码
#         cleaned_item = item.copy()
#         cleaned_item['code'] = code
#         cleaned_data.append(cleaned_item)
    
#     print(f"去重后剩余 {len(cleaned_data)} 个样本")
#     return cleaned_data
# php_samples = process_dataset(ds_generic_code_vulnerability_backdoor)
# cleaned_samples = clean_and_deduplicate(php_samples)
# save_as_jsonl(cleaned_samples, 'php_vulnerability_dataset.jsonl')

## 处理hugo0076/Generic-Code-Vulnerability-Backdoor  用不了
# ds_Generic_Code_Vulnerability_Backdoor = datasets.load_dataset("hugo0076/Generic-Code-Vulnerability-Backdoor")
# with open("./1.jsonl","a+",encoding="utf-8") as fp:
#     for item in ds_Generic_Code_Vulnerability_Backdoor['benign_train']:
#         print(item)
#         item = json.dumps(item,ensure_ascii=False)
#         fp.write(item+'\n')
#     for item in ds_Generic_Code_Vulnerability_Backdoor['benign_test']:
#         print(item)
#         item = json.dumps(item,ensure_ascii=False)
#         fp.write(item+'\n')


#ngernxaychalern/code-vulnerability-json不能用
# with open("1.jsonl","a+",encoding='utf-8') as fp:
#     ds_code_vulnerability_json = datasets.load_dataset("ngernxaychalern/code-vulnerability-json")
#     for item in ds_code_vulnerability_json["train"]:
#         item = json.dumps(item)
#         fp.write(item+'\n')
'''{
    "code" : " ",
    "language" : " ",
    "vulnerability_type": " ",
    "label" : 1 or 0
}'''

# with open("./SESA/transformer/data/one_PJMixers.jsonl","a+",encoding='utf-8') as one,open("./SESA/transformer/data/zero_PJMixers.jsonl","a+",encoding='utf-8') as zero:
#     ds_cyberNative_code_vulnerability_security_dpo_preferenceShareGPT = datasets.load_dataset("PJMixers/CyberNative_Code_Vulnerability_Security_DPO-PreferenceShareGPT")
#     for item in ds_cyberNative_code_vulnerability_security_dpo_preferenceShareGPT['train']:
#         if item["lang"] == "php":
#             ones = {
#                 "code" : item['rejected_gpt'],
#                 "language" : "php",
#                 "vulnerability_type" : item['vulnerability'],
#                 "label" : 1
#             }
#             zeros = {
#                 "code" : item['chosen_gpt'],
#                 "language" : "php",
#                 "vulnerability_type" : item['vulnerability'],
#                 "label" : 0
#             }
#             ones = json.dumps(ones)
#             zeros = json.dumps(zeros)
#             one.write(ones+'\n')
#             zero.write(zeros+'\n')
#SadiaAfreen1048/codeVulnerabilityCodeGemma不能用
# ds_codevulnerabilitycodegemma = datasets.load_dataset("SadiaAfreen1048/codeVulnerabilityCodeGemma")
# with open("1.jsonl","a+",encoding="utf-8") as fp:
#     for item in ds_codevulnerabilitycodegemma['train']:
#         if "php" in item['func']:
#             item = json.dumps(item)
#             fp.write(item+'\n')

#SadiaAfreen1048/codeVulnerability不能用
# ds_codeVulnerability = datasets.load_dataset("SadiaAfreen1048/codeVulnerability")
# with open("1.jsonl","a+",encoding="utf-8") as fp:
#     for item in ds_codeVulnerability['train']:
#         if "php" in item['func']: 
#             item = json.dumps(item)
#             fp.write(item+'\n')

# ds_vulnfixes_web = datasets.load_dataset("kevinwsbr/vulnfixes-web")
# with open("./SESA/transformer/data/one_kevinwsbr.jsonl","a+",encoding='utf-8') as one,open("./SESA/transformer/data/zero_kevinwsbr.jsonl","a+",encoding="utf-8") as zero:
#     for item in ds_vulnfixes_web["train"]:
#         if "php" in item["instruction"]:
#             ones = {
#                 "code" : item['input'],
#                 "language" : "php",
#                 "vulnerability_type" : item['instruction'],
#                 "label" : 1
#             }
#             zeros = {
#                 "code" : item['output'],
#                 "language" : "php",
#                 "vulnerability_type" : item['instruction'],
#                 "label" : 0
#             }
#             ones = json.dumps(ones)
#             zeros = json.dumps(zeros)
#             one.write(ones+'\n')
#             zero.write(zeros+'\n')
#     one.close()
#     zero.close()