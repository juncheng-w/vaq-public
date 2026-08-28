import os
import requests
from dotenv import load_dotenv
from voxel_alpha_quant.public.core.network_gateway import setup_global_proxy

# 激活环境变量与全局网络网关
load_dotenv()
setup_global_proxy()

SERVERCHAN_SENDKEY = os.getenv("SERVERCHAN_SENDKEY")

def send_wechat_notification(title: str, markdown_content: str) -> bool:
    """
    通过 Server酱 将 Markdown 格式的报告推送到微信
    """
    if not SERVERCHAN_SENDKEY or SERVERCHAN_SENDKEY.strip() == "" or "YOUR_" in SERVERCHAN_SENDKEY:
        print("\n⚠️ 未在 .env 中检测到有效的 SERVERCHAN_SENDKEY，跳过微信推送（仅终端输出）：")
        print("--------------------------------------------------")
        print(f"【标题】: {title}\n")
        print(markdown_content)
        print("--------------------------------------------------")
        return False

    url = f"https://sctapi.ftqq.com/{SERVERCHAN_SENDKEY}.send"
    payload = {
        "title": title,
        "desp": markdown_content
    }

    try:
        response = requests.post(url, data=payload, timeout=10)
        res_json = response.json()
        
        if response.status_code == 200 and res_json.get("code") == 0:
            print(f"📱 [微信推送] 成功推送到微信！标题: {title}")
            return True
        else:
            print(f"❌ [微信推送失败] Server酱响应: {res_json.get('message', response.text)}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ [微信推送异常] 网络请求失败: {e}")
        return False

if __name__ == "__main__":
    # 独立连通性测试
    test_title = "Voxel_Alpha_Quant 通信测试"
    test_content = """### 🚀 基础设施就绪
* **状态**: 微信通知网关接入成功
* **环境**: 本地量化中枢正常运行
"""
    send_wechat_notification(test_title, test_content)