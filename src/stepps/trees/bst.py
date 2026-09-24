from abc import abstractmethod
from typing import Protocol

from stepps.nodes import BinaryNode
from stepps.trees.binary_tree import BinaryTree


class Comparable(Protocol):
    """
    Define the comparison operations required by a binary search tree.
    """

    def __lt__(self, other: object, /) -> bool: ...

    def __gt__(self, other: object, /) -> bool: ...


class BST[T: Comparable](BinaryTree[T], Protocol):
    """
    Define the interface for binary search tree implementations.

    A binary search tree maintains the ordering property that values
    smaller than a node are stored in its left subtree and values
    greater than a node are stored in its right subtree.
    """

    @abstractmethod
    def minimum(self, node: BinaryNode[T] | None = None) -> BinaryNode[T] | None:
        """
        Find the minimum-valued node in a subtree.

        :param node: The node at which to start the search.
        :return: The minimum-valued node, or ``None`` if the tree is empty.
        """
        ...

    @abstractmethod
    def maximum(self, node: BinaryNode[T] | None = None) -> BinaryNode[T] | None:
        """
        Find the maximum-valued node in a subtree.

        :param node: The node at which to start the search.
        :return: The maximum-valued node, or ``None`` if the tree is empty.
        """
        ...

    @abstractmethod
    def min(self) -> BinaryNode[T] | None:
        """
        Return the minimum-valued node in the tree.

        :return: The minimum-valued node, or ``None`` if the tree is empty.
        """
        ...

    @abstractmethod
    def max(self) -> BinaryNode[T] | None:
        """
        Return the maximum-valued node in the tree.

        :return: The maximum-valued node, or ``None`` if the tree is empty.
        """
        ...
