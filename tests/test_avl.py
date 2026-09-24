from stepps.iterators.levelorder import LevelOrderIterator
from stepps.nodes import BinaryNode
from stepps.trees.balanced.avl_impl import AVLImpl
from stepps.trees.binary_tree_impl import BinaryTreeImpl


def create_tree(root: BinaryNode[int], size: int) -> BinaryTreeImpl[int]:
    tree = BinaryTreeImpl[int](LevelOrderIterator)
    tree.root = root
    tree._size = size

    return tree


# =====================================================
# Basic Cases
# =====================================================


def test_balance_empty_tree():
    tree = BinaryTreeImpl[int](LevelOrderIterator)
    avl = AVLImpl[int](tree)

    result = avl.balance()

    assert result is tree
    assert result.is_empty()
    assert result.size() == 0


def test_balance_single_node_tree():
    tree = create_tree(BinaryNode(10), 1)
    avl = AVLImpl[int](tree)

    result = avl.balance()

    assert result is tree
    assert result.root is not None
    assert result.root.value == 10
    assert result.root.left is None
    assert result.root.right is None
    assert result.size() == 1


def test_balance_already_balanced_tree():
    root = BinaryNode(20)
    root.left = BinaryNode(10)
    root.right = BinaryNode(30)

    tree = create_tree(root, 3)
    avl = AVLImpl[int](tree)

    result = avl.balance()

    assert result is tree
    assert result.root is not None
    assert result.root.value == 20

    assert result.root.left is not None
    assert result.root.left.value == 10

    assert result.root.right is not None
    assert result.root.right.value == 30


# =====================================================
# Basic AVL Rotation Cases
# =====================================================


def test_balance_ll_case():
    root = BinaryNode(30)
    root.left = BinaryNode(20)
    root.left.left = BinaryNode(10)

    tree = create_tree(root, 3)
    avl = AVLImpl[int](tree)

    result = avl.balance()

    assert result.root is not None
    assert result.root.value == 20

    assert result.root.left is not None
    assert result.root.left.value == 10

    assert result.root.right is not None
    assert result.root.right.value == 30


def test_balance_rr_case():
    root = BinaryNode(10)
    root.right = BinaryNode(20)
    root.right.right = BinaryNode(30)

    tree = create_tree(root, 3)
    avl = AVLImpl[int](tree)

    result = avl.balance()

    assert result.root is not None
    assert result.root.value == 20

    assert result.root.left is not None
    assert result.root.left.value == 10

    assert result.root.right is not None
    assert result.root.right.value == 30


def test_balance_lr_case():
    root = BinaryNode(30)
    root.left = BinaryNode(10)
    root.left.right = BinaryNode(20)

    tree = create_tree(root, 3)
    avl = AVLImpl[int](tree)

    result = avl.balance()

    assert result.root is not None
    assert result.root.value == 20

    assert result.root.left is not None
    assert result.root.left.value == 10

    assert result.root.right is not None
    assert result.root.right.value == 30


def test_balance_rl_case():
    root = BinaryNode(10)
    root.right = BinaryNode(30)
    root.right.left = BinaryNode(20)

    tree = create_tree(root, 3)
    avl = AVLImpl[int](tree)

    result = avl.balance()

    assert result.root is not None
    assert result.root.value == 20

    assert result.root.left is not None
    assert result.root.left.value == 10

    assert result.root.right is not None
    assert result.root.right.value == 30


# =====================================================
# Nested Subtree Cases
# =====================================================


def test_balance_ll_case_in_left_subtree():
    root = BinaryNode(100)
    root.left = BinaryNode(50)
    root.left.left = BinaryNode(30)
    root.left.left.left = BinaryNode(20)

    tree = create_tree(root, 4)
    avl = AVLImpl[int](tree)

    result = avl.balance()

    assert result.root is not None
    assert result.root.value == 30

    assert result.root.left is not None
    assert result.root.left.value == 20

    assert result.root.right is not None
    assert result.root.right.value == 100

    assert result.root.right.left is not None
    assert result.root.right.left.value == 50


