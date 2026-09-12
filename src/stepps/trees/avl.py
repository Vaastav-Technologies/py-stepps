from stepps.trees.bst import BST, Comparable


class AVL[T: Comparable](BST[T]):
    """
    Define the interface for AVL tree implementations.

    An AVL tree is a self-balancing binary search tree that maintains
    the balance property that the height difference between the left
    and right subtrees of every node is at most one.
    """
