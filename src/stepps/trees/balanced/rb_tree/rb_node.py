from __future__ import annotations

from abc import abstractmethod
from typing import Protocol

from stepps.nodes import BinaryNode


class RBNode[T](BinaryNode[T], Protocol):
    """
    Define the interface for nodes in a Red-Black tree.

    Extend a binary node with a parent reference and a color.
    ``RED`` is represented by ``0`` and ``BLACK`` by ``1``.
    """

    RED: int = 0
    BLACK: int = 1

    @property
    @abstractmethod
    def parent(self) -> RBNode[T] | None:
        """
        Return the parent node.

        :return: The parent node, or ``None`` if the node has no parent.
        """
        ...

    @parent.setter
    @abstractmethod
    def parent(self, node: RBNode[T] | None) -> None:
        """
        Set the parent node.

        :param node: The parent node, or ``None`` if the node has no parent.
        :return: ``None``.
        """
        ...

    @property
    @abstractmethod
    def color(self) -> int:
        """
        Return the color of the node.

        :return: ``RED`` or ``BLACK``.
        """
        ...

    @color.setter
    @abstractmethod
    def color(self, color: int) -> None:
        """
        Set the color of the node.

        :param color: The node color, represented by ``RED`` or ``BLACK``.
        :return: ``None``.
        """
        ...
