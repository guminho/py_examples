import torch
from transformers import pipeline

pipeline = pipeline(
    task="text-generation",
    model="Qwen/Qwen2.5-1.5B-Instruct",
    dtype=torch.bfloat16,
    device_map="auto",
)

chat = [
    {"role": "system", "content": "You are Hermione"},
    {"role": "user", "content": "Who is Dumbledore?"},
]
response = pipeline(chat, max_new_tokens=512)
print(response[0]["generated_text"][-1]["content"])
