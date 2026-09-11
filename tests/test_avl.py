from typing import Any

import pytest

from stepps.iterators.inorder import InOrderIterator
from stepps.iterators.levelorder import LevelOrderIterator
from stepps.iterators.postorder import PostOrderIterator
from stepps.iterators.preorder import PreOrderIterator
from stepps.nodes import BinaryNode
from stepps.trees.avl_impl import AVLImpl


@pytest.fixture
def avl_tree() -> AVLImpl[Any]:
    tree: AVLImpl[Any] = AVLImpl()

    for value in [50, 30, 70, 20, 40, 60, 80]:
        tree.insert(value)

    return tree


def check_balanced(tree: AVLImpl[Any]) -> None:
    def check(node: BinaryNode[int] | None) -> int:
        if node is None:
            return -1

        left_height = check(node.left)
        right_height = check(node.right)

        assert abs(left_height - right_height) <= 1

        return 1 + max(left_height, right_height)

    check(tree.root)


def test_empty_tree() -> None:
    tree: AVLImpl[Any] = AVLImpl()

    assert tree.is_empty()
    assert tree.size() == 0
    assert tree.height() == -1
    assert tree.min() is None
    assert tree.max() is None
    assert tree.root is None


def test_insert_and_size() -> None:
    tree: AVLImpl[Any] = AVLImpl()

    tree.insert(50)
    tree.insert(30)
    tree.insert(70)

    assert tree.size() == 3
    assert not tree.is_empty()
    assert tree.root is not None
    assert tree.root.value == 50


def test_duplicate_insert() -> None:
    tree: AVLImpl[Any] = AVLImpl()

    first = tree.insert(50)
    second = tree.insert(50)

    assert first is second
    assert tree.size() == 1
    assert tree.root is first


def test_find() -> None:
    tree: AVLImpl[Any] = AVLImpl()

    for value in [50, 30, 70]:
        tree.insert(value)

    node = tree.find(30)

    assert node is not None
    assert node.value == 30
    assert tree.find(100) is None


def test_contains() -> None:
    tree: AVLImpl[Any] = AVLImpl()

    for value in [50, 30, 70]:
        tree.insert(value)

    assert tree.contains(30)
    assert 30 in tree
    assert not tree.contains(100)
    assert 100 not in tree


def test_minimum_and_maximum(avl_tree: AVLImpl[Any]) -> None:
    minimum = avl_tree.minimum()
    maximum = avl_tree.maximum()

    assert minimum is not None
    assert minimum.value == 20

    assert maximum is not None
    assert maximum.value == 80


def test_min_and_max(avl_tree: AVLImpl[Any]) -> None:
    minimum = avl_tree.min()
    maximum = avl_tree.max()

    assert minimum is not None
    assert minimum.value == 20

    assert maximum is not None
    assert maximum.value == 80


def test_height(avl_tree: AVLImpl[Any]) -> None:
    assert avl_tree.height() == 2


def test_leaf_count(avl_tree: AVLImpl[Any]) -> None:
    assert avl_tree.count_leaves() == 4


def test_internal_node_count(avl_tree: AVLImpl[Any]) -> None:
    assert avl_tree.count_internal_nodes() == 3


def test_inorder_traversal(avl_tree: AVLImpl[Any]) -> None:
    values = [node.value for node in InOrderIterator(avl_tree.root)]

    assert values == [20, 30, 40, 50, 60, 70, 80]


def test_preorder_traversal(avl_tree: AVLImpl[Any]) -> None:
    values = [node.value for node in PreOrderIterator(avl_tree.root)]

    assert values == [50, 30, 20, 40, 70, 60, 80]


def test_postorder_traversal(avl_tree: AVLImpl[Any]) -> None:
    values = [node.value for node in PostOrderIterator(avl_tree.root)]

    assert values == [20, 40, 30, 60, 80, 70, 50]


def test_levelorder_traversal(avl_tree: AVLImpl[Any]) -> None:
    values = [node.value for node in LevelOrderIterator(avl_tree.root)]

    assert values == [50, 30, 70, 20, 40, 60, 80]


