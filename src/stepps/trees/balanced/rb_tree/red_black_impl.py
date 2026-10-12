from typing import Any, cast, override

from stepps.comparable import Comparable
from stepps.nodes import BinaryNode
from stepps.trees.balanced.rb_tree.rb_node import RBNode
from stepps.trees.balanced.rb_tree.rb_node_impl import RBNodeImpl
from stepps.trees.balanced.rb_tree.red_black import RedBlack
from stepps.trees.binary_tree import BinaryTree
from stepps.trees.bst_impl import BSTImpl


class RedBlackImpl[T: Comparable](RedBlack[T], BSTImpl[T]):
    """
    Provide the default implementation of a Red-Black tree.
    """

    def __init__(self, tree: BinaryTree[T]) -> None:
        self.tree = tree
        self.root: RBNode[T] | None = None
        self._initialize_tree()

    @override
    def balance(self) -> BinaryTree[T]:
        """
        Balance the tree using Red-Black tree rules.

        :return: The balanced tree.
        """
        if self.root is None:
            return self.tree

        self._insert_fixup(self.root)
        self.root.color = RBNode.BLACK
        self._set_tree_root(self.root)
        return self.tree

    def insert(self, value: T) -> BinaryNode[T]:
        """
        Insert a value into the Red-Black tree.

        :param value: The value to insert.
        :return: The inserted node.
        """
        new_node = RBNodeImpl(value)

        if self.root is None:
            new_node.color = RBNode.BLACK
            self.root = new_node
            self._set_tree_root(new_node)
            self._increment_size()
            return new_node

        parent: RBNode[T] | None = None
        current: RBNode[T] | None = self.root

        while current is not None:
            parent = current

            if value < self._value_of(current):
                current = self._as_rb_node(current.left)
            elif value > self._value_of(current):
                current = self._as_rb_node(current.right)
            else:
                return current

        new_node.parent = parent

        if parent is not None:
            if value < self._value_of(parent):
                parent.left = new_node
            else:
                parent.right = new_node

        self._increment_size()
        self._insert_fixup(new_node)

        self.root = self._root_from(new_node)

        if self.root is not None:
            self.root.color = RBNode.BLACK

        self._set_tree_root(self.root)
        return new_node

    def delete(self, value: T) -> bool:
        """
        Delete a value from the Red-Black tree.

        :param value: The value to delete.
        :return: True if the value was deleted, otherwise False.
        """
        node = self._find_rb_node(value)

        if node is None:
            return False

        self._delete_node(node)
        self._decrement_size()

        if self.root is not None:
            self.root.color = RBNode.BLACK
            self._set_tree_root(self.root)

        return True

    def find(self, value: T) -> BinaryNode[T] | None:
        """
        Find a value in the tree.

        :param value: The value to search for.
        :return: The matching node, or None if not found.
        """
        return self._find_rb_node(value)

    def contains(self, value: T) -> bool:
        """
        Return whether a value exists in the tree.

        :param value: The value to search for.
        :return: True if the value exists, otherwise False.
        """
        return self._find_rb_node(value) is not None

    def __contains__(self, value: T) -> bool:
        return self.contains(value)

    def height(self) -> int:
        """
        Return the height of the tree.

        :return: The tree height.
        """
        return self.tree.height()

    def count_leaves(self) -> int:
        """
        Count the leaf nodes in the tree.

        :return: The number of leaf nodes.
        """
        return self.tree.count_leaves()

    def count_internal_nodes(self) -> int:
        """
        Count the internal nodes in the tree.

        :return: The number of internal nodes.
        """
        return self.tree.count_internal_nodes()

    def get_root(self) -> BinaryNode[T] | None:
        """
        Return the root node.

        :return: The root node, or None if the tree is empty.
        """
        return self.tree.get_root()

    def get_left_subtree(self) -> BinaryTree[T]:
        """
        Return the left subtree.

        :return: The left subtree.
        """
        return self.tree.get_left_subtree()

    def get_right_subtree(self) -> BinaryTree[T]:
        """
        Return the right subtree.

        :return: The right subtree.
        """
        return self.tree.get_right_subtree()

    def _set_left_subtree(self, subtree: BinaryTree[T]) -> None:
        """
        Set the left subtree.

        :param subtree: The tree to use as the left subtree.
        """
        self.tree._set_left_subtree(subtree)

    def _set_right_subtree(self, subtree: BinaryTree[T]) -> None:
        """
        Set the right subtree.

        :param subtree: The tree to use as the right subtree.
        """
        self.tree._set_right_subtree(subtree)

    def right_rotate(self) -> BinaryTree[T]:
        """
        Perform a right rotation.

        :return: The tree after the rotation.
        """
        if self.root is None:
            return self.tree

        self._right_rotate(self.root)
        self._set_tree_root(self.root)
        return self.tree

    def left_rotate(self) -> BinaryTree[T]:
        """
        Perform a left rotation.

        :return: The tree after the rotation.
        """
        if self.root is None:
            return self.tree

        self._left_rotate(self.root)
        self._set_tree_root(self.root)
        return self.tree

    def invert_tree(self) -> None:
        """
        Invert the tree.
        """
        self.tree.invert_tree()

    def is_empty(self) -> bool:
        """
        Return whether the tree is empty.

        :return: True if the tree is empty, otherwise False.
        """
        return self.tree.is_empty()

    def clear(self) -> None:
        """
        Clear the tree.
        """
        self.tree.clear()
        self.root = None

    def size(self) -> int:
        """
        Return the number of nodes in the tree.

        :return: The tree size.
        """
        return self.tree.size()

    def __len__(self) -> int:
        return len(self.tree)

    def __bool__(self) -> bool:
        return bool(self.tree)

    def _initialize_tree(self) -> None:
        """
        Initialize the Red-Black tree from the supplied binary tree.
        """
        root = self.tree.get_root()

        if root is None:
            return

        if isinstance(root, RBNodeImpl):
            self.root = cast(RBNode[T], root)
            self._repair_parent_links(self.root)
            self.root.color = RBNode.BLACK
            self._set_tree_root(self.root)
            return

        values = self._collect_values(root)
        self.tree.clear()

        for value in values:
            self.insert(value)

    def _collect_values(self, node: BinaryNode[T] | None) -> list[T]:
        """
        Collect values from an existing binary tree.

        :param node: The root node.
        :return: The values contained in the tree.
        """
        if node is None:
            return []

        if node.value is None:
            raise ValueError("RB node value cannot be None")

        values = [node.value]
        values.extend(self._collect_values(node.left))
        values.extend(self._collect_values(node.right))
        return values

    def _repair_parent_links(self, node: RBNode[T] | None) -> None:
        """
        Repair parent links throughout an existing RB tree.

        :param node: The subtree root.
        """
        if node is None:
            return

        left = self._as_rb_node(node.left)
        right = self._as_rb_node(node.right)

        if left is not None:
            left.parent = node
            self._repair_parent_links(left)

        if right is not None:
            right.parent = node
            self._repair_parent_links(right)

    def _insert_fixup(self, node: RBNode[T]) -> None:
        """
        Restore Red-Black properties after insertion.

        :param node: The newly inserted node.
        """
        current = node

        while True:
            parent = current.parent

            if parent is None or parent.color != RBNode.RED:
                break

            grandparent = parent.parent

            if grandparent is None:
                break

            if parent is grandparent.left:
                uncle = self._as_rb_node(grandparent.right)

                if self._color_of(uncle) == RBNode.RED:
                    parent.color = RBNode.BLACK

                    if uncle is not None:
                        uncle.color = RBNode.BLACK

                    grandparent.color = RBNode.RED
                    current = grandparent
                    continue

                if current is parent.right:
                    current = parent
                    self._left_rotate(current)
                    parent = current.parent

                    if parent is None:
                        break

                    grandparent = parent.parent

                    if grandparent is None:
                        break

                parent.color = RBNode.BLACK
                grandparent.color = RBNode.RED
                self._right_rotate(grandparent)

            else:
                uncle = self._as_rb_node(grandparent.left)

                if self._color_of(uncle) == RBNode.RED:
                    parent.color = RBNode.BLACK

                    if uncle is not None:
                        uncle.color = RBNode.BLACK

                    grandparent.color = RBNode.RED
                    current = grandparent
                    continue

                if current is parent.left:
                    current = parent
                    self._right_rotate(current)
                    parent = current.parent

                    if parent is None:
                        break

                    grandparent = parent.parent

                    if grandparent is None:
                        break

                parent.color = RBNode.BLACK
                grandparent.color = RBNode.RED
                self._left_rotate(grandparent)

        self.root = self._root_from(node)

        if self.root is not None:
            self.root.color = RBNode.BLACK

    def _delete_node(self, node: RBNode[T]) -> None:
        """
        Delete a node and restore Red-Black properties.

        :param node: The node to delete.
        """
        replacement: RBNode[T] | None
        replacement_parent: RBNode[T] | None
        original_color = node.color

        if node.left is None:
            replacement = self._as_rb_node(node.right)
            replacement_parent = node.parent
            self._transplant(node, replacement)

        elif node.right is None:
            replacement = self._as_rb_node(node.left)
            replacement_parent = node.parent
            self._transplant(node, replacement)

        else:
            successor = self._minimum(self._as_rb_node(node.right))

            if successor is None:
                return

            original_color = successor.color
            replacement = self._as_rb_node(successor.right)

            if successor.parent is node:
                replacement_parent = successor

                if replacement is not None:
                    replacement.parent = successor

            else:
                replacement_parent = successor.parent
                self._transplant(successor, replacement)
                successor.right = node.right

                successor_right = self._as_rb_node(successor.right)

                if successor_right is not None:
                    successor_right.parent = successor

            self._transplant(node, successor)
            successor.left = node.left

            successor_left = self._as_rb_node(successor.left)

            if successor_left is not None:
                successor_left.parent = successor

            successor.color = node.color

            if replacement is not None:
                replacement_parent = replacement.parent

        if original_color == RBNode.BLACK:
            self._delete_fixup(replacement, replacement_parent)

        if self.root is not None:
            new_root = self._root_from(self.root)

            if new_root is not None:
                self.root = new_root
                self.root.color = RBNode.BLACK
                self._set_tree_root(self.root)

    def _delete_fixup(
        self,
        node: RBNode[T] | None,
        parent: RBNode[T] | None,
    ) -> None:
        """
        Restore Red-Black properties after deletion.

        :param node: The replacement node.
        :param parent: The parent of the replacement node.
        """
        current = node
        current_parent = parent

        while current is not self.root and self._color_of(current) == RBNode.BLACK:
            if current_parent is None:
                break

            if current is current_parent.left:
                sibling = self._as_rb_node(current_parent.right)

                if self._color_of(sibling) == RBNode.RED:
                    if sibling is not None:
                        sibling.color = RBNode.BLACK

                    current_parent.color = RBNode.RED
                    self._left_rotate(current_parent)
                    sibling = self._as_rb_node(current_parent.right)

                sibling_left = (
                    self._as_rb_node(sibling.left) if sibling is not None else None
                )

                sibling_right = (
                    self._as_rb_node(sibling.right) if sibling is not None else None
                )

                if (
                    self._color_of(sibling_left) == RBNode.BLACK
                    and self._color_of(sibling_right) == RBNode.BLACK
                ):
                    if sibling is not None:
                        sibling.color = RBNode.RED

                    current = current_parent
                    current_parent = cast(
                        RBNode[T] | None,
                        current.parent,
                    )

                else:
                    if self._color_of(sibling_right) == RBNode.BLACK:
                        if sibling_left is not None:
                            sibling_left.color = RBNode.BLACK

                        if sibling is not None:
                            sibling.color = RBNode.RED
                            self._right_rotate(sibling)

                        sibling = self._as_rb_node(
                            current_parent.right,
                        )

                    if sibling is not None:
                        sibling.color = current_parent.color

                    current_parent.color = RBNode.BLACK

                    sibling_right = (
                        self._as_rb_node(sibling.right) if sibling is not None else None
                    )

                    if sibling_right is not None:
                        sibling_right.color = RBNode.BLACK

                    self._left_rotate(current_parent)

                    current = self.root
                    current_parent = None

            else:
                sibling = self._as_rb_node(current_parent.left)

                if self._color_of(sibling) == RBNode.RED:
                    if sibling is not None:
                        sibling.color = RBNode.BLACK

                    current_parent.color = RBNode.RED
                    self._right_rotate(current_parent)
                    sibling = self._as_rb_node(current_parent.left)

                sibling_left = (
                    self._as_rb_node(sibling.left) if sibling is not None else None
                )

                sibling_right = (
                    self._as_rb_node(sibling.right) if sibling is not None else None
                )

                if (
                    self._color_of(sibling_left) == RBNode.BLACK
                    and self._color_of(sibling_right) == RBNode.BLACK
                ):
                    if sibling is not None:
                        sibling.color = RBNode.RED

                    current = current_parent
                    current_parent = cast(
                        RBNode[T] | None,
                        current.parent,
                    )

                else:
                    if self._color_of(sibling_left) == RBNode.BLACK:
                        if sibling_right is not None:
                            sibling_right.color = RBNode.BLACK

                        if sibling is not None:
                            sibling.color = RBNode.RED
                            self._left_rotate(sibling)

                        sibling = self._as_rb_node(
                            current_parent.left,
                        )

                    if sibling is not None:
                        sibling.color = current_parent.color

                    current_parent.color = RBNode.BLACK

                    sibling_left = (
                        self._as_rb_node(sibling.left) if sibling is not None else None
                    )

                    if sibling_left is not None:
                        sibling_left.color = RBNode.BLACK

                    self._right_rotate(current_parent)

                    current = self.root
                    current_parent = None

        if current is not None:
            current.color = RBNode.BLACK

        self.root = self._root_from(
            current if current is not None else current_parent,
        )

        if self.root is not None:
            self.root.color = RBNode.BLACK
            self._set_tree_root(self.root)

    def _left_rotate(self, node: RBNode[T]) -> None:
        """
        Perform a Red-Black left rotation.

        :param node: The node to rotate around.
        """
        right = self._as_rb_node(node.right)

        if right is None:
            return

        node.right = right.left

        right_left = self._as_rb_node(right.left)

        if right_left is not None:
            right_left.parent = node

        right.parent = node.parent

        if node.parent is None:
            self.root = right
        elif node is node.parent.left:
            node.parent.left = right
        else:
            node.parent.right = right

        right.left = node
        node.parent = right
        self._set_tree_root(self.root)

    def _right_rotate(self, node: RBNode[T]) -> None:
        """
        Perform a Red-Black right rotation.

        :param node: The node to rotate around.
        """
        left = self._as_rb_node(node.left)

        if left is None:
            return

        node.left = left.right

        left_right = self._as_rb_node(left.right)

        if left_right is not None:
            left_right.parent = node

        left.parent = node.parent

        if node.parent is None:
            self.root = left
        elif node is node.parent.right:
            node.parent.right = left
        else:
            node.parent.left = left

        left.right = node
        node.parent = left
        self._set_tree_root(self.root)

    def _transplant(
        self,
        old_node: RBNode[T],
        new_node: RBNode[T] | None,
    ) -> None:
        """
        Replace one subtree with another.

        :param old_node: The root of the subtree being replaced.
        :param new_node: The replacement subtree root.
        """
        parent = old_node.parent

        if parent is None:
            self.root = new_node
        elif old_node is parent.left:
            parent.left = new_node
        else:
            parent.right = new_node

        if new_node is not None:
            new_node.parent = parent

        self._set_tree_root(self.root)

    def _minimum(
        self,
        node: RBNode[T] | None,
    ) -> RBNode[T] | None:
        """
        Return the minimum node in a subtree.

        :param node: The subtree root.
        :return: The minimum node.
        """
        current = node

        while current is not None:
            left = self._as_rb_node(current.left)

            if left is None:
                break

            current = left

        return current

    def _find_rb_node(self, value: T) -> RBNode[T] | None:
        """
        Find a node using Red-Black ordering.

        :param value: The value to search for.
        :return: The matching node, or None.
        """
        current: RBNode[T] | None = self.root

        while current is not None:
            if value == self._value_of(current):
                return current

            if value < self._value_of(current):
                current = self._as_rb_node(current.left)
            else:
                current = self._as_rb_node(current.right)

        return None

    def _color_of(self, node: RBNode[T] | None) -> int:
        """
        Return the color of a node.

        Missing children are treated as black.

        :param node: The node.
        :return: The node color.
        """
        if node is None:
            return RBNode.BLACK

        return node.color

    def _value_of(self, node: RBNode[T]) -> T:
        """
        Return the value of an RB node.

        """
        value = node.value

        if value is None:
            raise ValueError("RB node value cannot be None")

        return value

    def _as_rb_node(
        self,
        node: BinaryNode[T] | None,
    ) -> RBNode[T] | None:
        """
        Treat a binary node as an RB node.

        :param node: The binary node.
        :return: The RB node, or None.
        """
        if node is None:
            return None

        if not isinstance(node, RBNodeImpl):
            raise TypeError("Expected an RBNode")

        return cast(RBNode[T], node)

    def _root_from(
        self,
        node: RBNode[T] | None,
    ) -> RBNode[T] | None:
        """
        Find the root of the tree from a node.

        :param node: Any RB node in the tree.
        :return: The root node.
        """
        current = node

        while current is not None and current.parent is not None:
            current = current.parent

        return current

    def _set_tree_root(self, root: RBNode[T] | None) -> None:
        """
        Synchronize the supplied BinaryTree's root with the RB root.

        :param root: The new root node.
        """
        cast(Any, self.tree).root = root

    def _increment_size(self) -> None:
        """
        Increment the underlying tree size.
        """
        tree = cast(Any, self.tree)
        tree._size += 1

    def _decrement_size(self) -> None:
        """
        Decrement the underlying tree size.
        """
        tree = cast(Any, self.tree)
        tree._size -= 1
