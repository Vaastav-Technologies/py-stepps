import pytest

from stepps.iterators.levelorder import LevelOrderIterator
from stepps.nodes import BinaryNode
from stepps.trees.binary_tree_impl import BinaryTreeImpl


@pytest.fixture
def tree():
    tree = BinaryTreeImpl[int](LevelOrderIterator)

    root = BinaryNode(50)
    root.left = BinaryNode(30)
    root.right = BinaryNode(70)
    root.left.left = BinaryNode(20)
    root.left.right = BinaryNode(40)
    root.right.left = BinaryNode(60)
    root.right.right = BinaryNode(80)

    tree.root = root
    tree._size = 7

    return tree


# =====================================================
# Basic Properties
# =====================================================


def test_new_tree_is_empty():
    tree = BinaryTreeImpl[int](LevelOrderIterator)

    assert tree.is_empty()
    assert len(tree) == 0
    assert tree.size() == 0
    assert not tree


def test_size(tree):
    assert tree.size() == 7
    assert len(tree) == 7
    assert tree


def test_clear(tree):
    tree.clear()

    assert tree.is_empty()
    assert tree.size() == 0
    assert len(tree) == 0


# =====================================================
# Search
# =====================================================


def test_find_existing(tree):
    node = tree.find(40)

    assert node is not None
    assert node.value == 40


def test_find_missing(tree):
    assert tree.find(999) is None


def test_contains(tree):
    assert 60 in tree


def test_not_contains(tree):
    assert 100 not in tree


# =====================================================
# Tree Statistics
# =====================================================


def test_height(tree):
    assert tree.height() == 2


def test_empty_tree_height():
    tree = BinaryTreeImpl[int](LevelOrderIterator)

    assert tree.height() == -1


def test_leaf_count(tree):
    assert tree.count_leaves() == 4


def test_empty_tree_leaf_count():
    tree = BinaryTreeImpl[int](LevelOrderIterator)

    assert tree.count_leaves() == 0


def test_internal_nodes(tree):
    assert tree.count_internal_nodes() == 3


def test_empty_tree_internal_nodes():
    tree = BinaryTreeImpl[int](LevelOrderIterator)

    assert tree.count_internal_nodes() == 0


# =====================================================
# Tree Inversion
# =====================================================


def test_invert_tree(tree):
    tree.invert_tree()

    assert tree.root is not None
    assert tree.root.value == 50

    assert tree.root.left is not None
    assert tree.root.left.value == 70

    assert tree.root.right is not None
    assert tree.root.right.value == 30

    assert tree.root.left.left is not None
    assert tree.root.left.left.value == 80

    assert tree.root.left.right is not None
    assert tree.root.left.right.value == 60

    assert tree.root.right.left is not None
    assert tree.root.right.left.value == 40

    assert tree.root.right.right is not None
    assert tree.root.right.right.value == 20


def test_invert_empty_tree():
    tree = BinaryTreeImpl[int](LevelOrderIterator)

    tree.invert_tree()

    assert tree.is_empty()


def test_invert_single_node_tree():
    tree = BinaryTreeImpl[int](LevelOrderIterator)

    tree.root = BinaryNode(50)
    tree._size = 1

    tree.invert_tree()

    assert tree.root is not None
    assert tree.root.value == 50
    assert tree.root.left is None
    assert tree.root.right is None


# =====================================================
# Tree Access
# =====================================================


def test_get_root(tree):
    root = tree.get_root()

    assert root is tree.root
    assert root is not None
    assert root.value == 50


def test_get_root_empty_tree():
    tree = BinaryTreeImpl[int](LevelOrderIterator)

    assert tree.get_root() is None


def test_get_left_subtree(tree):
    subtree = tree.get_left_subtree()

    assert subtree is not tree
    assert subtree.get_root() is tree.root.left

    root = subtree.get_root()
    assert root is not None
    assert root.value == 30

    assert root.left is not None
    assert root.left.value == 20

    assert root.right is not None
    assert root.right.value == 40


def test_get_right_subtree(tree):
    subtree = tree.get_right_subtree()

    assert subtree is not tree
    assert subtree.get_root() is tree.root.right

    root = subtree.get_root()
    assert root is not None
    assert root.value == 70

    assert root.left is not None
    assert root.left.value == 60

    assert root.right is not None
    assert root.right.value == 80


def test_get_left_subtree_empty_tree():
    tree = BinaryTreeImpl[int](LevelOrderIterator)

    subtree = tree.get_left_subtree()

    assert subtree.is_empty()
    assert subtree.get_root() is None


def test_get_right_subtree_empty_tree():
    tree = BinaryTreeImpl[int](LevelOrderIterator)

    subtree = tree.get_right_subtree()

    assert subtree.is_empty()
    assert subtree.get_root() is None


def test_get_left_subtree_without_left_child():
    tree = BinaryTreeImpl[int](LevelOrderIterator)

    tree.root = BinaryNode(50)
    tree._size = 1

    subtree = tree.get_left_subtree()

    assert subtree.is_empty()
    assert subtree.get_root() is None


