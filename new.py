import json
import random
import uuid
import numpy as np
from tqdm import tqdm

# 标签映射
attack_labels = {
    "normal": "这是一次正常的通信行为。",
    "replay": "无人机此时极大可能受到 Replay 攻击。",
    "dos": "无人机此时极大可能受到 DoS 攻击。",
    "gps": "无人机此时极大可能受到 GPS Spoofing 攻击。",
    "FDI": "无人机此时极大可能受到 FDI 攻击。"
}

# 基础字段及其范围，可根据实际数据修改
base_ranges = {
    "height": (60, 85),
    "x_speed": (-5, 5),
    "y_speed": (-5, 5),
    "z_speed": (-2, 2),
    "pitch": (-10, 10),
    "roll": (-10, 10),
    "yaw": (0, 360),
    "temperature": (60, 75),
    "distance": (60, 90),
    "barometer": (13000, 22000),
    "flight_time": (10, 70),
    "battery": (50, 100),
    "mp_distance_x": (-60, 60),
    "mp_distance_y": (-60, 60),
    "mp_distance_z": (70, 90),
}

def generate_physical_features(attack_type):
    def clip(val, field):
        min_val, max_val = base_ranges[field]
        return max(min(val, max_val), min_val)

    feature = {
        "timestamp_p": round(random.uniform(10000, 50000), 5)
    }

    # 根据攻击类型扰动特征
    for key in base_ranges:
        base_min, base_max = base_ranges[key]
        value = round(random.uniform(base_min, base_max), 2)

        # 攻击类型引入特征异常
        if attack_type == "replay":
            # 某些值保持接近但不完全一样
            value = round(np.random.normal(loc=value, scale=0.5), 2)
        elif attack_type == "dos":
            if key in ["x_speed", "y_speed", "z_speed"]:
                value = 0
        elif attack_type == "gps":
            if key in ["mp_distance_x", "mp_distance_y", "mp_distance_z"]:
                value = round(np.random.normal(loc=100, scale=20), 2)  # 假 GPS 偏移
        elif attack_type == "FDI":
            if key == "yaw":
                value = round(random.uniform(180, 360), 2)  # 异常方向
        elif attack_type == "normal":
            pass  # 正常范围

        feature[key] = clip(value, key)

    # 填充空字段
    for i in range(17, 37):
        feature[f"Unnamed: {i}"] = "nan"

    return feature

def generate_sample(id_start, attack_type, count):
    samples = []
    for i in range(count):
        sample_id = id_start + i
        feature_dict = generate_physical_features(attack_type)
        human_str = "以下是无人机物理特征：\n" + "\n".join([f"- {k}: {v}" for k, v in feature_dict.items()])
        label = attack_labels[attack_type]

        sample = {
            "id": sample_id,
            "conversations": [
                {"from": "human", "value": human_str + "\n请判断是否受到攻击并说明类型。"},
                {"from": "gpt", "value": label}
            ]
        }
        samples.append(sample)
    return samples

# 总生成数据
all_data = []
start_id = 100000

attack_types = ["normal", "replay", "dos", "gps", "FDI"]
for idx, attack in enumerate(attack_types):
    all_data.extend(generate_sample(start_id + idx * 400, attack, 400))

# 保存为 JSONL 文件
with open("generated_uav_dataset.jsonl", "w", encoding="utf-8") as f:
    for item in all_data:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print("✅ 已成功生成 2000 条样本数据（按类型划分，每类400条）")
