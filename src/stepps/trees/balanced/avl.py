from stepps.trees.binary_tree import BinaryTree


class AVL[T]:
    """
    Define the interface for balancing a binary tree.
    """

    def balance(self, tree: BinaryTree[T]) -> BinaryTree[T]:
        """
        Balance the given tree using AVL rotations.

        :param tree: The tree to balance.
        :return: The balanced tree.
        """
        raise NotImplementedError
