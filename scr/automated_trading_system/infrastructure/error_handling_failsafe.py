from infrastructure.logging_service import LoggingService

class ErrorHandler:
    def __init__(self, logging_service: LoggingService):
        self.logging_service = logging_service

    async def handle_error(self, error: Exception):
        await self.logging_service.log_error(f"Error occurred: {str(error)}")
        # Implement error handling logic, e.g., retrying operations, notifying admins, etc.

    async def handle_critical_error(self, error: Exception):
        await self.logging_service.log_error(f"Critical error occurred: {str(error)}")
        # Implement critical error handling logic, e.g., shutting down the system, notifying admins, etc.