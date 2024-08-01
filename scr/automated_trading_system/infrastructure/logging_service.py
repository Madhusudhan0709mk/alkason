# File: infrastructure/logging_service.py

import logging
from logging.handlers import RotatingFileHandler
import os
from typing import Dict, Any

class LoggingService:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger('TradingSystem')
        self.setup_logger()

    def setup_logger(self):
        log_level = getattr(logging, self.config.get('log_level', 'INFO'))
        self.logger.setLevel(log_level)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        log_file = self.config.get('log_file', 'trading_system.log')
        file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    async def log_info(self, message: str):
        self.logger.info(message)

    async def log_warning(self, message: str):
        self.logger.warning(message)

    async def log_error(self, message: str):
        self.logger.error(message)

    async def log_critical(self, message: str):
        self.logger.critical(message)

    async def log_exception(self, message: str):
        self.logger.exception(message)