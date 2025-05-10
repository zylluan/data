import json
from collections import deque

def get_last_n_lines(file_path, n):
    # 使用 deque 保留最后 n 行数据
    last_n_lines = deque(maxlen=n)
    
    with open(file_path, 'r', encoding='utf-8') as file:  # 指定文件编码为 utf-8
        for line in file:
            last_n_lines.append(json.loads(line))  # 逐行读取并解析成 JSON
    
    return list(last_n_lines)

def save_to_new_jsonl(last_n_data, new_file_path):
    with open(new_file_path, 'w', encoding='utf-8') as file:  # 指定文件编码为 utf-8
        for data in last_n_data:
            json.dump(data, file, ensure_ascii=False)  # 保持原始字符，不转义
            file.write('\n')  # 每条数据后换行

# 示例调用
file_path = 'merge_lora.jsonl'  # 请替换成你的源文件路径
new_file_path = 'last_12225.jsonl'  # 请替换成你想保存的新文件路径

# 获取后 12225 条数据
last_12225_lines = get_last_n_lines(file_path, 12225)

# 将数据保存到新的 .jsonl 文件
save_to_new_jsonl(last_12225_lines, new_file_path)

print(f"后 12225 条数据已保存到 {new_file_path}")
