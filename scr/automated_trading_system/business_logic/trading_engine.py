import asyncio
from typing import Dict, Any, List
from infrastructure.logging_service import LoggingService
from analysis.main_analysis import MainAnalysis
from analysis.post_trade_analysis import PostTradeAnalysis
from ai_analysis.main_ai_analysis import MainAIAnalysis
from decision_making.decision_engine import DecisionEngine
from order_execution.smart_order_router import SmartOrderRouter
from data.stock_data_manager import StockDataManager
from data.stock_watchlist import StockWatchlist
from data.enhanced_vector_database import EnhancedVectorDatabase
from repositories.config_repository import ConfigRepository
from business_logic.trading_strategy_interface import TradingStrategy, CombinedStrategy
from infrastructure.messaging import MessageBroker
from decision_making.risk_management import RiskManagement
from ai_analysis.ai_performance_tracker import PerformanceTracker

class TradingEngine:
    def __init__(self, config_repository: ConfigRepository, logging_service: LoggingService, 
                 main_analysis: MainAnalysis, main_ai_analysis: MainAIAnalysis, 
                 decision_engine: DecisionEngine, smart_order_router: SmartOrderRouter, 
                 stock_data_manager: StockDataManager, stock_watchlist: StockWatchlist,
                 vector_database: EnhancedVectorDatabase, strategies: List[TradingStrategy], 
                 message_broker: MessageBroker, risk_management: RiskManagement,
                 performance_tracker: PerformanceTracker, post_trade_analysis: PostTradeAnalysis):
        self.config_repository = config_repository
        self.logging_service = logging_service
        self.main_analysis = main_analysis
        self.main_ai_analysis = main_ai_analysis
        self.decision_engine = decision_engine
        self.smart_order_router = smart_order_router
        self.stock_data_manager = stock_data_manager
        self.stock_watchlist = stock_watchlist
        self.vector_database = vector_database
        self.strategy = CombinedStrategy(strategies)
        self.message_broker = message_broker
        self.risk_management = risk_management
        self.performance_tracker = performance_tracker
        self.post_trade_analysis = post_trade_analysis
        self.config = {}
        self.is_running = False

    async def initialize(self):
        try:
            await self.config_repository.initialize()
            self.config = await self.config_repository.get_system_settings()
            await self.main_analysis.initialize()
            await self.main_ai_analysis.initialize()
            decision_engine_config = await self.config_repository.get_decision_engine_config()
            await self.decision_engine.initialize(decision_engine_config)
            await self.smart_order_router.initialize()
            await self.stock_data_manager.initialize()
            await self.stock_watchlist.initialize()
            await self.vector_database.initialize()
            await self.message_broker.connect()
            await self.logging_service.log_info("Trading Engine initialized successfully")
        except Exception as e:
            await self.logging_service.log_error(f"Error initializing Trading Engine: {str(e)}")
            raise

    async def run(self):
        self.is_running = True
        while self.is_running:
            try:
                await self.trading_cycle()
            except Exception as e:
                await self.logging_service.log_error(f"Error in trading cycle: {str(e)}")
            await asyncio.sleep(self.config.get('trading_interval', 60))

    async def trading_cycle(self):
        try:
            active_stocks = self.stock_watchlist.get_active_stocks()
            
            for symbol in active_stocks:
                await self.process_stock(symbol)

            await self.post_cycle_tasks()
        except Exception as e:
            await self.logging_service.log_error(f"Error in trading cycle: {str(e)}")

    async def process_stock(self, symbol: str):
        try:
            market_data = await self.stock_data_manager.get_stock_data(symbol)
            news_data = await self.stock_data_manager.get_news_data(symbol)
            
            analysis_results = await self.main_analysis.analyze(market_data, news_data)
            analysis_summary = await self.main_analysis.get_analysis_summary(analysis_results)
            
            ai_analysis_results = await self.main_ai_analysis.analyze(market_data, news_data, analysis_results)
            
            combined_data = {
                'symbol': symbol,
                'market_data': market_data,
                'news_data': news_data,
                'analysis_results': analysis_results,
                'analysis_summary': analysis_summary,
                'ai_analysis_results': ai_analysis_results
            }

            decision = await self.decision_engine.make_decision(combined_data)
            risk_adjusted_decision = await self.risk_management.apply_risk_limits(decision, analysis_summary['risk_level'])

            if risk_adjusted_decision['action'] != 'HOLD':
                order_result = await self.smart_order_router.route_order(risk_adjusted_decision)
                await self.logging_service.log_info(f"Order executed for {symbol}: {order_result}")

                await self.performance_tracker.track_performance(symbol, risk_adjusted_decision, order_result)
                
                # Store vector with versioning
                vector_metadata = {
                    'symbol': symbol,
                    'timestamp': market_data['timestamp'][-1],
                    'action': risk_adjusted_decision['action'],
                    'outcome': order_result['outcome']
                }
                await self.vector_database.store_vector(analysis_results['vector'], vector_metadata)

                await self.message_broker.publish('trade_executed', {
                    'symbol': symbol,
                    'action': risk_adjusted_decision['action'],
                    'result': order_result,
                    'analysis_summary': analysis_summary
                })

                await self.perform_post_trade_analysis(combined_data, order_result)

        except Exception as e:
            await self.logging_service.log_error(f"Error processing stock {symbol}: {str(e)}")

    async def perform_post_trade_analysis(self, trade_data: Dict[str, Any], order_result: Dict[str, Any]):
        try:
            post_trade_results = await self.post_trade_analysis.analyze(trade_data, order_result['outcome'])
            
            await self.main_analysis.update_with_post_trade_analysis(post_trade_results)
            await self.main_ai_analysis.track_performance(trade_data, post_trade_results)
            await self.decision_engine.update_with_post_trade_analysis(post_trade_results)
            
            await self.vector_database.update_metadata(trade_data['symbol'], post_trade_results)
            
            await self.message_broker.publish('post_trade_analysis', {
                'symbol': trade_data['symbol'],
                'results': post_trade_results
            })
            
        except Exception as e:
            await self.logging_service.log_error(f"Error in post-trade analysis: {str(e)}")

    async def post_cycle_tasks(self):
        try:
            performance_report = await self.performance_tracker.generate_performance_report()
            await self.message_broker.publish('performance_update', performance_report)

            risk_assessment = await self.risk_management.assess_portfolio_risk()
            await self.message_broker.publish('risk_assessment', risk_assessment)

            market_overview = await self.stock_data_manager.get_market_overview()
            insights = await self.main_ai_analysis.generate_trading_insights(market_overview)
            await self.message_broker.publish('market_insights', insights)

            # Create database snapshot
            snapshot_name = f"snapshot_{int(time.time())}"
            await self.vector_database.create_snapshot(snapshot_name)

        except Exception as e:
            await self.logging_service.log_error(f"Error in post-cycle tasks: {str(e)}")

    async def shutdown(self):
        await self.logging_service.log_info("Trading engine shutting down...")
        self.is_running = False
        await self.stock_data_manager.close()
        await self.vector_database.close()
        await self.message_broker.close()
        await self.logging_service.log_info("Trading engine shut down successfully")