def test_get_right_subtree_without_right_child():
    tree = BinaryTreeImpl[int](LevelOrderIterator)

    tree.root = BinaryNode(50)
    tree._size = 1

    subtree = tree.get_right_subtree()

    assert subtree.is_empty()
    assert subtree.get_root() is None


# =====================================================
# Tree Rotations
# =====================================================


def test_right_rotate(tree):
    tree.root = BinaryNode(30)
    tree.root.left = BinaryNode(20)
    tree.root.left.left = BinaryNode(10)
    tree._size = 3

    result = tree.right_rotate()

    assert result is tree
    assert tree.root is not None
    assert tree.root.value == 20

    assert tree.root.left is not None
    assert tree.root.left.value == 10

    assert tree.root.right is not None
    assert tree.root.right.value == 30


def test_left_rotate(tree):
    tree.root = BinaryNode(10)
    tree.root.right = BinaryNode(20)
    tree.root.right.right = BinaryNode(30)
    tree._size = 3

    result = tree.left_rotate()

    assert result is tree
    assert tree.root is not None
    assert tree.root.value == 20

    assert tree.root.left is not None
    assert tree.root.left.value == 10

    assert tree.root.right is not None
    assert tree.root.right.value == 30


def test_right_rotate_with_middle_subtree():
    tree = BinaryTreeImpl[int](LevelOrderIterator)

    root = BinaryNode(30)
    root.left = BinaryNode(20)
    root.left.right = BinaryNode(25)

    tree.root = root
    tree._size = 3

    tree.right_rotate()

    assert tree.root is not None
    assert tree.root.value == 20

    assert tree.root.left is None

    assert tree.root.right is not None
    assert tree.root.right.value == 30

    assert tree.root.right.left is not None
    assert tree.root.right.left.value == 25


def test_left_rotate_with_middle_subtree():
    tree = BinaryTreeImpl[int](LevelOrderIterator)

    root = BinaryNode(10)
    root.right = BinaryNode(20)
    root.right.left = BinaryNode(15)

    tree.root = root
    tree._size = 3

    tree.left_rotate()

    assert tree.root is not None
    assert tree.root.value == 20

    assert tree.root.right is None

    assert tree.root.left is not None
    assert tree.root.left.value == 10

    assert tree.root.left.right is not None
    assert tree.root.left.right.value == 15


def test_right_rotate_empty_tree():
    tree = BinaryTreeImpl[int](LevelOrderIterator)

    result = tree.right_rotate()

    assert result is tree
    assert tree.root is None


def test_left_rotate_empty_tree():
    tree = BinaryTreeImpl[int](LevelOrderIterator)

    result = tree.left_rotate()

    assert result is tree
    assert tree.root is None


def test_right_rotate_without_left_child():
    tree = BinaryTreeImpl[int](LevelOrderIterator)

    tree.root = BinaryNode(30)
    tree._size = 1

    result = tree.right_rotate()

    assert result is tree
    assert tree.root is not None
    assert tree.root.value == 30


def test_left_rotate_without_right_child():
    tree = BinaryTreeImpl[int](LevelOrderIterator)

    tree.root = BinaryNode(30)
    tree._size = 1

    result = tree.left_rotate()

    assert result is tree
    assert tree.root is not None
    assert tree.root.value == 30


# =====================================================
# Tree Subtree Assignment
# =====================================================


def test_set_left_subtree(tree):
    subtree = BinaryTreeImpl[int](LevelOrderIterator)

    subtree.root = BinaryNode(30)
    subtree.root.left = BinaryNode(20)
    subtree.root.right = BinaryNode(40)
    subtree._size = 3

    tree._set_left_subtree(subtree)

    assert tree.root is not None
    assert tree.root.left is subtree.root
    assert tree.root.left.value == 30

    assert tree.root.left.left is not None
    assert tree.root.left.left.value == 20

    assert tree.root.left.right is not None
    assert tree.root.left.right.value == 40


def test_set_right_subtree(tree):
    subtree = BinaryTreeImpl[int](LevelOrderIterator)

    subtree.root = BinaryNode(70)
    subtree.root.left = BinaryNode(60)
    subtree.root.right = BinaryNode(80)
    subtree._size = 3

    tree._set_right_subtree(subtree)

    assert tree.root is not None
    assert tree.root.right is subtree.root
    assert tree.root.right.value == 70

    assert tree.root.right.left is not None
    assert tree.root.right.left.value == 60

    assert tree.root.right.right is not None
    assert tree.root.right.right.value == 80


def test_right_rotate_nested_subtree():
    tree = BinaryTreeImpl[int](LevelOrderIterator)

    root = BinaryNode(100)
    root.left = BinaryNode(50)
    root.left.left = BinaryNode(30)
    root.left.left.left = BinaryNode(20)

    tree.root = root
    tree._size = 4

    subtree = tree.get_left_subtree()
    subtree.right_rotate()
    tree._set_left_subtree(subtree)

    assert tree.root is not None
    assert tree.root.value == 100

    assert tree.root.left is not None
    assert tree.root.left.value == 30

    assert tree.root.left.left is not None
    assert tree.root.left.left.value == 20

    assert tree.root.left.right is not None
    assert tree.root.left.right.value == 50
