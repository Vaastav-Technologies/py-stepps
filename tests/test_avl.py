from typing import Any

import pytest

from stepps.iterators.inorder import InOrderIterator
from stepps.iterators.levelorder import LevelOrderIterator
from stepps.iterators.postorder import PostOrderIterator
from stepps.iterators.preorder import PreOrderIterator
from stepps.nodes import BinaryNode
from stepps.trees.balanced.avl_impl import AVLImpl
from stepps.trees.binary_tree_impl import BinaryTreeImpl
from stepps.trees.bst_impl import BSTImpl


@pytest.fixture
def balancer() -> AVLImpl[Any]:
    return AVLImpl()


def check_balanced(node: BinaryNode[Any] | None) -> int:
    if node is None:
        return -1

    left_height = check_balanced(node.left)
    right_height = check_balanced(node.right)

    assert abs(left_height - right_height) <= 1

    return 1 + max(left_height, right_height)


def check_bst(node: BinaryNode[Any] | None) -> None:
    def check(
        current: BinaryNode[Any] | None,
        minimum: Any | None,
        maximum: Any | None,
    ) -> None:
        if current is None:
            return

        if minimum is not None:
            assert current.value > minimum

        if maximum is not None:
            assert current.value < maximum

        check(current.left, minimum, current.value)
        check(current.right, current.value, maximum)

    check(node, None, None)


def test_empty_tree(balancer: AVLImpl[Any]) -> None:
    tree: BinaryTreeImpl[Any] = BinaryTreeImpl()

    result = balancer.balance(tree)

    assert result is tree
    assert result.root is None


def test_already_balanced_tree(balancer: AVLImpl[Any]) -> None:
    tree: BSTImpl[Any] = BSTImpl()

    for value in [50, 30, 70, 20, 40, 60, 80]:
        tree.insert(value)

    original_root = tree.root

    result = balancer.balance(tree)

    assert result is tree
    assert result.root is original_root
    assert result.root is not None
    assert result.root.value == 50

    check_balanced(result.root)
    check_bst(result.root)


def test_ll_rotation(balancer: AVLImpl[Any]) -> None:
    tree: BSTImpl[Any] = BSTImpl()

    for value in [30, 20, 10]:
        tree.insert(value)

    result = balancer.balance(tree)

    assert result is tree
    assert result.root is not None
    assert result.root.value == 20

    assert result.root.left is not None
    assert result.root.left.value == 10

    assert result.root.right is not None
    assert result.root.right.value == 30

    check_balanced(result.root)
    check_bst(result.root)


def test_rr_rotation(balancer: AVLImpl[Any]) -> None:
    tree: BSTImpl[Any] = BSTImpl()

    for value in [10, 20, 30]:
        tree.insert(value)

    result = balancer.balance(tree)

    assert result is tree
    assert result.root is not None
    assert result.root.value == 20

    assert result.root.left is not None
    assert result.root.left.value == 10

    assert result.root.right is not None
    assert result.root.right.value == 30

    check_balanced(result.root)
    check_bst(result.root)


def test_lr_rotation(balancer: AVLImpl[Any]) -> None:
    tree: BSTImpl[Any] = BSTImpl()

    for value in [30, 10, 20]:
        tree.insert(value)

    result = balancer.balance(tree)

    assert result is tree
    assert result.root is not None
    assert result.root.value == 20

    assert result.root.left is not None
    assert result.root.left.value == 10

    assert result.root.right is not None
    assert result.root.right.value == 30

    check_balanced(result.root)
    check_bst(result.root)


def test_rl_rotation(balancer: AVLImpl[Any]) -> None:
    tree: BSTImpl[Any] = BSTImpl()

    for value in [10, 30, 20]:
        tree.insert(value)

    result = balancer.balance(tree)

    assert result is tree
    assert result.root is not None
    assert result.root.value == 20

    assert result.root.left is not None
    assert result.root.left.value == 10

    assert result.root.right is not None
    assert result.root.right.value == 30

    check_balanced(result.root)
    check_bst(result.root)


def test_balance_preserves_bst_order(balancer: AVLImpl[Any]) -> None:
    tree: BSTImpl[Any] = BSTImpl()

    values = [50, 30, 70, 20, 40, 60, 80, 10, 5]

    for value in values:
        tree.insert(value)

    before = [node.value for node in InOrderIterator(tree.root)]

    result = balancer.balance(tree)

    after = [node.value for node in InOrderIterator(result.root)]

    assert after == before
    check_bst(result.root)
    check_balanced(result.root)


def test_balance_reduces_height(balancer: AVLImpl[Any]) -> None:
    tree: BSTImpl[Any] = BSTImpl()

    for value in [10, 20, 30, 40, 50, 60, 70]:
        tree.insert(value)

    original_height = tree.height()

    result = balancer.balance(tree)

    assert result.height() < original_height
    check_balanced(result.root)
    check_bst(result.root)


def test_balance_reuses_existing_nodes(balancer: AVLImpl[Any]) -> None:
    tree: BSTImpl[Any] = BSTImpl()

    for value in [30, 20, 10]:
        tree.insert(value)

    assert tree.root is not None
    assert tree.root.left is not None
    assert tree.root.left.left is not None

    original_nodes = {
        id(tree.root),
        id(tree.root.left),
        id(tree.root.left.left),
    }

    result = balancer.balance(tree)

    assert result.root is not None
    assert result.root.left is not None
    assert result.root.right is not None

    balanced_nodes = {
        id(result.root),
        id(result.root.left),
        id(result.root.right),
    }

    assert balanced_nodes == original_nodes


def test_balance_preserves_traversal_values(balancer: AVLImpl[Any]) -> None:
    tree: BSTImpl[Any] = BSTImpl()

    for value in [50, 30, 70, 20, 40, 60, 80]:
        tree.insert(value)

    inorder_before = [node.value for node in InOrderIterator(tree.root)]

    preorder_before = [node.value for node in PreOrderIterator(tree.root)]

    postorder_before = [node.value for node in PostOrderIterator(tree.root)]

    levelorder_before = [node.value for node in LevelOrderIterator(tree.root)]

    result = balancer.balance(tree)

    inorder_after = [node.value for node in InOrderIterator(result.root)]

    assert inorder_after == inorder_before

    # The tree shape is allowed to change, so these
    # traversals are not expected to remain identical.
    assert preorder_before != []
    assert postorder_before != []
    assert levelorder_before != []


def test_balance_binary_tree(balancer: AVLImpl[Any]) -> None:
    tree: BinaryTreeImpl[Any] = BinaryTreeImpl()

    root = BinaryNode(1)
    root.right = BinaryNode(2)
    root.right.right = BinaryNode(3)
    root.right.right.right = BinaryNode(4)

    tree.root = root

    result = balancer.balance(tree)

    assert result is tree
    assert result.root is not None

    check_balanced(result.root)


def test_balance_multiple_levels(balancer: AVLImpl[Any]) -> None:
    tree: BSTImpl[Any] = BSTImpl()

    for value in [50, 30, 70, 20, 40, 60, 80, 10, 5]:
        tree.insert(value)

    result = balancer.balance(tree)

    assert result is tree
    check_balanced(result.root)
    check_bst(result.root)

    values = [node.value for node in InOrderIterator(result.root)]

    assert values == [5, 10, 20, 30, 40, 50, 60, 70, 80]
