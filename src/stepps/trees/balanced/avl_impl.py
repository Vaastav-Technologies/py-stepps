from typing import override

from stepps.nodes import BinaryNode
from stepps.trees.balanced.avl import AVL
from stepps.trees.binary_tree import BinaryTree


class AVLImpl[T](AVL[T]):
    """
    Provide the default implementation for balancing a binary tree using AVL
    rotations.
    """

    def __init__(
        self,
        tree: BinaryTree[T],
        balance_factor: int = 1,
    ) -> None:
        self.tree = tree
        self.balance_factor = balance_factor

    @override
    def balance(self) -> BinaryTree[T]:
        """
        Balance the tree using AVL rotations.

        :return: The balanced tree.
        """
        self.tree = self._balance(self.tree)
        return self.tree

    def insert(self, value: T) -> BinaryNode[T]:
        """
        Insert a value into the tree and balance it.

        :param value: The value to insert.
        :return: The inserted node.
        """
        node = self.tree.insert(value)
        self.balance()
        return node

    def delete(self, value: T) -> bool:
        """
        Delete a value from the tree and balance it.

        :param value: The value to delete.
        :return: True if the value was deleted, otherwise False.
        """
        deleted = self.tree.delete(value)
        self.balance()
        return deleted

    def find(self, value: T) -> BinaryNode[T] | None:
        """
        Find a value in the tree.

        :param value: The value to find.
        :return: The node containing the value, or None if not found.
        """
        return self.tree.find(value)

    def contains(self, value: T) -> bool:
        """
        Check whether the tree contains a value.

        :param value: The value to check.
        :return: True if the value exists, otherwise False.
        """
        return self.tree.contains(value)

    def __contains__(self, value: T) -> bool:
        return value in self.tree

    def height(self) -> int:
        """
        Return the height of the tree.

        :return: The tree height.
        """
        return self.tree.height()

    def count_leaves(self) -> int:
        """
        Count the leaf nodes in the tree.

        :return: The number of leaf nodes.
        """
        return self.tree.count_leaves()

    def count_internal_nodes(self) -> int:
        """
        Count the internal nodes in the tree.

        :return: The number of internal nodes.
        """
        return self.tree.count_internal_nodes()

    def get_root(self) -> BinaryNode[T] | None:
        """
        Return the root node.

        :return: The root node, or None if the tree is empty.
        """
        return self.tree.get_root()

    def get_left_subtree(self) -> BinaryTree[T]:
        """
        Return the left subtree.

        :return: The left subtree.
        """
        return self.tree.get_left_subtree()

    def get_right_subtree(self) -> BinaryTree[T]:
        """
        Return the right subtree.

        :return: The right subtree.
        """
        return self.tree.get_right_subtree()

    def set_left_subtree(self, subtree: BinaryTree[T]) -> None:
        """
        Set the left subtree.

        :param subtree: The tree to use as the left subtree.
        """
        self.tree.set_left_subtree(subtree)

    def set_right_subtree(self, subtree: BinaryTree[T]) -> None:
        """
        Set the right subtree.

        :param subtree: The tree to use as the right subtree.
        """
        self.tree.set_right_subtree(subtree)

    def right_rotate(self) -> BinaryTree[T]:
        """
        Perform a right rotation.

        :return: The tree after the rotation.
        """
        self.tree = self.tree.right_rotate()
        return self.tree

    def left_rotate(self) -> BinaryTree[T]:
        """
        Perform a left rotation.

        :return: The tree after the rotation.
        """
        self.tree = self.tree.left_rotate()
        return self.tree

    def invert_tree(self) -> None:
        """
        Invert the tree.
        """
        self.tree.invert_tree()

    def is_empty(self) -> bool:
        """
        Check whether the tree is empty.

        :return: True if the tree is empty, otherwise False.
        """
        return self.tree.is_empty()

    def clear(self) -> None:
        """
        Clear the tree.
        """
        self.tree.clear()

    def size(self) -> int:
        """
        Return the number of nodes in the tree.

        :return: The tree size.
        """
        return self.tree.size()

    def __len__(self) -> int:
        return len(self.tree)

    def __bool__(self) -> bool:
        return bool(self.tree)

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

    def _rebalance(self, tree: BinaryTree[T]) -> BinaryTree[T]:
        """
        Rebalance the given tree if it violates the AVL balance condition.

        :param tree: The tree to rebalance.
        :return: The rebalanced tree.
        """
        balance_factor = self._balance_factor(tree)

        if balance_factor > self.balance_factor:
            left_subtree = tree.get_left_subtree()

            if self._balance_factor(left_subtree) < 0:
                left_subtree.left_rotate()
                tree.set_left_subtree(left_subtree)

            return tree.right_rotate()

        if balance_factor < -self.balance_factor:
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
