import os

# 在这里统一配置你的代理地址
PROXY_URL = "http://127.0.0.1:7897"  # 请确保端口号与你实际使用的一致

def setup_global_proxy():
    """
    配置全局代理环境变量。
    运行此函数后，yfinance, requests 等大部分标准网络库会自动通过此网口路由。
    """
    os.environ['HTTP_PROXY'] = PROXY_URL
    os.environ['HTTPS_PROXY'] = PROXY_URL
    os.environ['http_proxy'] = PROXY_URL   # 兼容小写格式
    os.environ['https_proxy'] = PROXY_URL
    print(f"[Network] 全局网络网口已接入，代理出口: {PROXY_URL}")

def get_ccxt_proxy_config():
    """
    返回字典格式的代理配置。
    专供 CCXT 等需要显式传入代理参数的库使用。
    """
    return {
        'http': PROXY_URL,
        'https': PROXY_URL
    }