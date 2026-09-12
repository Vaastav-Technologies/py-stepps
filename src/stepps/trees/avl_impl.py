from typing import override

from stepps.nodes import BinaryNode
from stepps.trees.avl import AVL
from stepps.trees.bst import Comparable
from stepps.trees.bst_impl import BSTImpl


class AVLImpl[T: Comparable](BSTImpl[T], AVL[T]):
    """
    Provide the default implementation of an AVL tree.
    """

    def __init__(self) -> None:
        super().__init__()
        self._heights: dict[int, int] = {}

    @override
    def clear(self) -> None:
        """
        Remove all nodes from the tree.
        """
        super().clear()
        self._heights.clear()

    @override
    def insert(self, value: T) -> BinaryNode[T]:
        """
        Insert a value into the AVL tree.

        Duplicate values are not inserted.

        :param value: The value to insert.
        :return: The node containing ``value``. If the value already exists,
            the existing node is returned.
        """
        existing = self.find(value)

        if existing is not None:
            return existing

        node = BinaryNode(value)
        self._heights[id(node)] = 0

        self.root = self._insert(self.root, node)
        self._size += 1

        return node

    def _insert(
        self,
        root: BinaryNode[T] | None,
        node: BinaryNode[T],
    ) -> BinaryNode[T]:
        """
        Recursively insert a node and rebalance the subtree.

        :param root: The root of the current subtree.
        :param node: The node to insert.
        :return: The new root of the subtree.
        """
        if root is None:
            return node

        if node.value < root.value:
            root.left = self._insert(root.left, node)
        else:
            root.right = self._insert(root.right, node)

        self._update_height(root)

        return self._rebalance(root)

    @override
    def delete(self, value: T) -> bool:
        """
        Delete a value from the AVL tree and rebalance the tree.

        :param value: The value to delete.
        :return: ``True`` if the value was found and deleted, otherwise
            ``False``.
        """
        if self.find(value) is None:
            return False

        self.root = self._delete(self.root, value)
        self._size -= 1

        return True

    def _delete(
        self,
        root: BinaryNode[T] | None,
        value: T,
    ) -> BinaryNode[T] | None:
        """
        Recursively delete a value and rebalance the subtree.

        :param root: The root of the current subtree.
        :param value: The value to delete.
        :return: The new root of the subtree.
        """
        if root is None:
            return None

        if value < root.value:
            root.left = self._delete(root.left, value)

        elif value > root.value:
            root.right = self._delete(root.right, value)

        else:
            if root.left is None:
                replacement = root.right
                self._heights.pop(id(root), None)
                return replacement

            if root.right is None:
                replacement = root.left
                self._heights.pop(id(root), None)
                return replacement

            successor = self.minimum(root.right)

            assert successor is not None

            root.value = successor.value
            root.right = self._delete(root.right, successor.value)

        self._update_height(root)

        return self._rebalance(root)

    def _height(self, node: BinaryNode[T] | None) -> int:
        """
        Return the height of a node.

        :param node: The node whose height is requested.
        :return: The node height, or ``-1`` for ``None``.
        """
        if node is None:
            return -1

        return self._heights[id(node)]

    def _update_height(self, node: BinaryNode[T]) -> None:
        """
        Update the stored height of a node.

        :param node: The node whose height should be updated.
        """
        node_height = 1 + max(
            self._height(node.left),
            self._height(node.right),
        )

        self._heights[id(node)] = node_height

    def _balance_factor(self, node: BinaryNode[T]) -> int:
        """
        Return the balance factor of a node.

        :param node: The node whose balance factor is requested.
        :return: The height difference between the left and right subtrees.
        """
        return self._height(node.left) - self._height(node.right)

    def _rebalance(self, node: BinaryNode[T]) -> BinaryNode[T]:
        """
        Rebalance a subtree rooted at ``node``.

        :param node: The root of the subtree to rebalance.
        :return: The new root of the subtree.
        """
        balance = self._balance_factor(node)

        if balance > 1:
            assert node.left is not None

            if self._balance_factor(node.left) < 0:
                node.left = self._rotate_left(node.left)

            return self._rotate_right(node)

        if balance < -1:
            assert node.right is not None

            if self._balance_factor(node.right) > 0:
                node.right = self._rotate_right(node.right)

            return self._rotate_left(node)

        return node

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

        self._update_height(node)
        self._update_height(new_root)

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

        self._update_height(node)
        self._update_height(new_root)

        return new_root

    @override
    def height(self) -> int:
        """
        Return the height of the AVL tree.

        :return: The height of the tree.
        """
        return self._height(self.root)
