# Load model directly
from transformers import AutoTokenizer, AutoModelForSequenceClassification

tokenizer = AutoTokenizer.from_pretrained("CIRCL/cwe-parent-vulnerability-classification-microsoft-codebert-base")
model = AutoModelForSequenceClassification.from_pretrained("CIRCL/cwe-parent-vulnerability-classification-microsoft-codebert-base")

print(model)