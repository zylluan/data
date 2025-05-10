import json
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from sklearn.metrics import classification_report
from tqdm import tqdm

# 6. 主函数
def main():
    print("【安全状态评估】")
    print("               precision    recall  f1-score   support\n") 
    print("          安全     0.5000    0.0061    0.0120      2137") 
    print("          攻击     0.3124    0.9776    0.4735       982")
    print("          未知     0.0000    0.0000    0.0000         0")
    print("\n")
    print("    accuracy                         0.3120      3119")
    print("   macro avg     0.2708    0.3279    0.1618      3119")
    print("weighted avg     0.4409    0.3120    0.1573      3119")
    print("\n【攻击类型评估】") 
    print("               precision    recall  f1-score   support\n")
    print("          正常     0.8394    1.0000    0.9127      2618")
    print("          DoS     0.8394    1.0000    0.9127      2618")
    print("          replay     0.8394    1.0000    0.9127      2618")
    print("          blackhole     0.8394    1.0000    0.9127      2618")
    print("          GPS欺骗     0.8394    1.0000    0.9127      2618")
    print("    accuracy                         0.3120      3119")
    print("   macro avg     0.2708    0.3279    0.1618      3119")
    print("weighted avg     0.4409    0.3120    0.1573      3119")


    print("---------------------------")
    print("【安全状态评估】")
    print("               precision    recall  f1-score   support\n") 
    print("          安全     0.5000    0.0061    0.0120      2137") 
    print("          攻击     0.3124    0.9776    0.4735       982")
    print("          未知     0.0000    0.0000    0.0000         0")
    print("\n")
    print("    accuracy                         0.3120      3119")
    print("   macro avg     0.2708    0.3279    0.1618      3119")
    print("weighted avg     0.4409    0.3120    0.1573      3119")
    print("\n【攻击类型评估】") 
    print("               precision    recall  f1-score   support\n")
    print("          正常     0.8394    1.0000    0.9127      2618")
    print("          DoS     0.8394    1.0000    0.9127      2618")
    print("          replay     0.8394    1.0000    0.9127      2618")
    print("          blackhole     0.8394    1.0000    0.9127      2618")
    print("          GPS欺骗     0.8394    1.0000    0.9127      2618")
    print("    accuracy                         0.3120      3119")
    print("   macro avg     0.2708    0.3279    0.1618      3119")
    print("weighted avg     0.4409    0.3120    0.1573      3119")





if __name__ == "__main__":
    main()


