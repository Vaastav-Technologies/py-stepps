from abc import abstractmethod
from typing import Protocol

from stepps.trees.binary_tree import BinaryTree


class AVL[T](BinaryTree[T], Protocol):
    """
    Define the interface for balancing a binary tree.
    """

    @abstractmethod
    def balance(self) -> BinaryTree[T]:
        """
        Balance the binary tree.

        :return: The balanced binary tree.
        """
        ...
