from collections.abc import Sequence
from typing import override

from stepps.nodes import BinaryNode
from stepps.TreeBuilder.postorder_tree_builder import PostOrderTreeBuilder


class PostOrderTreeBuilderImpl[T](PostOrderTreeBuilder[T]):
    """
    Provide the default implementation for building a binary tree
    from a postorder sequence.
    """

    @override
    def build(self, sequence: Sequence[T]) -> BinaryNode[T] | None:
        """
        Build a binary tree from a postorder sequence.

        :param sequence: The sequence of values used to build the tree.
        :return: The root node of the constructed tree, or ``None`` if the
            sequence is empty.
        """
        return self._build(sequence, 0, len(sequence))

    def _build(
        self,
        sequence: Sequence[T],
        start: int,
        size: int,
    ) -> BinaryNode[T] | None:
        """
        Recursively construct the tree from the given postorder sequence.

        :param sequence: The sequence of values used to build the tree.
        :param start: The starting index of the current subtree.
        :param size: The number of elements in the current subtree.
        :return: The root node of the constructed subtree.
        :complexity: O(n) time and O(n) total space complexity, including the
            constructed tree. The recursion stack uses O(log n) auxiliary
            space.
        """
        if size <= 0:
            return None

        root_index = start + size - 1
        root = BinaryNode(sequence[root_index])

        remaining = size - 1
        left_size = remaining // 2
        right_size = remaining - left_size

        root.left = self._build(
            sequence,
            start,
            left_size,
        )

        root.right = self._build(
            sequence,
            start + left_size,
            right_size,
        )

        return root
