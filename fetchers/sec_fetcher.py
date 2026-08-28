import os
import requests
import time
from dotenv import load_dotenv

# 【改造点 1】引入路径管理器，并增加资产大类 ASSET_US_EQUITIES
from voxel_alpha_quant.public.core.paths import get_data_dir, STAGE_RAW, ASSET_US_EQUITIES
# 【改造点 2】修复网络网口的绝对路径引用
from voxel_alpha_quant.public.core.network_gateway import setup_global_proxy

# 1. 激活网络与环境变量
setup_global_proxy()
load_dotenv()

# 2. 从 .env 安全读取
SEC_USER_AGENT = os.getenv("SEC_USER_AGENT", "VoxelAlphaBot/1.0 (admin@example.com)")

SEC_HEADERS = {
    "User-Agent": SEC_USER_AGENT,
    "Accept-Encoding": "gzip, deflate",
}

# 【改造点 3】增加 ticker 参数，方便后续向下载函数传递标的名
def fetch_latest_earnings_release(ticker="NVDA", cik="0001045810"):
    """
    抓取指定公司最新的 8-K 财报新闻稿 (精准过滤 Item 2.02 财报)
    """
    print(f"开始抓取 [{ticker}] (CIK: {cik}) 的最新财报目录...")
    cik_padded = str(cik).zfill(10)
    submissions_url = f"https://data.sec.gov/submissions/CIK{cik_padded}.json"
    
    headers = SEC_HEADERS.copy()
    headers["Host"] = "data.sec.gov"
    
    try:
        response = requests.get(submissions_url, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        recent = data['filings']['recent']
        
        # 遍历归档，寻找最近的 8-K
        for i, form in enumerate(recent['form']):
            if form == "8-K":
                items = recent.get('items', [])[i]
                if "2.02" not in items:
                    print(f"跳过非财报 8-K (归档号: {recent['accessionNumber'][i]}, Item: {items})")
                    continue
                    
                accession_number = recent['accessionNumber'][i]
                report_date = recent['reportDate'][i]
                acc_no_raw = accession_number.replace("-", "")
                
                print(f"✅ 找到最新财报 8-K！归档号: {accession_number} (发布日期: {report_date})")
                
                folder_url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc_no_raw}/"
                index_json_url = f"{folder_url}index.json"
                
                headers_sec = SEC_HEADERS.copy()
                headers_sec["Host"] = "www.sec.gov"
                
                time.sleep(0.3)
                idx_res = requests.get(index_json_url, headers=headers_sec, timeout=15)
                
                target_doc_name = None
                primary_doc = recent['primaryDocument'][i].lower()
                
                if idx_res.status_code == 200:
                    directory_items = idx_res.json().get("directory", {}).get("item", [])
                    
                    html_attachments = [
                        item['name'] for item in directory_items 
                        if item['name'].lower().endswith(('.htm', '.html')) 
                        and item['name'].lower() != primary_doc
                    ]
                    
                    for name in html_attachments:
                        name_lower = name.lower()
                        if "pr" in name_lower or "commentary" in name_lower or "99" in name_lower:
                            target_doc_name = name
                            print(f"🎯 成功锁定财报核心附件: {target_doc_name}")
                            if "pr" in name_lower:
                                break
                                
                    if not target_doc_name and html_attachments:
                        target_doc_name = html_attachments[0]
                        print(f"⚠️ 未找到特征词，尝试抓取第一个 HTML 附件: {target_doc_name}")
                
                if not target_doc_name:
                    target_doc_name = recent['primaryDocument'][i]
                    print(f"⚠️ 未检测到任何有效网页版附件，回退下载主文件: {target_doc_name}")
                
                final_download_url = f"{folder_url}{target_doc_name}"
                # 将 ticker 传递给下载函数
                return download_file(final_download_url, ticker)
                
        print("未找到近期的财报 8-K 文件。")
        return None

    except Exception as e:
        print(f"抓取异常: {e}")
        return None

# 【改造点 4】接收 ticker 参数并执行智能落盘
def download_file(url, ticker):
    print(f"正在下载财报核心内容: {url}")
    headers_sec = SEC_HEADERS.copy()
    headers_sec["Host"] = "www.sec.gov"
    
    try:
        time.sleep(0.5)
        res = requests.get(url, headers=headers_sec, timeout=20)
        res.raise_for_status()
        
        # --- 核心数据落盘逻辑升级 ---
        # 自动获取形如: C:\Quant\data\01_raw\us_equities\NVDA 的绝对路径
        target_dir = get_data_dir(STAGE_RAW, ASSET_US_EQUITIES, ticker)
        
        # 拼装最终文件路径
        file_path = target_dir / f"{ticker.lower()}_raw_8k.html"
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(res.text)
            
        print(f"✅ 下载完毕！文本长度: {len(res.text)} 字符\n📁 已规范化保存至: {file_path}")
        return res.text
        
    except Exception as e:
        print(f"下载失败: {e}")
        return None

if __name__ == "__main__":
    fetch_latest_earnings_release("NVDA", "0001045810")