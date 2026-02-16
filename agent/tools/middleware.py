from utils.logger_handler import logger


def log_tool_call(tool_name: str, args: dict):
    logger.info(f"[Tool Call] 执行工具：{tool_name}")
    logger.info(f"[Tool Call] 传入参数：{args}")


def log_tool_result(tool_name: str, result: str):
    logger.info(f"[Tool Result] 工具 {tool_name} 调用成功")
