from tenacity import retry, stop_after_attempt, wait_exponential
from utils.logger import logger


def retry_on_error(max_attempts=3):
    """重试装饰器"""
    return retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        before=lambda retry_state: logger.info(f"尝试第 {retry_state.attempt_number} 次"),
        after=lambda retry_state: logger.warning(f"重试后成功")
    )