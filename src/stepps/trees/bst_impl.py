from typing import override

from stepps.nodes import BinaryNode
from stepps.nodes.binary_node import BinaryNodeImpl
from stepps.trees.binary_tree_impl import BinaryTreeImpl
from stepps.trees.bst import BST, Comparable


class BSTImpl[T: Comparable](BST[T], BinaryTreeImpl[T]):
    """
    Provide the default implementation of a binary search tree.
    """

    @override
    def insert(self, value: T) -> BinaryNode[T]:
        """
        Insert a value into the binary search tree.

        Duplicate values are not inserted.

        :param value: The value to insert.
        :return: The node containing ``value``. If the value already exists,
            the existing node is returned.
        """
        new_node = BinaryNodeImpl(value)

        if self.root is None:
            self.root = new_node
            self._size = 1
            return new_node

        current: BinaryNode[T] | None = self.root
        parent: BinaryNode[T] | None = None

        while current is not None:
            parent = current

            if value < current.value:
                current = current.left
            elif value > current.value:
                current = current.right
            else:
                return current

        assert parent is not None

        if value < parent.value:
            parent.left = new_node
        else:
            parent.right = new_node

        self._size += 1

        return new_node

    @override
    def find(self, value: T) -> BinaryNode[T] | None:
        """
        Find a node containing ``value``.

        :param value: The value to search for.
        :return: The matching node, or ``None`` if the value is not found.
        """
        current = self.root

        while current is not None:
            if value == current.value:
                return current

            if value < current.value:
                current = current.left
            else:
                current = current.right

        return None

    @override
    def minimum(self, node: BinaryNode[T] | None = None) -> BinaryNode[T] | None:
        """
        Find the minimum-valued node in a subtree.

        If ``node`` is not provided, the search starts at the tree root.

        :param node: The node at which to start the search.
        :return: The minimum-valued node, or ``None`` if the tree is empty.
        """
        if node is None:
            if self.root is None:
                return None
            node = self.root

        while node.left is not None:
            node = node.left

        return node

    @override
    def maximum(self, node: BinaryNode[T] | None = None) -> BinaryNode[T] | None:
        """
        Find the maximum-valued node in a subtree.

        If ``node`` is not provided, the search starts at the tree root.

        :param node: The node at which to start the search.
        :return: The maximum-valued node, or ``None`` if the tree is empty.
        """
        if node is None:
            if self.root is None:
                return None
            node = self.root

        while node.right is not None:
            node = node.right

        return node

    @override
    def delete(self, value: T) -> bool:
        """
        Delete a value from the binary search tree.

        :param value: The value to delete.
        :return: ``True`` if the value was found and deleted, otherwise
            ``False``.
        """
        parent: BinaryNode[T] | None = None
        node = self.root

        while node is not None and node.value != value:
            parent = node

            if value < node.value:
                node = node.left
            else:
                node = node.right

        if node is None:
            return False

        if node.left is None:
            replacement = node.right

        elif node.right is None:
            replacement = node.left

        else:
            successor_parent = node
            successor = node.right

            while successor.left is not None:
                successor_parent = successor
                successor = successor.left

            if successor_parent != node:
                successor_parent.left = successor.right
                successor.right = node.right

            replacement = successor
            replacement.left = node.left

        if parent is None:
            self.root = replacement
        elif parent.left is node:
            parent.left = replacement
        else:
            parent.right = replacement

        self._size -= 1

        return True

    @override
    def min(self) -> BinaryNode[T] | None:
        """
        Return the minimum-valued node in the tree.

        :return: The minimum-valued node, or ``None`` if the tree is empty.
        """
        return self.minimum()

    @override
    def max(self) -> BinaryNode[T] | None:
        """
        Return the maximum-valued node in the tree.

        :return: The maximum-valued node, or ``None`` if the tree is empty.
        """
        return self.maximum()
