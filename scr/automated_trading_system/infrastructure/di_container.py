from dependency_injector import containers, providers
from config.config_manager import ConfigManager
from infrastructure.logging_service import LoggingService
from infrastructure.error_handling_failsafe import ErrorHandler
from ai_analysis.data_preparation import DataPreparation
from ai_analysis.ai_recommendation_system import AIRecommendationSystem
from ai_analysis.ai_performance_tracker import AIPerformanceTracker
from ai_analysis.main_ai_analysis import MainAIAnalysis
from decision_making.decision_engine import DecisionEngine
from order_execution.smart_order_router import SmartOrderRouter
from business_logic.trading_engine import TradingEngine
from analysis.main_analysis import MainAnalysis
from web.web_server import WebServer

# Infrastructure/DI Container
class DIContainer(containers.DeclarativeContainer):
    config = providers.Singleton(ConfigManager)
    logging_service = providers.Singleton(LoggingService, config)
    data_preparation = providers.Singleton(DataPreparation, config)
    ai_recommendation_system = providers.Singleton(AIRecommendationSystem, config)
    ai_performance_tracker = providers.Singleton(AIPerformanceTracker, config)
    
    # Main AI Analysis with all required dependencies
    main_ai_analysis = providers.Singleton(
        MainAIAnalysis,
        config=config,
        logging_service=logging_service,
        data_preparation=data_preparation,
        recommendation_system=ai_recommendation_system,
        performance_tracker=ai_performance_tracker
    )
    
    error_handler = providers.Singleton(ErrorHandler, logging_service)

    decision_engine = providers.Singleton(DecisionEngine, config)
    smart_order_router = providers.Singleton(SmartOrderRouter, config)

    # Trading Engine with all required dependencies
    trading_engine = providers.Singleton(
        TradingEngine,
        config=config,
        logging_service=logging_service,
        main_ai_analysis=main_ai_analysis,
        decision_engine=decision_engine,
        smart_order_router=smart_order_router
    )

    web_server = providers.Singleton(WebServer, config, trading_engine)
