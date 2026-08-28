import yaml
from pathlib import Path
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from voxel_alpha_quant.public.core.paths import PROJECT_ROOT

def load_universe_config():
    """加载静态资产池配置"""
    config_path = PROJECT_ROOT / "config" / "universe_config.yaml"
    if not config_path.exists():
        return None
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_active_strategy(ticker: str, asset_class="us_equities", target_date_str=None):
    """
    根据给定时区与日期（默认读取当前美东时间），动态加载生效的策略规则资产
    """
    strategy_dir = PROJECT_ROOT / "config" / "strategies" / asset_class / ticker.upper()
    if not strategy_dir.exists():
        print(f"⚠️ 未找到标的 [{ticker}] 的策略目录: {strategy_dir}")
        return None

    # 计算目标比对日期（默认为美东当前日期）
    if not target_date_str:
        ny_time = datetime.now(timezone.utc).astimezone(ZoneInfo("America/New_York"))
        target_date = ny_time.date()
    else:
        target_date = datetime.strptime(target_date_str, "%Y-%m-%d").date()

    for file_path in strategy_dir.glob("*.yaml"):
        with open(file_path, "r", encoding="utf-8") as f:
            strategy_data = yaml.safe_load(f)
            
        valid_from = datetime.strptime(strategy_data.get("valid_from", "1970-01-01"), "%Y-%m-%d").date()
        valid_to = datetime.strptime(strategy_data.get("valid_to", "2099-12-31"), "%Y-%m-%d").date()

        if valid_from <= target_date <= valid_to:
            print(f"🎯 [{ticker}] 成功命中生效策略资产: {file_path.name} (目标日期: {target_date})")
            return strategy_data

    print(f"⚠️ [{ticker}] 在日期 {target_date} 下没有匹配到任何有效策略规则。")
    return None