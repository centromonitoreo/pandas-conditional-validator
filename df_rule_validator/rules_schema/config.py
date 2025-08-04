"""Utilities for loading rule configurations from external sources."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List

import yaml
from pydantic import BaseModel

from .rules import ParametricRule


class ConfigLoader(ABC):
    """Abstract interface for configuration loaders."""

    @abstractmethod
    def load(self, source: str) -> Dict[str, Any]:
        """Load raw data from a source."""
        raise NotImplementedError


class YamlConfigLoader(ConfigLoader):
    """Concrete loader that reads configuration from YAML files."""

    def load(self, source: str) -> Dict[str, Any]:
        with open(source, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)


class RulesConfig(BaseModel):
    """Top-level container holding all parametric rules."""

    validations: List[ParametricRule] = None

    @classmethod
    def from_source(cls, source: str, loader: ConfigLoader) -> "RulesConfig":
        """Load rule configuration using a provided loader."""
        raw_data = loader.load(source)
        return cls._build_from_data(raw_data)

    @classmethod
    def from_yaml(cls, yaml_path: str) -> "RulesConfig":
        """Convenience method for loading configuration from YAML."""
        loader = YamlConfigLoader()
        return cls.from_source(yaml_path, loader)

    @classmethod
    def _build_from_data(cls, raw_data: Dict[str, Any]) -> "RulesConfig":
        """Construct configuration from raw dictionary data."""
        params_raw = raw_data.get("validations")
        if not isinstance(params_raw, list):
            raise ValueError(
                "El archivo debe contener una lista de validaciones bajo la clave 'validations'."
            )

        validations = [ParametricRule.from_dict(param) for param in params_raw]
        return cls(validations=validations)
