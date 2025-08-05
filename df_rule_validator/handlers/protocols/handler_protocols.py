from __future__ import annotations


from abc import abstractmethod
from pandas import pd
from typing import Any, Dict, Protocol, runtime_checkable

@runtime_checkable
class DeleteRowProtocol(Protocol):
    """Protocol for objects capable of deleting rows based on conditions."""

    @abstractmethod
    def HandlerError(self, data: pd.DataFrame, conditions: pd.Series) -> pd.DataFrame:
        """Delete rows from the dataset based on the provided conditions."""
        ...

