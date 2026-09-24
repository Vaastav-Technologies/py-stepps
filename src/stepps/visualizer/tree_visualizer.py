from abc import abstractmethod
from typing import Protocol


class TreeVisualizer[T](Protocol):
    """
    Define the interface for tree visualization.
    """

    @abstractmethod
    def treevisualizer(self, tree: T) -> None:
        """
        Visualize a tree.

        :param tree: The tree to visualize.
        """
        ...
