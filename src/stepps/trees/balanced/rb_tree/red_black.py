from abc import abstractmethod
from typing import Protocol

from stepps.comparable import Comparable
from stepps.trees.binary_tree import BinaryTree
from stepps.trees.bst import BST


class RedBlack[T: Comparable](BST[T], Protocol):
    """
    Define the interface for a Red-Black tree.
    """

    @abstractmethod
    def balance(self) -> BinaryTree[T]:
        """
        Balance the tree using Red-Black tree rules.

        :return: The balanced tree.
        """
        ...
