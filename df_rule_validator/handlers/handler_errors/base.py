from abc import abstractmethod, ABC
from typing import Any, Dict

class HandlerError(ABC):
    """Base class for handler errors."""

    @abstractmethod
    def handle_error(self, *args, **kwargs) -> None:
        """Handle the error based on the provided data and conditions."""
        raise NotImplementedError("Subclasses must implement this method.")