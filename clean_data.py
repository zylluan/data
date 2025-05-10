import json

def load_and_clean_data(input_file, output_file):
    data = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            entry = json.loads(line)
            conversations = entry['conversations']
            valid = True
            
            # 只检查 gpt 消息中的 "value" 是否包含 "nan"
            for conv in conversations:
                if conv['from'] == 'gpt' and 'value' in conv and 'nan' in conv['value']:
                    valid = False
                    break

            if valid:
                data.append(entry)

    # 将清洗后的数据保存到输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in data:
            json.dump(item, f, ensure_ascii=False)
            f.write('\n')

    print(f"Data cleaning complete. Cleaned data saved to {output_file}")

if __name__ == "__main__":
    input_file = 'last_12225.jsonl'  # 输入文件路径
    output_file = 'test.jsonl'    # 输出文件路径

    load_and_clean_data(input_file, output_file)
