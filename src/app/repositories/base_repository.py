from abc import ABC, abstractmethod

class ICollectionRepository(ABC):

    @abstractmethod
    async def has_collection(
        self,
        collection_name: str | None = None, # type: ignore
        collection_id: int | None = None, # type: ignore
    ) -> bool:
        pass

    @abstractmethod
    async def list_collections(
        self,
        show: bool | None = None, # type: ignore
    ) -> list[dict]:
        pass

    @abstractmethod
    async def create_collection(
        self,
        collection_name: str,
        collection_id: int,
        description: str,
    ):
        pass

    @abstractmethod
    async def delete_collection(
        self,
        collection_name: str,
    ) -> None:
        pass

    @abstractmethod
    async def update_collection(
        self,
        collection_name: str,
        data: dict,
    ):
        pass

    @abstractmethod
    async def get_collection(
        self,
        collection_name: str,
    ) -> dict:
        pass



class ITableRepository(ABC):
    @abstractmethod
    async def get_table(self, table_name: str) -> dict:
        pass

    @abstractmethod
    async def create_table(self, table_name: str) -> dict:
        pass

    @abstractmethod
    async def delete_table(self, table_name: str) -> None:
        pass

    @abstractmethod
    async def has_table(self, table_name: str) -> bool:
        pass

    @abstractmethod
    async def list_tables(self) -> list[dict]:
        pass