from abc import abstractmethod
from types import TracebackType
from typing import Protocol, Self

from stepps.nodes import BinaryNode


class MorrisIterator[T](Protocol):
    """
    Define the interface for Morris inorder traversal of a binary tree.

    Nodes are visited in Left -> Root -> Right order using O(1) auxiliary
    space. Temporary links are removed when traversal finishes. If traversal
    stops early, call ``close`` or use a ``with`` block to restore the tree.
    Returned nodes may contain temporary links, so do not modify or traverse
    the tree independently until the iterator is exhausted or closed.
    """

    @abstractmethod
    def __iter__(self) -> Self:
        """Return the iterator itself."""
        ...

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
