from abc import ABC, abstractmethod
from typing import List, Dict, Any

class Observer(ABC):
    @abstractmethod
    async def update(self, data: Dict[str, Any]):
        pass

class MarketDataSubject:
    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    async def notify(self, data: Dict[str, Any]):
        for observer in self._observers:
            await observer.update(data)
