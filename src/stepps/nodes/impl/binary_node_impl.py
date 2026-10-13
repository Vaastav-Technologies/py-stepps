from __future__ import annotations

from stepps.nodes import BinaryNode


class BinaryNodeImpl[T](BinaryNode[T]):
    """
    Represent a node in a binary tree.

    """

    @property
    def value(self) -> T | None:
        return self._value

    @property
    def right(self) -> BinaryNode[T] | None:
        return self._right

    @right.setter
    def right(self, node: BinaryNode[T] | None) -> None:
        self._right = node

    @property
    def left(self) -> BinaryNode[T] | None:
        return self._left

    @left.setter
    def left(self, node: BinaryNode[T] | None) -> None:
        self._left = node

    def __init__(self, value: T) -> None:
        """
        Initialize a binary tree node.

        :param value: The value to store in the node.
        """
        self._value: T = value
        self._right = None
        self._left = None

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
