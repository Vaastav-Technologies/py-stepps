from abc import abstractmethod

from stepps.nodes import BinaryNode
from stepps.trees.tree import Tree


class BinaryTree[T](Tree[T]):
    """
    Define the interface for binary tree implementations.
    """

    @abstractmethod
    def find(self, value: T) -> BinaryNode[T] | None:
        """
        Find the first node containing ``value``.

        :param value: The value to search for.
        :return: The matching node, or ``None`` if the value is not found.
        """
        ...

    @abstractmethod
    def contains(self, value: T) -> bool:
        """
        Return whether ``value`` exists in the tree.

        :param value: The value to search for.
        :return: ``True`` if the value exists, otherwise ``False``.
        """
        ...

    @abstractmethod
    def __contains__(self, value: T) -> bool:
        """
        Return whether ``value`` exists in the tree.

        :param value: The value to search for.
        :return: ``True`` if the value exists, otherwise ``False``.
        """
        ...

    @abstractmethod
    def height(self) -> int:
        """
        Return the height of the tree.

        :return: The height of the tree.
        """
        ...

    @abstractmethod
    def count_leaves(self) -> int:
        """
        Return the number of leaf nodes in the tree.

        :return: The number of leaf nodes.
        """
        ...

    @abstractmethod
    def count_internal_nodes(self) -> int:
        """
        Return the number of internal nodes in the tree.

        :return: The number of internal nodes.
        """
        ...

    @abstractmethod
    def insert(self, value: T) -> BinaryNode[T]:
        """
        Insert a value into the tree.

        :param value: The value to insert.
        :return: The node containing the inserted value.
        """
        ...

    @abstractmethod
    def delete(self, value: T) -> bool:
        """
        Delete a value from the tree.

        :param value: The value to delete.
        :return: ``True`` if the value was deleted, otherwise ``False``.
        """
        ...

    @abstractmethod
    def invert_tree(self) -> None:
        """
        Invert the binary tree in place.

        The left and right children of every node are exchanged.

        :return: ``None``.
        """
        ...

    @abstractmethod
    def get_left_subtree(self) -> BinaryTree[T]:
        """
        Return the left subtree.

        :return: The left subtree.
        """
        ...

    @abstractmethod
    def get_right_subtree(self) -> BinaryTree[T]:
        """
        Return the right subtree.

        :return: The right subtree.
        """
        ...

    @abstractmethod
    def right_rotation(self) -> BinaryNode[T] | None:
        """
        Perform a right rotation on the tree.

        :return: The new root node after the rotation.
        """
        ...

    @abstractmethod
    def left_rotation(self) -> BinaryNode[T] | None:
        """
        Perform a left rotation on the tree.

        :return: The new root node after the rotation.
        """
        ...
