from abc import abstractmethod
from types import TracebackType
from typing import Self

from stepps.iterators.base_iterator import BinaryTreeIterator
from stepps.nodes import BinaryNode


class MorrisIterator[T](BinaryTreeIterator[BinaryNode[T]]):
    """
    Define the binary tree iterator interface for Morris inorder traversal.

    Like ``InOrderIterator``, this iterator visits nodes in Left -> Root -> Right
    order. Inorder describes the visit order; Morris describes the traversal
    algorithm. ``InOrderIterator`` uses an explicit stack with O(h) auxiliary
    space, where h is the tree height. Morris traversal uses O(1) auxiliary
    space by temporarily linking inorder predecessors to their ancestors
    through right pointers, without a stack or recursion.

    Temporary links are removed when traversal finishes. If traversal
    stops early, call ``close`` or use a ``with`` block to restore the tree.
    Returned nodes may contain temporary links, so do not modify or traverse
    the tree independently until the iterator is exhausted or closed.
    """

    @abstractmethod
    def __next__(self) -> BinaryNode[T]:
        """
        Return the next node in inorder traversal.

        :return: The next node in the traversal.
        :raises StopIteration: If the iterator is exhausted or closed.
        """
        ...

    @abstractmethod
    def close(self) -> None:
        """
        Restore temporary links and exhaust the iterator.

        Calling this method on an exhausted or closed iterator has no effect.
        """
        ...

    @abstractmethod
    def __enter__(self) -> Self:
        """Return the iterator for use in a context manager."""
        ...

    @abstractmethod
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Restore temporary links, allowing exceptions to propagate."""
        ...
