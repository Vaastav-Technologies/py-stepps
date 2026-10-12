from typing import Protocol


class Comparable(Protocol):
    """
    Define the comparison operations required by ordered tree implementations.
    """

    def __lt__(self, other: object, /) -> bool:
        """
        Return whether this value is less than another value.

        :param other: The value to compare with.
        :return: ``True`` if this value is less than ``other``, otherwise
            ``False``.
        """
        ...

    def __gt__(self, other: object, /) -> bool:
        """
        Return whether this value is greater than another value.

        :param other: The value to compare with.
        :return: ``True`` if this value is greater than ``other``, otherwise
            ``False``.
        """
        ...
