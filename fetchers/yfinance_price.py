import yfinance as yf
# 引入自定义的网口模块
from network_gateway import setup_global_proxy

# 1. 脚本启动后，第一时间打通网络环境
setup_global_proxy()

def get_stock_price(ticker_symbol="AAPL"):
    ticker = yf.Ticker(ticker_symbol)
    
    # 此时 yfinance 会自动读取环境变量并走代理通道
    data = ticker.history(period="1d", interval="1m")
    
    if not data.empty:
        latest_price = data['Close'].iloc[-1]
        latest_time = data.index[-1]
        return latest_price, latest_time
    else:
        return None, None

if __name__ == "__main__":
    target_ticker = "AAPL"
    price, time_obj = get_stock_price(target_ticker)
    if price:
        print(f"[{time_obj}] {target_ticker} 最新成交价: ${price:.2f}")