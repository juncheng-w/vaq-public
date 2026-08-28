import ccxt
# 引入自定义的网口模块
from network_gateway import get_ccxt_proxy_config

def get_crypto_price(symbol="BTC/USDT"):
    # 使用网口模块提供的标准代理配置
    exchange = ccxt.binance({
        'enableRateLimit': True,
        'proxies': get_ccxt_proxy_config(), 
        'timeout': 5000,
    })
    
    ticker = exchange.fetch_ticker(symbol)
    return ticker['last'], ticker['datetime']

if __name__ == "__main__":
    target_symbol = "BTC/USDT"
    price, time_str = get_crypto_price(target_symbol)
    print(f"[{time_str}] {target_symbol} 当前价格: ${price:,.2f}")