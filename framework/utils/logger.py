import sys
from pathlib import Path
from loguru import logger
from framework.utils.config_loader import ConfigLoader
from framework.core.context.execution_context import ExecutionContext


class LoggerManager:
    """
    Centralized logger manager.

    Responsibilities:
    - Configure console logging
    - Configure file logging
    - Standardize log format
    - Provide reusable logger instance
    """

    _configured = False

    @classmethod
    def setup_logger(cls):
        """
        Configure logger only once.
        """

        if cls._configured:
            return logger

        config = ConfigLoader.load_config()

        log_level = config.get("log_level", "INFO")

     #   project_root = Path(__file__).resolve().parents[2]

        log_directory = ExecutionContext.get_logs_dir()
        log_directory.mkdir(parents=True, exist_ok=True)

        worker_id = ExecutionContext.get_worker_id()
        log_file = log_directory / f"framework_{worker_id}.log"

        logger.remove()

        # Console logging
        logger.add(
            sys.stdout,
            level=log_level,
            format=(
                "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                "<level>{level: <8}</level> | "
                "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
                "<level>{message}</level>"
            ),
            colorize=True
        )

        # File logging
        logger.add(
            log_file,
            level=log_level,
            rotation="10 MB",
            retention="10 days",
            compression="zip",
            enqueue=True,
            backtrace=True,
            diagnose=True,
            format=(
                "{time:YYYY-MM-DD HH:mm:ss} | "
                "{level: <8} | "
                "{name}:{function}:{line} | "
                "{message}"
            )
        )

        cls._configured = True

        logger.info("Logger initialized successfully")

        return logger

    @classmethod
    def get_logger(cls):
        """
        Return configured logger instance.
        """

        if not cls._configured:
            cls.setup_logger()

        return logger