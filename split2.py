import json
import random

input_file = "test.jsonl"
output_file1 = "test_1.jsonl"
output_file2 = "test_2.jsonl"

# 1. 读取 jsonl 文件
with open(input_file, 'r', encoding='utf-8') as f:
    lines = [json.loads(line) for line in f]

# 2. 打乱顺序
random.shuffle(lines)

# 3. 对半分
mid = len(lines) // 2
part1 = lines[:mid]
part2 = lines[mid:]

# 4. 写入 part1
with open(output_file1, 'w', encoding='utf-8') as f:
    for item in part1:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')

# 5. 写入 part2
with open(output_file2, 'w', encoding='utf-8') as f:
    for item in part2:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')
