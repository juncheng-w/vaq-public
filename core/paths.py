from pathlib import Path

# 定位项目根目录
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# 定义标准的处理阶段
STAGE_RAW = "01_raw"
STAGE_CLEANED = "02_cleaned"
STAGE_EXTRACTED = "03_extracted"

# 预定义资产类别常量（防止拼写错误）
ASSET_US_EQUITIES = "us_equities"
ASSET_CRYPTO = "crypto"
ASSET_COMMODITIES = "commodities"

def get_data_dir(stage: str, asset_class: str = None, ticker: str = None) -> Path:
    """
    智能路径生成器：根据处理阶段、资产类别和标的，动态生成绝对路径。
    
    :param stage: 数据所处阶段 (如 STAGE_RAW)
    :param asset_class: (可选) 资产类别 (如 ASSET_US_EQUITIES)
    :param ticker: (可选) 标的代码 (如 'NVDA')
    :return: 对应的绝对路径 (Path 对象)
    """
    # 基础路径：比如 data/01_raw/
    dir_path = DATA_DIR / stage
    
    if asset_class:
        # 如果有大类，进入大类文件夹：比如 data/01_raw/us_equities/
        dir_path = dir_path / asset_class.lower()
        
        if ticker:
            # 如果指定了具体标的，进入标的文件夹：比如 data/01_raw/us_equities/NVDA/
            dir_path = dir_path / str(ticker).upper()
            
    # 自动创建所缺失的所有父层级目录
    dir_path.mkdir(parents=True, exist_ok=True)
    
    return dir_path