import asyncio
from config.config_manager import ConfigManager
from infrastructure.di_container import DIContainer
from infrastructure.plugin_loader import PluginLoader
from web.web_server import WebServer
from business_logic.trading_engine import TradingEngine

class TradingSystem:
    def __init__(self):
        self.config_manager = ConfigManager()
        self.di_container = DIContainer()
        self.plugin_loader = PluginLoader("plugins")

    async def initialize(self):
        await self.config_manager.load()
        self.di_container.config.from_dict(self.config_manager.config)
        self.di_container.wire(modules=[__name__])
        await self.plugin_loader.load_plugins()

        self.web_server = self.di_container.resolve(WebServer)
        self.trading_engine = self.di_container.resolve(TradingEngine)

        await self.web_server.initialize()
        await self.trading_engine.initialize()

    async def run(self):
        await self.initialize()
        try:
            await asyncio.gather(
                self.web_server.run(),
                self.trading_engine.run()
            )
        except Exception as e:
            error_handler = self.di_container.resolve("ErrorHandler")
            await error_handler.handle_critical_error(e)
        finally:
            await self.cleanup()

    async def cleanup(self):
        await self.web_server.shutdown()
        await self.trading_engine.shutdown()

if __name__ == "__main__":
    trading_system = TradingSystem()
    asyncio.run(trading_system.run())