def test_balance_rr_case_in_right_subtree():
    root = BinaryNode(100)
    root.right = BinaryNode(150)
    root.right.right = BinaryNode(170)
    root.right.right.right = BinaryNode(180)

    tree = create_tree(root, 4)
    avl = AVLImpl[int](tree)

    result = avl.balance()

    assert result.root is not None
    assert result.root.value == 170

    assert result.root.left is not None
    assert result.root.left.value == 100

    assert result.root.left.right is not None
    assert result.root.left.right.value == 150

    assert result.root.right is not None
    assert result.root.right.value == 180


def test_balance_lr_case_in_left_subtree():
    root = BinaryNode(100)
    root.left = BinaryNode(50)
    root.left.left = BinaryNode(30)
    root.left.left.right = BinaryNode(40)

    tree = create_tree(root, 4)
    avl = AVLImpl[int](tree)

    result = avl.balance()

    assert result.root is not None
    assert result.root.value == 40

    assert result.root.left is not None
    assert result.root.left.value == 30

    assert result.root.right is not None
    assert result.root.right.value == 100

    assert result.root.right.left is not None
    assert result.root.right.left.value == 50


def test_balance_rl_case_in_right_subtree():
    root = BinaryNode(100)
    root.right = BinaryNode(150)
    root.right.right = BinaryNode(170)
    root.right.right.left = BinaryNode(160)

    tree = create_tree(root, 4)
    avl = AVLImpl[int](tree)

    result = avl.balance()

    assert result.root is not None
    assert result.root.value == 160

    assert result.root.left is not None
    assert result.root.left.value == 100

    assert result.root.left.right is not None
    assert result.root.left.right.value == 150

    assert result.root.right is not None
    assert result.root.right.value == 170


# =====================================================
# Larger Trees
# =====================================================


def test_balance_left_heavy_tree():
    root = BinaryNode(50)

    root.left = BinaryNode(30)
    root.left.left = BinaryNode(20)
    root.left.left.left = BinaryNode(10)
    root.left.right = BinaryNode(40)

    root.right = BinaryNode(70)
    root.right.left = BinaryNode(60)
    root.right.right = BinaryNode(80)

    tree = create_tree(root, 8)
    avl = AVLImpl[int](tree)

    result = avl.balance()

    assert result.root is not None
    assert result.height() <= 3
    assert result.size() == 8

    for value in (10, 20, 30, 40, 50, 60, 70, 80):
        assert result.contains(value)


def test_balance_right_heavy_tree():
    root = BinaryNode(50)

    root.left = BinaryNode(30)
    root.left.left = BinaryNode(20)
    root.left.right = BinaryNode(40)

    root.right = BinaryNode(70)
    root.right.right = BinaryNode(80)
    root.right.right.right = BinaryNode(90)

    tree = create_tree(root, 7)
    avl = AVLImpl[int](tree)

    result = avl.balance()

    assert result.root is not None
    assert result.height() <= 3
    assert result.size() == 7

    for value in (20, 30, 40, 50, 70, 80, 90):
        assert result.contains(value)


def test_balance_complex_tree():
    root = BinaryNode(50)

    root.left = BinaryNode(30)
    root.left.left = BinaryNode(20)
    root.left.right = BinaryNode(40)
    root.left.left.left = BinaryNode(10)

    root.right = BinaryNode(70)
    root.right.right = BinaryNode(80)
    root.right.right.right = BinaryNode(90)

    tree = create_tree(root, 8)
    avl = AVLImpl[int](tree)

    result = avl.balance()

    assert result.root is not None
    assert result.height() <= 3
    assert result.size() == 8

    for value in (10, 20, 30, 40, 50, 70, 80, 90):
        assert result.contains(value)


# =====================================================
# Tree Structure Preservation
# =====================================================


def test_balance_preserves_all_nodes():
    root = BinaryNode(50)

    root.left = BinaryNode(30)
    root.left.left = BinaryNode(20)
    root.left.right = BinaryNode(40)

    root.right = BinaryNode(70)
    root.right.left = BinaryNode(60)
    root.right.right = BinaryNode(80)

    tree = create_tree(root, 7)
    avl = AVLImpl[int](tree)

    result = avl.balance()

    assert result.size() == 7

    for value in (20, 30, 40, 50, 60, 70, 80):
        assert result.contains(value)


def test_balance_returns_same_tree_object():
    root = BinaryNode(30)
    root.left = BinaryNode(20)
    root.left.left = BinaryNode(10)

    tree = create_tree(root, 3)
    avl = AVLImpl[int](tree)

    result = avl.balance()

    assert result is tree
