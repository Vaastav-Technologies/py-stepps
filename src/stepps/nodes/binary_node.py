from __future__ import annotations

from abc import abstractmethod
from typing import Protocol


class BinaryNode[T](Protocol):

    @property
    @abstractmethod
    def value(self) -> T | None:
        ...

    @property
    @abstractmethod
    def right(self) -> "BinaryNode[T] | None":
        ...

    @property
    @abstractmethod
    def left(self) -> "BinaryNode[T] | None":
        ...

    @abstractmethod
    def is_leaf(self):
        """
        Return whether the node has no children.

        :return: ``True`` if the node has no children, otherwise ``False``.
        """
        pass

    @abstractmethod
    def has_left(self):
        """
        Return whether the node has a left child.

        :return: ``True`` if a left child exists, otherwise ``False``.
        """
        pass

    @abstractmethod
    def has_right(self):
        """
        Return whether the node has a right child.

        :return: ``True`` if a right child exists, otherwise ``False``.
        """
        pass

    @abstractmethod
    def has_children(self):
        """
        Return whether the node has at least one child.

        :return: ``True`` if the node has one or more children, otherwise ``False``.
        """
        pass

    @abstractmethod
    def child_count(self):
        """
        Return the number of children of the node.

        :return: The number of children, either ``0``, ``1``, or ``2``.
        """
        pass


