from abc import ABC, abstractmethod
from typing import Dict, Any
from langchain.llms import AzureOpenAI
from langchain.chat_models import ChatAnthropic
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

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
                input_variables=["market_data"],
                template="Analyze the following market data and provide a trading recommendation:\n{market_data}"
            )
        )

    async def generate_recommendation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            result = await self.chain.arun(market_data=str(data))
            return {"recommendation": result, "provider": "Azure OpenAI"}
        except Exception as e:
            print(f"Error in AzureOpenAIProvider: {str(e)}")
            return {"error": str(e), "provider": "Azure OpenAI"}

class ClaudeProvider(AIProvider):
    def __init__(self, config: Dict[str, Any]):
        self.llm = ChatAnthropic(
            model=config["model_name"],
            anthropic_api_key=config["api_key"],
        )
        self.chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate(
                input_variables=["market_data"],
                template="Analyze the following market data and provide a trading recommendation:\n{market_data}"
            )
        )

    async def generate_recommendation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            result = await self.chain.arun(market_data=str(data))
            return {"recommendation": result, "provider": "Claude"}
        except Exception as e:
            print(f"Error in ClaudeProvider: {str(e)}")
            return {"error": str(e), "provider": "Claude"}

class AIProviderFactory:
    @staticmethod
    def create(provider_name: str, config: Dict[str, Any]) -> AIProvider:
        if provider_name == "azure_openai":
            return AzureOpenAIProvider(config)
        elif provider_name == "claude":
            return ClaudeProvider(config)
        else:
            raise ValueError(f"Unsupported AI provider: {provider_name}")