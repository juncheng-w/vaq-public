import re
from bs4 import BeautifulSoup

# 引入强大的路径管理中枢
from voxel_alpha_quant.public.core.paths import get_data_dir, STAGE_RAW, STAGE_CLEANED, ASSET_US_EQUITIES

def clean_html_to_text(ticker="NVDA"):
    """
    读取 HTML 财报文件，剔除所有标签，并保存为纯净文本文件。
    遵循模块化与数据隔离原则，自动从 01_raw 读取并输出至 02_cleaned。
    """
    # 1. 自动定位生肉数据与清洗后数据的绝对路径
    raw_dir = get_data_dir(STAGE_RAW, ASSET_US_EQUITIES, ticker)
    cleaned_dir = get_data_dir(STAGE_CLEANED, ASSET_US_EQUITIES, ticker)
    
    # 拼装输入与输出的完整文件路径
    input_filepath = raw_dir / f"{ticker.lower()}_raw_8k.html"
    output_filepath = cleaned_dir / f"{ticker.lower()}_cleaned_8k.txt"
    
    print(f"开始处理生肉数据: {input_filepath}")
    
    if not input_filepath.exists():
        print(f"❌ 错误: 找不到文件 {input_filepath}，请确认是否已成功抓取并落盘。")
        return False

    try:
        # 2. 读取 HTML 源码
        with open(input_filepath, "r", encoding="utf-8") as f:
            raw_html = f.read()
            
        # 3. 使用 BeautifulSoup 解析 HTML (提取纯文本)
        soup = BeautifulSoup(raw_html, 'html.parser')
        pure_text = soup.get_text(separator=' ')
        
        # 4. 基础文本降噪 (正则清洗)
        pure_text = re.sub(r'[ \t]+', ' ', pure_text)
        pure_text = re.sub(r'\n\s*\n', '\n\n', pure_text)
        pure_text = pure_text.strip()
        
        # 5. 落盘保存为中间态文件 (贯彻高模块化思想)
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write(pure_text)
            
        print(f"✅ 清洗完成！提取出纯文本长度: {len(pure_text)} 字符")
        print(f"📁 已将纯净文本规范化保存至: {output_filepath}")
        return True
        
    except Exception as e:
        print(f"清洗过程中发生异常: {e}")
        return False

if __name__ == "__main__":
    clean_html_to_text("NVDA")