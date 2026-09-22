from abc import abstractmethod

from stepps.trees.binary_tree import BinaryTree


class AVL[T]:
    """
    Define the interface for balancing a binary tree.
    """

    @abstractmethod
    def balance(self, tree: BinaryTree[T]) -> BinaryTree[T]:
        """
        Balance the given tree.

        :param tree: The tree to balance.
        :return: The balanced tree.
        """
        ...
