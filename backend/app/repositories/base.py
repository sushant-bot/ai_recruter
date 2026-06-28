"""Repository contracts used by services and API layers."""
from typing import Protocol, TypeVar, runtime_checkable

T = TypeVar("T")


@runtime_checkable
class Repository(Protocol[T]):
    """Generic repository contract."""

    def add(self, item: T) -> T:
        """Persist an item and return the stored version."""

    def get(self, item_id: int) -> T | None:
        """Fetch an item by identifier."""
