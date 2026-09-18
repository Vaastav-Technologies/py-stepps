from typing import override

from stepps.nodes import BinaryNode
from stepps.trees.balanced.avl import AVL
from stepps.trees.binary_tree import BinaryTree


class AVLImpl[T](AVL[T]):
    """
    Provide the default implementation for balancing a binary tree.
    """

    @override
    def balance(self, tree: BinaryTree[T]) -> BinaryTree[T]:
        """
        Balance the given tree using AVL rotations.

        :param tree: The tree to balance.
        :return: The balanced tree.
        """
        tree.root = self._balance(tree.root)
        return tree

    def _balance(
        self,
        node: BinaryNode[T] | None,
    ) -> BinaryNode[T] | None:
        """
        Recursively balance the subtree rooted at ``node``.

        :param node: The root of the subtree.
        :return: The new root of the subtree.
        """
        if node is None:
            return None

        node.left = self._balance(node.left)
        node.right = self._balance(node.right)

        balance = self._balance_factor(node)

        if balance > 1:
            assert node.left is not None

            if self._balance_factor(node.left) < 0:
                node.left = self._rotate_left(node.left)

            node = self._rotate_right(node)

        elif balance < -1:
            assert node.right is not None

            if self._balance_factor(node.right) > 0:
                node.right = self._rotate_right(node.right)

            node = self._rotate_left(node)

        node.left = self._balance(node.left)
        node.right = self._balance(node.right)

        return node

    def _height(self, node: BinaryNode[T] | None) -> int:
        """
        Return the height of a subtree.

        :param node: The root of the subtree.
        :return: The height of the subtree.
        """
        if node is None:
            return -1

        return 1 + max(
            self._height(node.left),
            self._height(node.right),
        )

    def _balance_factor(self, node: BinaryNode[T]) -> int:
        """
        Return the balance factor of a node.

        :param node: The node whose balance factor is calculated.
        :return: The height difference between the left and right subtrees.
        """
        return self._height(node.left) - self._height(node.right)

    def _rotate_left(self, node: BinaryNode[T]) -> BinaryNode[T]:
        """
        Perform a left rotation.

        :param node: The root of the subtree to rotate.
        :return: The new root of the subtree.
        """
        new_root = node.right

        assert new_root is not None

        node.right = new_root.left
        new_root.left = node

        return new_root

    def _rotate_right(self, node: BinaryNode[T]) -> BinaryNode[T]:
        """
        Perform a right rotation.

        :param node: The root of the subtree to rotate.
        :return: The new root of the subtree.
        """
        new_root = node.left

        assert new_root is not None

        node.left = new_root.right
        new_root.right = node

        return new_root
