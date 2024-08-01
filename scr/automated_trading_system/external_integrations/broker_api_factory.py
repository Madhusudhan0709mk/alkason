import logging
from abc import ABC, abstractmethod
from typing import Dict, Any
import aiohttp
from infrastructure.logging_service import LoggingService

class BrokerAPIError(Exception):
    pass

class BrokerAPI(ABC):
    def __init__(self, config: Dict[str, Any], logging_service: LoggingService):
        self.config = config
        self.logging_service = logging_service
        self.session = None

    @abstractmethod
    async def authenticate(self):
        pass

    @abstractmethod
    async def place_order(self, order: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def cancel_order(self, order_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_order_status(self, order_id: str) -> Dict[str, Any]:
        pass

    async def _init_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()

    async def _make_request(self, method: str, url: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        try:
            await self._init_session()
            async with getattr(self.session, method)(url, json=data) as response:
                if response.status >= 400:
                    await self.logging_service.log_error(f"API request failed: {response.status} {await response.text()}")
                    raise BrokerAPIError(f"API request failed with status {response.status}")
                return await response.json()
        except aiohttp.ClientError as e:
            await self.logging_service.log_error(f"HTTP error occurred: {str(e)}")
            raise BrokerAPIError(f"HTTP error: {str(e)}")
        except Exception as e:
            await self.logging_service.log_error(f"Unexpected error occurred: {str(e)}")
            raise BrokerAPIError(f"Unexpected error: {str(e)}")

class AngelOneBrokerAPI(BrokerAPI):
    async def authenticate(self):
        if 'Authorization' not in self.session.headers:
            login_url = f"{self.config['base_url']}/rest/auth/angelbroking/user/v1/loginByPassword"
            login_data = {
                "clientcode": self.config['client_id'],
                "password": self.config['password']
            }
            login_response = await self._make_request('post', login_url, login_data)
            if login_response.get('status'):
                self.session.headers.update({"Authorization": f"Bearer {login_response['data']['jwtToken']}"})
            else:
                raise BrokerAPIError("Failed to login to Angel One")

    async def place_order(self, order: Dict[str, Any]) -> Dict[str, Any]:
        await self.authenticate()
        url = f"{self.config['base_url']}/rest/secure/angelbroking/order/v1/placeOrder"
        return await self._make_request('post', url, order)

    async def cancel_order(self, order_id: str) -> Dict[str, Any]:
        await self.authenticate()
        url = f"{self.config['base_url']}/rest/secure/angelbroking/order/v1/cancelOrder"
        data = {"variety": "NORMAL", "orderid": order_id}
        return await self._make_request('post', url, data)

    async def get_order_status(self, order_id: str) -> Dict[str, Any]:
        await self.authenticate()
        url = f"{self.config['base_url']}/rest/secure/angelbroking/order/v1/details/{order_id}"
        return await self._make_request('get', url)

class UpstoxBrokerAPI(BrokerAPI):
    async def authenticate(self):
        if 'Authorization' not in self.session.headers:
            # Implement Upstox OAuth flow here
            # This is a placeholder and should be replaced with actual Upstox OAuth process
            self.session.headers.update({"Authorization": f"Bearer {self.config['access_token']}"})

    async def place_order(self, order: Dict[str, Any]) -> Dict[str, Any]:
        await self.authenticate()
        url = f"{self.config['base_url']}/order/place"
        return await self._make_request('post', url, order)

    async def cancel_order(self, order_id: str) -> Dict[str, Any]:
        await self.authenticate()
        url = f"{self.config['base_url']}/order/cancel/{order_id}"
        return await self._make_request('delete', url)

    async def get_order_status(self, order_id: str) -> Dict[str, Any]:
        await self.authenticate()
        url = f"{self.config['base_url']}/order/{order_id}"
        return await self._make_request('get', url)

class ZerodhaBrokerAPI(BrokerAPI):
    async def authenticate(self):
        if 'Authorization' not in self.session.headers:
            # Implement Zerodha OAuth flow here
            # This is a placeholder and should be replaced with actual Zerodha OAuth process
            self.session.headers.update({"X-Kite-Version": "3", "Authorization": f"token {self.config['api_key']}:{self.config['access_token']}"})

    async def place_order(self, order: Dict[str, Any]) -> Dict[str, Any]:
        await self.authenticate()
        url = f"{self.config['base_url']}/orders/regular"
        return await self._make_request('post', url, order)

    async def cancel_order(self, order_id: str) -> Dict[str, Any]:
        await self.authenticate()
        url = f"{self.config['base_url']}/orders/regular/{order_id}"
        return await self._make_request('delete', url)

    async def get_order_status(self, order_id: str) -> Dict[str, Any]:
        await self.authenticate()
        url = f"{self.config['base_url']}/orders/{order_id}"
        return await self._make_request('get', url)

class BrokerAPIFactory:
    @staticmethod
    def create(broker_name: str, config: Dict[str, Any], logging_service: LoggingService) -> BrokerAPI:
        if broker_name == "angel_one":
            return AngelOneBrokerAPI(config, logging_service)
        elif broker_name == "upstox":
            return UpstoxBrokerAPI(config, logging_service)
        elif broker_name == "zerodha":
            return ZerodhaBrokerAPI(config, logging_service)
        else:
            raise ValueError(f"Unsupported broker: {broker_name}")