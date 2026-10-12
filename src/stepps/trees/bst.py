from abc import abstractmethod
from typing import Protocol

from stepps.comparable import Comparable
from stepps.nodes import BinaryNode
from stepps.trees.binary_tree import BinaryTree


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
