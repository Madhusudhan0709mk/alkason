from abc import ABC, abstractmethod
from typing import Any, List

class Repository(ABC):
    @abstractmethod
    async def get(self, id: str) -> Any:
        pass

    @abstractmethod
    async def get_all(self) -> List[Any]:
        pass

    @abstractmethod
    async def add(self, entity: Any) -> str:
        pass

    @abstractmethod
    async def update(self, id: str, entity: Any) -> bool:
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        pass
