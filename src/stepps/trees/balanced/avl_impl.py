from typing import override

from stepps.trees.balanced.avl import AVL
from stepps.trees.binary_tree import BinaryTree


class AVLImpl[T](AVL[T]):
    """
    Provide the default implementation for balancing a binary tree using AVL
    rotations.
    """

    @override
    def balance(self, tree: BinaryTree[T]) -> BinaryTree[T]:
        """
        Balance the given tree using AVL rotations.

        :param tree: The tree to balance.
        :return: The balanced tree.
        """
        if tree.is_empty():
            return tree

        left_subtree = self._balance(tree.get_left_subtree())
        right_subtree = self._balance(tree.get_right_subtree())

        tree.set_left_subtree(left_subtree)
        tree.set_right_subtree(right_subtree)

        return self._rebalance(tree)

    def _rebalance(self, tree: BinaryTree[T]) -> BinaryTree[T]:
        """
        Rebalance the given tree if it violates the AVL balance condition.

        :param tree: The tree to rebalance.
        :return: The rebalanced tree.
        """
        balance_factor = self._balance_factor(tree)

        if balance_factor > 1:
            left_subtree = tree.get_left_subtree()

            if self._balance_factor(left_subtree) < 0:
                left_subtree.left_rotate()
                tree.set_left_subtree(left_subtree)

            return tree.right_rotate()

        if balance_factor < -1:
            right_subtree = tree.get_right_subtree()

            if self._balance_factor(right_subtree) > 0:
                right_subtree.right_rotate()
                tree.set_right_subtree(right_subtree)

            return tree.left_rotate()

        return tree

    def _balance_factor(self, tree: BinaryTree[T]) -> int:
        """
        Return the AVL balance factor of the tree.

        :param tree: The tree whose balance factor is calculated.
        :return: The height difference between the left and right subtrees.
        """
        return tree.get_left_subtree().height() - tree.get_right_subtree().height()

    def _balance(self, tree: BinaryTree[T]) -> BinaryTree[T]:
        """
        Recursively balance the given tree.

        :param tree: The tree to balance.
        :return: The balanced tree.
        """
        if tree.is_empty():
            return tree

        left_subtree = self._balance(tree.get_left_subtree())
        right_subtree = self._balance(tree.get_right_subtree())

        tree.set_left_subtree(left_subtree)
        tree.set_right_subtree(right_subtree)

        return self._rebalance(tree)
