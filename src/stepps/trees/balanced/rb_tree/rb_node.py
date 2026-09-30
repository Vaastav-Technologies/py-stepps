from __future__ import annotations

from abc import abstractmethod
from typing import Protocol

from stepps.nodes import BinaryNode


class RBNode[T](BinaryNode[T], Protocol):
    RED: int = 0
    BLACK: int = 1

    @property
    @abstractmethod
    def parent(self) -> RBNode[T] | None: ...

    @parent.setter
    @abstractmethod
    def parent(self, node: RBNode[T] | None) -> None: ...

    @property
    @abstractmethod
    def color(self) -> int: ...

    @color.setter
    @abstractmethod
    def color(self, color: int) -> None: ...
