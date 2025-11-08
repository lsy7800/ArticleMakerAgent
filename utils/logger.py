from loguru import logger
import sys

logger.remove()     # 移除默认配置
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | {message}",
    level="INFO")

# 输出文件
logger.add(
    "../logs/spider_{time:YYYY-MM-DD}.log",
    rotation="00:00",   # 每天轮转
    retention="7 days",     # 保留7天
    level="DEBUG",
)

