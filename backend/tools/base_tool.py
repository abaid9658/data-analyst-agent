"""
Base Tool class
"""
from abc import ABC, abstractmethod
from typing import Any


class BaseTool(ABC):
    """Abstract base class for all agent tools."""

    @property
    @abstractmethod
    def name(self) -> str:
        """The tool's unique identifier name."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """A description of what the tool does for intent planning."""
        pass

    @abstractmethod
    async def execute(self, params: dict[str, Any]) -> dict[str, Any]:
        """Execute the tool with the provided parameters."""
        pass
