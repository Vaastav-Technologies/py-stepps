from __future__ import annotations

from stepps.nodes import BinaryNode
from stepps.trees.balanced.rb_tree.rb_node import RBNode


class RBNodeImpl[T](RBNode[T]):
    """
    Represent a node in a Red-Black tree.
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

    @property
    def parent(self) -> RBNode[T] | None:
        return self._parent

    @parent.setter
    def parent(self, node: RBNode[T] | None) -> None:
        self._parent = node

    @property
    def color(self) -> int:
        return self._color

    @color.setter
    def color(self, color: int) -> None:
        self._color = color

    def __init__(self, value: T) -> None:
        """
        Initialize a Red-Black tree node.

        :param value: The value to store in the node.
        """
        self._value = value
        self._right = None
        self._left = None
        self._parent = None
        self._color = RBNode.RED

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