def test_ll_rotation() -> None:
    tree: AVLImpl[Any] = AVLImpl()

    tree.insert(30)
    tree.insert(20)
    tree.insert(10)

    assert tree.root is not None
    assert tree.root.value == 20
    assert tree.root.left is not None
    assert tree.root.left.value == 10
    assert tree.root.right is not None
    assert tree.root.right.value == 30

    check_balanced(tree)


def test_rr_rotation() -> None:
    tree: AVLImpl[Any] = AVLImpl()

    tree.insert(10)
    tree.insert(20)
    tree.insert(30)

    assert tree.root is not None
    assert tree.root.value == 20
    assert tree.root.left is not None
    assert tree.root.left.value == 10
    assert tree.root.right is not None
    assert tree.root.right.value == 30

    check_balanced(tree)


def test_lr_rotation() -> None:
    tree: AVLImpl[Any] = AVLImpl()

    tree.insert(30)
    tree.insert(10)
    tree.insert(20)

    assert tree.root is not None
    assert tree.root.value == 20
    assert tree.root.left is not None
    assert tree.root.left.value == 10
    assert tree.root.right is not None
    assert tree.root.right.value == 30

    check_balanced(tree)


def test_rl_rotation() -> None:
    tree: AVLImpl[Any] = AVLImpl()

    tree.insert(10)
    tree.insert(30)
    tree.insert(20)

    assert tree.root is not None
    assert tree.root.value == 20
    assert tree.root.left is not None
    assert tree.root.left.value == 10
    assert tree.root.right is not None
    assert tree.root.right.value == 30

    check_balanced(tree)


def test_insert_keeps_tree_balanced() -> None:
    tree: AVLImpl[Any] = AVLImpl()

    for value in [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]:
        tree.insert(value)
        check_balanced(tree)


def test_delete_leaf() -> None:
    tree: AVLImpl[Any] = AVLImpl()

    for value in [50, 30, 70, 20, 40, 60, 80]:
        tree.insert(value)

    assert tree.delete(20)
    assert tree.size() == 6
    assert tree.find(20) is None

    check_balanced(tree)


def test_delete_node_with_one_child() -> None:
    tree: AVLImpl[Any] = AVLImpl()

    for value in [50, 30, 70, 20]:
        tree.insert(value)

    assert tree.delete(30)
    assert tree.size() == 3
    assert tree.find(30) is None

    check_balanced(tree)


def test_delete_node_with_two_children() -> None:
    tree: AVLImpl[Any] = AVLImpl()

    for value in [50, 30, 70, 20, 40, 60, 80]:
        tree.insert(value)

    assert tree.delete(30)
    assert tree.size() == 6
    assert tree.find(30) is None

    check_balanced(tree)

    values = [node.value for node in InOrderIterator(tree.root)]

    assert values == [20, 40, 50, 60, 70, 80]


def test_delete_root() -> None:
    tree: AVLImpl[Any] = AVLImpl()

    for value in [50, 30, 70]:
        tree.insert(value)

    assert tree.delete(50)
    assert tree.size() == 2
    assert tree.find(50) is None

    check_balanced(tree)


def test_delete_missing_value() -> None:
    tree: AVLImpl[Any] = AVLImpl()

    for value in [50, 30, 70]:
        tree.insert(value)

    assert not tree.delete(100)
    assert tree.size() == 3

    check_balanced(tree)


def test_delete_keeps_tree_balanced() -> None:
    tree: AVLImpl[Any] = AVLImpl()

    for value in [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]:
        tree.insert(value)

    for value in [80, 70, 60, 50]:
        assert tree.delete(value)
        check_balanced(tree)


def test_clear(avl_tree: AVLImpl[Any]) -> None:
    avl_tree.clear()

    assert avl_tree.is_empty()
    assert avl_tree.size() == 0
    assert avl_tree.root is None
    assert avl_tree.height() == -1
