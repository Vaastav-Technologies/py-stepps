from typing import Protocol

from stepps.tree_builder.tree_builder import TreeBuilder


class InOrderTreeBuilder[T](TreeBuilder[T], Protocol):
    """
    Define the interface for building a binary tree from a sequence
    using inorder traversal.
    """
