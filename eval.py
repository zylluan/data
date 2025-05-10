import json
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from sklearn.metrics import classification_report
from tqdm import tqdm

# 1. 状态与攻击类型关键词，用于提取标签
status_keywords = {
    "安全": ["安全", "正常", "无异常", "未检测到攻击"],
    "攻击": ["攻击", "欺骗", "干扰", "异常", "入侵"]
}

attack_type_keywords = {
    "GPS欺骗": ["GPS欺骗", "GPS干扰", "定位伪造", "GPS Spoofing"],
    "DOS攻击": ["DoS", "拒绝服务", "流量攻击", "资源耗尽"],
    "MITM攻击": ["中间人", "MITM", "通信篡改", "监听数据"],
    "电磁干扰": ["电磁", "磁电"],
    "重放攻击": ["replay", "Replay", "RePlay"],
    "FDI": ["Fdi", "FDI"],
    "evil_twin": ["恶意双胞胎", "黑洞","evil_twin","Evil_twin"],
    "未知攻击": ["未知攻击", "异常行为", "不明模式"]
}

# 2. 标签提取函数
def extract_label(text, keywords_dict):
    for label, keywords in keywords_dict.items():
        for kw in keywords:
            if kw in text:
                return label
    return "未知"

# 3. 加载验证集
def load_validation_data(path):
    samples = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            item = json.loads(line)  # 每行是一个独立的 JSON 对象
            sample_id = item["id"]
            convs = item["conversations"]
            prompt = convs[0]["value"]
            reference = convs[1]["value"]
            samples.append({
                "id": sample_id,
                "prompt": prompt,
                "reference": reference
            })
    return samples


# 4. 模型预测函数
@torch.no_grad()
def generate_predictions_mul(samples, model, tokenizer, max_new_tokens=1024):
    predictions = []
    model.eval()
    device = model.device
    for sample in tqdm(samples, desc="Generating predictions"):
        inputs = tokenizer(sample["prompt"], return_tensors="pt").to(device)
        output_ids = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id
        )
        output_text = tokenizer.decode(output_ids[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True)
        predictions.append({
            "id": sample["id"],
            "prompt": sample["prompt"],
            "reference": sample["reference"],
            "prediction": output_text.strip()
        })
    return predictions

# 4. 模型预测函数
@torch.no_grad()
def generate_predictions(samples, model, tokenizer, max_new_tokens_max=1024):
    predictions = []
    model.eval()
    device = model.device
    generation_config = dict(max_new_tokens=1024, do_sample=False)
    for sample in tqdm(samples, desc="Generating predictions"):
        # 构建聊天消息格式
# 确保 prompt 是字符串类型
        pp = "你作为一个无人机的大脑。分析无人机是否存在异常，哪里异常，然后给出分析结果，如果存在攻击则判断可能是哪种攻击类型，并分析受攻击的严重程度。接下来是无人机的一些数据："
        #system_msg = {"role": "system", "content": pp}
        messages = pp+sample["prompt"]

        
        # 使用 chat 接口进行生成
        response = model.chat(
            tokenizer, 
            None,
            messages,
            generation_config, 
            history=None, 
            return_history=False
        )
        
        #output_text = response['choices'][0]['message']['content'].strip()
        print(str(sample["id"])+ "Internvl————" + response+"\n")
        
        predictions.append({
            "id": sample["id"],
            "prompt": sample["prompt"],
            "reference": sample["reference"],
            "prediction": response
        })
    return predictions

# 5. 评估指标
def evaluate(predictions):
    y_status_true, y_status_pred = [], []
    y_attack_true, y_attack_pred = [], []

    for item in predictions:
        ref = item["reference"]
        pred = item["prediction"]

        y_status_true.append(extract_label(ref, status_keywords))
        y_status_pred.append(extract_label(pred, status_keywords))

        y_attack_true.append(extract_label(ref, attack_type_keywords))
        y_attack_pred.append(extract_label(pred, attack_type_keywords))

    print("【安全状态评估】")
    print(classification_report(y_status_true, y_status_pred, digits=4))

    print("\n【攻击类型评估】")
    print(classification_report(y_attack_true, y_attack_pred, digits=4))


# 6. 主函数
def main():
    # 模型路径
    model_path = "/home/ubuntu//InternVL/internvl_chat/InternVL2-2B-8/lora_merge"  # 替换为你的LoRA模型路径
    val_path = "/home/ubuntu/data/ge_uav_test.jsonl"                # 替换为验证集路径

    # 加载 tokenizer 和模型
    tokenizer = AutoTokenizer.from_pretrained(
        model_path, 
        trust_remote_code=True, 
        local_files_only=True
    )
    model = AutoModelForCausalLM.from_pretrained(
        model_path, 
        trust_remote_code=True, 
        device_map="auto", 
        local_files_only=True,
        torch_dtype=torch.float32, 
        use_flash_attn=False
    )

    # 加载验证集
    samples = load_validation_data(val_path)

    # 生成预测
    predictions = generate_predictions(samples, model, tokenizer)

    # 保存预测
    with open("ft_predictions.jsonl", "w", encoding="utf-8") as f:
        for item in predictions:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    # 评估
    evaluate(predictions)

if __name__ == "__main__":
    main()





