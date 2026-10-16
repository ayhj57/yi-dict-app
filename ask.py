import os

import requests
from dotenv import load_dotenv

# 1. 读取 .env 里的密钥
load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")

# 2. 准备请求地址和请求头
url = "https://api.deepseek.com/chat/completions"
headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

# 3. 获取用户输入，按文档拼装请求体
user_input = input("请输入问题：")
data = {
    "model": "deepseek-flash",
    "messages": [{"role": "user", "content": user_input}],
}

# 4. 发送请求 + 异常处理
try:
    response = requests.post(url, headers=headers, json=data, timeout=10)

    if response.status_code == 401:
        print("API Key 无效，检查一下 .env")
    elif response.status_code == 402:
        print("账户余额不足")
    elif response.status_code != 200:
        print(f"请求失败，状态码：{response.status_code}")
    else:
        result = response.json()
        try:
            answer = result["choices"][0]["message"]["content"]
            print("回答：", answer)
        except (KeyError, IndexError):
            print("服务返回了意料之外的内容")

except requests.exceptions.RequestException:
    print("网络好像断了，检查一下再试试")
