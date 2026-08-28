from voxel_alpha_quant.public.core.paths import get_data_dir, STAGE_CLEANED, ASSET_US_EQUITIES

def slice_context_for_llm(ticker="NVDA", keywords=None):
    """
    对清洗后的文本进行动态语义切片，提取命中关键词的段落并落盘。
    """
    if not keywords:
        print(f"ℹ️ [{ticker}] 未配置切片关键词，跳过文本切片。")
        return True

    cleaned_dir = get_data_dir(STAGE_CLEANED, ASSET_US_EQUITIES, ticker)
    input_filepath = cleaned_dir / f"{ticker.lower()}_cleaned_8k.txt"
    output_filepath = cleaned_dir / f"{ticker.lower()}_context.txt"

    if not input_filepath.exists():
        print(f"❌ 找不到清洗后文本: {input_filepath}")
        return False

    with open(input_filepath, "r", encoding="utf-8") as f:
        text = f.read()

    # 1. 按双换行符分割段落
    paragraphs = text.split('\n\n')
    keywords_lower = [k.lower() for k in keywords]
    extracted = []

    # 2. 遍历检查是否命中任意关键词
    for p in paragraphs:
        p_lower = p.lower()
        if any(kw in p_lower for kw in keywords_lower):
            extracted.append(p.replace('\n', ' ').strip())

    if not extracted:
        print(f"⚠️ [{ticker}] 未能在文本中切片到与关键词相关的段落。")
        return False

    # 3. 组装并落盘保存
    final_context = "\n\n---\n\n".join(extracted)
    with open(output_filepath, "w", encoding="utf-8") as f:
        f.write(final_context)

    print(f"✅ [{ticker}] 切片完成！提取出 {len(extracted)} 个高浓度段落 -> {output_filepath}")
    return True

if __name__ == "__main__":
    test_keywords = ["blackwell", "capacity", "ramp"]
    slice_context_for_llm("NVDA", test_keywords)