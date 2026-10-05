from abc import abstractmethod
from typing import Protocol

from stepps.trees.binary_tree import BinaryTree


class RedBlack[T](BinaryTree[T], Protocol):
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
