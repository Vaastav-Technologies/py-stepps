from types import TracebackType
from typing import Self, override

from stepps.iterators.morris import MorrisIterator
from stepps.nodes import BinaryNode


class MorrisIteratorImpl[T](MorrisIterator[T]):
    """
    Iterate over a binary tree using Morris inorder traversal.

    Nodes are visited in the following order:

    .. code-block:: text

        Left -> Root -> Right

    The traversal takes O(n) total time and O(1) auxiliary space by temporarily
    linking inorder predecessors to their ancestors through right pointers.

    All temporary links are removed when traversal finishes. If traversal
    stops early, call ``close`` or use a ``with`` block to restore the tree.
    Returned nodes may contain temporary links, so do not modify or traverse
    the tree independently until the iterator is exhausted or closed.

    :param root: The root node of the tree to traverse.
    """

    def __init__(self, root: BinaryNode[T] | None) -> None:
        """
        Initialize the Morris inorder iterator.

        :param root: The root node of the tree to traverse.
        """
        self._current: BinaryNode[T] | None = root
        """
        Node from which the next traversal step begins.
        """

    @override
    def __next__(self) -> BinaryNode[T]:
        """
        Return the next node in the inorder traversal.

        Each call takes O(1) amortized time and O(n) time in the worst case.

        :return: The next node in the traversal.
        :raises StopIteration: If all nodes have been visited or the iterator
            has been closed.
        """
        current = self._current

        while current is not None:
            predecessor = current.left

            if predecessor is None:
                self._current = current.right

                return current

            while predecessor.right is not None and predecessor.right is not current:
                predecessor = predecessor.right

            if predecessor.right is None:
                predecessor.right = current
                current = current.left
            else:
                predecessor.right = None
                self._current = current.right

                return current

        raise StopIteration

    @override
    def close(self) -> None:
        """
        Restore temporary links and exhaust the iterator.

        The remaining nodes are visited without being returned to the caller.
        This takes O(n) time in the worst case and O(1) auxiliary space.
        Calling this method on an exhausted or closed iterator has no effect.
        """
        for _ in self:
            pass

    @override
    def __enter__(self) -> Self:
        """
        Return the iterator for use in a context manager.

        :return: The current iterator instance.
        """
        return self

    @override
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """
        Restore temporary links when leaving the context.

        Exceptions from the context are allowed to propagate after cleanup.

        :param exc_type: The exception type, if an exception was raised.
        :param exc_value: The exception instance, if an exception was raised.
        :param traceback: The traceback, if an exception was raised.
        """
        self.close()
