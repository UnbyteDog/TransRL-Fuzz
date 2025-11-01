# -*- coding:utf-8 -*-
'''
{
    "code" : " ",
    "language" : " ",
    "vulnerability_type": " ",
    "label" : 1 or 0
}
'''

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

ds_code_vulnerability_labeled_dataset = datasets.load_dataset("lemon42-ai/Code_Vulnerability_Labeled_Dataset")
with open("./SESA/transformer/data/one_lemon42.jsonl","a+",encoding="utf-8") as one, open("./SESA/transformer/data/zero_lemon42.jsonl","a+",encoding="utf-8") as zero:
    for item in ds_code_vulnerability_labeled_dataset['train']:
        if("php" in item['code']):
            if(item['label'] == "safe"):
                zero_exp = {
                    "code" : item["code"],
                    "language" : "php",
                    "vulnerability_type" : item["label"],
                    "label" : 0
                }
                zeros_exp = json.dumps(zero_exp,ensure_ascii=False)
                zero.write(zeros_exp+'\n')
            else:
                one_exp = {
                    "code" : item["code"],
                    "language" : "php",
                    "vulnerability_type" : item["label"],
                    "label" : 1
                }
                ones_exp = json.dumps(one_exp,ensure_ascii=False)
                one.write(ones_exp+'\n')
