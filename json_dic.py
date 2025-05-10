import json

with open("/home/ubuntu/data/merge_lora.json", "r") as f:
    data_list = json.load(f)

# 将列表转换为以 index 为 key 的字典
data_dict = {f"dataset_{i}": item for i, item in enumerate(data_list)}

with open("/home/ubuntu/data/merge_lora_fixed.json", "w") as f:
    json.dump(data_dict, f, indent=4)
