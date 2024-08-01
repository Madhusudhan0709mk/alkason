# File: ai_analysis/ai_provider_factory.py

from typing import Dict, Any
from abc import ABC, abstractmethod
from langchain.llms import AzureOpenAI
from langchain.chat_models import ChatAnthropic
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

class AIProvider(ABC):
    @abstractmethod
    async def generate_recommendation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pass

class AzureOpenAIProvider(AIProvider):
    def __init__(self, config: Dict[str, Any]):
        self.llm = AzureOpenAI(
            deployment_name=config["deployment_name"],
            model_name=config["model_name"],
            openai_api_base=config["api_base"],
            openai_api_version=config["api_version"],
            openai_api_key=config["api_key"],
        )
        self.chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate(
                input_variables=["market_data", "technical_indicators", "sentiment_score", "intermarket_data"],
                template="""Analyze the following market data and provide a trading recommendation:
                Market Data: {market_data}
                Technical Indicators: {technical_indicators}
                Sentiment Score: {sentiment_score}
                Intermarket Data: {intermarket_data}

                Please provide a recommendation in the following format:
                Action: [BUY/SELL/HOLD]
                Confidence: [0-1]
                Reasoning: [Your analysis and reasoning]
                Target Price: [Suggested target price]
                Stop Loss: [Suggested stop loss price]
                """
            )
        )

    async def generate_recommendation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        response = await self.chain.arun(
            market_data=str(data['market_data']),
            technical_indicators=str(data['technical_indicators']),
            sentiment_score=str(data['sentiment_score']),
            intermarket_data=str(data['intermarket_data'])
        )
        return self._parse_response(response)

    def _parse_response(self, response: str) -> Dict[str, Any]:
        lines = response.strip().split('\n')
        parsed_response = {}
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                parsed_response[key.strip().lower()] = value.strip()
        
        return {
            'action': parsed_response.get('action', 'HOLD'),
            'confidence': float(parsed_response.get('confidence', 0)),
            'reasoning': parsed_response.get('reasoning', ''),
            'target_price': float(parsed_response.get('target price', 0)),
            'stop_loss': float(parsed_response.get('stop loss', 0))
        }

class ClaudeProvider(AIProvider):
    def __init__(self, config: Dict[str, Any]):
        self.llm = ChatAnthropic(
            model=config["model_name"],
            anthropic_api_key=config["api_key"],
        )
        self.chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate(
                input_variables=["market_data", "technical_indicators", "sentiment_score", "intermarket_data"],
                template="""Analyze the following market data and provide a trading recommendation:
                Market Data: {market_data}
                Technical Indicators: {technical_indicators}
                Sentiment Score: {sentiment_score}
                Intermarket Data: {intermarket_data}

                Please provide a recommendation in the following format:
                Action: [BUY/SELL/HOLD]
                Confidence: [0-1]
                Reasoning: [Your analysis and reasoning]
                Target Price: [Suggested target price]
                Stop Loss: [Suggested stop loss price]
                """
            )
        )

    async def generate_recommendation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        response = await self.chain.arun(
            market_data=str(data['market_data']),
            technical_indicators=str(data['technical_indicators']),
            sentiment_score=str(data['sentiment_score']),
            intermarket_data=str(data['intermarket_data'])
        )
        return self._parse_response(response)

    def _parse_response(self, response: str) -> Dict[str, Any]:
        lines = response.strip().split('\n')
        parsed_response = {}
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                parsed_response[key.strip().lower()] = value.strip()
        
        return {
            'action': parsed_response.get('action', 'HOLD'),
            'confidence': float(parsed_response.get('confidence', 0)),
            'reasoning': parsed_response.get('reasoning', ''),
            'target_price': float(parsed_response.get('target price', 0)),
            'stop_loss': float(parsed_response.get('stop loss', 0))
        }

class AIProviderFactory:
    @staticmethod
    def create(provider_name: str, config: Dict[str, Any]) -> AIProvider:
        if provider_name == "azure_openai":
            return AzureOpenAIProvider(config)
        elif provider_name == "claude":
            return ClaudeProvider(config)
        else:
            raise ValueError(f"Unsupported AI provider: {provider_name}")