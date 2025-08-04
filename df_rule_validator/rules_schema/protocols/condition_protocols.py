from __future__ import annotations

"""Protocols for rule schema conditions."""

from abc import abstractmethod
from typing import Any, Dict, Protocol, runtime_checkable


@runtime_checkable
class ConditionProtocol(Protocol):
    """Common interface that all condition schemas must implement."""

    type: str

    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary representation of the condition."""
        ...


@runtime_checkable
class ConditionFactory(Protocol):
    """Protocol for objects capable of building conditions from dictionaries."""

    @abstractmethod
    def create_condition(self, data: Dict[str, Any]) -> ConditionProtocol:
        """Create a condition from a dictionary."""
        ...
