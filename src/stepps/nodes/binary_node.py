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


class BinaryNodeImpl[T](BinaryNode[T]):
    """
    Represent a node in a binary tree.

    """

    @property
    def value(self) -> T | None:
        return self._value

    @property
    def right(self) -> T | None:
        return self._right

    @property
    def left(self) -> T | None:
        return self._left

    def __init__(self, value: T) -> None:
        """
        Initialize a binary tree node.

        :param value: The value to store in the node.
        """
        self._value: T = value
        self._right: BinaryNode[T] | None = None
        self._left: BinaryNode[T] | None = None

    def is_leaf(self) -> bool:
        """
        Return whether the node has no children.

        :return: ``True`` if the node has no children, otherwise ``False``.
        """
        return self.left is None and self.right is None

    def has_left(self) -> bool:
        """
        Return whether the node has a left child.

        :return: ``True`` if a left child exists, otherwise ``False``.
        """
        return self.left is not None

    def has_right(self) -> bool:
        """
        Return whether the node has a right child.

        :return: ``True`` if a right child exists, otherwise ``False``.
        """
        return self.right is not None

    def has_children(self) -> bool:
        """
        Return whether the node has at least one child.

        :return: ``True`` if the node has one or more children, otherwise ``False``.
        """
        return self.left is not None or self.right is not None

    def child_count(self) -> int:
        """
        Return the number of children of the node.

        :return: The number of children, either ``0``, ``1``, or ``2``.
        """
        return int(self.left is not None) + int(self.right is not None)
