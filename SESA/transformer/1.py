# from transformers import AutoModelForCausalLM, AutoTokenizer
# from peft import PeftModel

# # Load base model
# base_model = "deepseek-ai/deepseek-coder-1.3b-instruct"
# model = AutoModelForCausalLM.from_pretrained(base_model, device_map="auto",mirror="tuna")
# tokenizer = AutoTokenizer.from_pretrained(base_model)

# # Load LoRA adapter
# model = PeftModel.from_pretrained(model, "elsiddik/pentest-vulnerability-detector")

# # Analyze code
# code = "SELECT * FROM users WHERE id = 'user_input'"
# prompt = f"System: You are a security expert.\n\nUser: Analyze this code:\n{code}\n\nAssistant:"

# inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
# outputs = model.generate(**inputs, max_new_tokens=200)
# response = tokenizer.decode(outputs[0], skip_special_tokens=True)
# print(response)

from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch

# Load base model - 老王的正确写法
base_model = "deepseek-ai/deepseek-coder-1.3b-instruct"
model = AutoModelForCausalLM.from_pretrained(
    base_model,
    device_map="auto",
    torch_dtype="auto",  # 关键：自动选择数据类型
    low_cpu_mem_usage=True,  # 关键：避免meta device
    trust_remote_code=True,
    mirror="tuna"
)
tokenizer = AutoTokenizer.from_pretrained(base_model)

# Load LoRA adapter
model = PeftModel.from_pretrained(model, "elsiddik/pentest-vulnerability-detector")

# Analyze code
code = "SELECT * FROM users WHERE id = 'user_input'"
prompt = f"System: You are a security expert.\n\nUser: Analyze this code:\n{code}\n\nAssistant:"

inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=200)
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(response)