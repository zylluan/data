import json

# 打开 jsonl 文件和输出 json 文件
with open('merge_lora.jsonl', 'r') as jsonl_file, open('merge_lora.json', 'w') as json_file:
    # 将每行的 JSON 数据读入列表
    json_list = [json.loads(line) for line in jsonl_file]
    
    # 将列表写入到 output_file.json 中，保存为 JSON 格式
    json.dump(json_list, json_file, indent=4)
