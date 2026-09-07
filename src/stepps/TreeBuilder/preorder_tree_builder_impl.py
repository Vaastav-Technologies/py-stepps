from collections.abc import Sequence
from typing import override

from stepps.nodes import BinaryNode
from stepps.TreeBuilder.preorder_tree_builder import PreOrderTreeBuilder


class PreOrderTreeBuilderImpl[T](PreOrderTreeBuilder[T]):
    """
    Provide the default implementation for building a binary tree
    from a preorder sequence.
    """

    @override
    def build(self, sequence: Sequence[T]) -> BinaryNode[T] | None:
        """
        Build a binary tree from a preorder sequence.

        :param sequence: The sequence of values used to build the tree.
        :return: The root node of the constructed tree, or ``None`` if the
            sequence is empty.
        """
        return self._build(sequence, 0, len(sequence))

    def _build(
        self,
        sequence: Sequence[T],
        index: int,
        size: int,
    ) -> BinaryNode[T] | None:
        """
        Recursively construct the tree from the given preorder sequence.

        :param sequence: The sequence of values used to build the tree.
        :param index: The index of the root value in the current subtree.
        :param size: The number of elements in the current subtree.
        :return: The root node of the constructed subtree.
        :complexity: O(n) time and O(n) total space complexity, including the
            constructed tree. The recursion stack uses O(log n) auxiliary space.
        """
        if size <= 0:
            return None

        root = BinaryNode(sequence[index])

        left_size = (size - 1) // 2
        right_size = size - 1 - left_size

        root.left = self._build(
            sequence,
            index + 1,
            left_size,
        )

        root.right = self._build(
            sequence,
            index + 1 + left_size,
            right_size,
        )

        return root
