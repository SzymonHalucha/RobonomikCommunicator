from __future__ import annotations
from abc import ABC, abstractmethod


class ISerialize(ABC):
    @abstractmethod
    def serialize(self) -> dict:
        pass

    @abstractmethod
    def deserialize(self, dict: dict) -> object:
        pass
