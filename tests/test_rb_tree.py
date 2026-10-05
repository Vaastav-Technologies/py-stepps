from stepps.iterators.levelorder import LevelOrderIterator
from stepps.nodes import BinaryNode
from stepps.trees.balanced.rb_tree.rb_node import RBNode
from stepps.trees.balanced.rb_tree.rb_node_impl import RBNodeImpl
from stepps.trees.balanced.rb_tree.red_black_impl import RedBlackImpl
from stepps.trees.binary_tree_impl import BinaryTreeImpl


def create_tree(root: RBNodeImpl[int], size: int) -> BinaryTreeImpl[int]:
    tree = BinaryTreeImpl[int](LevelOrderIterator)
    tree.root = root
    tree._size = size

    return tree


# =====================================================
# Helper Functions
# =====================================================


def as_rb(node: BinaryNode[int] | None) -> RBNodeImpl[int] | None:
    if node is None:
        return None

    assert isinstance(node, RBNodeImpl)
    return node


def assert_root_is_black(tree: BinaryTreeImpl[int]) -> None:
    root = tree.root

    assert root is not None
    assert isinstance(root, RBNodeImpl)
    assert root.color == RBNode.BLACK
    assert root.parent is None


def assert_no_red_red(node: BinaryNode[int] | None) -> None:
    rb = as_rb(node)

    if rb is None:
        return

    left = as_rb(rb.left)
    right = as_rb(rb.right)

    if rb.color == RBNode.RED:
        if left is not None:
            assert left.color == RBNode.BLACK

        if right is not None:
            assert right.color == RBNode.BLACK

    assert_no_red_red(left)
    assert_no_red_red(right)


def assert_parent_links(
    node: RBNodeImpl[int] | None,
    parent: RBNodeImpl[int] | None = None,
) -> None:
    if node is None:
        return

    assert node.parent is parent

    if node.left is not None:
        assert isinstance(node.left, RBNodeImpl)
        assert_parent_links(node.left, node)

    if node.right is not None:
        assert isinstance(node.right, RBNodeImpl)
        assert_parent_links(node.right, node)


def black_height(node: BinaryNode[int] | None) -> int:
    rb = as_rb(node)

    if rb is None:
        return 1

    left_height = black_height(rb.left)
    right_height = black_height(rb.right)

    assert left_height == right_height

    return left_height + (1 if rb.color == RBNode.BLACK else 0)


def assert_red_black_properties(tree: BinaryTreeImpl[int]) -> None:
    root = tree.root

    if root is None:
        return

    assert isinstance(root, RBNodeImpl)

    # Property 2: root is black.
    assert root.color == RBNode.BLACK

    # Root has no parent.
    assert root.parent is None

    # Property 4: red nodes cannot have red children.
    assert_no_red_red(root)

    # Property 5: equal black height.
    black_height(root)

    # Parent pointers are correct.
    assert_parent_links(root)


# =====================================================
# Basic Cases
# =====================================================


def test_empty_tree():
    tree = BinaryTreeImpl[int](LevelOrderIterator)
    rb = RedBlackImpl[int](tree)

    assert rb.is_empty()
    assert rb.size() == 0
    assert rb.get_root() is None


def test_single_node_tree():
    tree = BinaryTreeImpl[int](LevelOrderIterator)
    rb = RedBlackImpl[int](tree)

    rb.insert(10)

    assert rb.size() == 1
    assert rb.root is not None
    assert rb.root.value == 10
    assert rb.root.color == RBNode.BLACK
    assert rb.root.parent is None

    assert_red_black_properties(tree)


def test_insert_multiple_nodes():
    tree = BinaryTreeImpl[int](LevelOrderIterator)
    rb = RedBlackImpl[int](tree)

    for value in (20, 10, 30, 5, 15, 25, 35):
        rb.insert(value)

    assert rb.size() == 7

    for value in (5, 10, 15, 20, 25, 30, 35):
        assert rb.contains(value)

    assert_red_black_properties(tree)


# =====================================================
# Basic Insertion Rotation Cases
# =====================================================


def test_insert_ll_case():
    tree = BinaryTreeImpl[int](LevelOrderIterator)
    rb = RedBlackImpl[int](tree)

    rb.insert(30)
    rb.insert(20)
    rb.insert(10)

    assert rb.root is not None
    assert rb.root.value == 20

    assert rb.root.left is not None
    assert rb.root.left.value == 10

    assert rb.root.right is not None
    assert rb.root.right.value == 30

    assert rb.root.color == RBNode.BLACK
    assert rb.root.left.color == RBNode.RED
    assert rb.root.right.color == RBNode.RED

    assert_red_black_properties(tree)


def test_insert_rr_case():
    tree = BinaryTreeImpl[int](LevelOrderIterator)
    rb = RedBlackImpl[int](tree)

    rb.insert(10)
    rb.insert(20)
    rb.insert(30)

    assert rb.root is not None
    assert rb.root.value == 20

    assert rb.root.left is not None
    assert rb.root.left.value == 10

    assert rb.root.right is not None
    assert rb.root.right.value == 30

    assert rb.root.color == RBNode.BLACK
    assert rb.root.left.color == RBNode.RED
    assert rb.root.right.color == RBNode.RED

    assert_red_black_properties(tree)


def test_insert_lr_case():
    tree = BinaryTreeImpl[int](LevelOrderIterator)
    rb = RedBlackImpl[int](tree)

    rb.insert(30)
    rb.insert(10)
    rb.insert(20)

    assert rb.root is not None
    assert rb.root.value == 20

    assert rb.root.left is not None
    assert rb.root.left.value == 10

    assert rb.root.right is not None
    assert rb.root.right.value == 30

    assert_red_black_properties(tree)


def test_insert_rl_case():
    tree = BinaryTreeImpl[int](LevelOrderIterator)
    rb = RedBlackImpl[int](tree)

    rb.insert(10)
    rb.insert(30)
    rb.insert(20)

    assert rb.root is not None
    assert rb.root.value == 20

    assert rb.root.left is not None
    assert rb.root.left.value == 10

    assert rb.root.right is not None
    assert rb.root.right.value == 30

    assert_red_black_properties(tree)


# =====================================================
# Recoloring Cases
# =====================================================


def test_insert_causes_recoloring():
    tree = BinaryTreeImpl[int](LevelOrderIterator)
    rb = RedBlackImpl[int](tree)

    rb.insert(20)
    rb.insert(10)
    rb.insert(30)
    rb.insert(5)

    assert rb.root is not None
    assert rb.root.value == 20
    assert rb.root.color == RBNode.BLACK

    assert rb.root.left is not None
    assert rb.root.left.value == 10
    assert rb.root.left.color == RBNode.BLACK

    assert rb.root.right is not None
    assert rb.root.right.value == 30
    assert rb.root.right.color == RBNode.BLACK

    assert rb.root.left.left is not None
    assert rb.root.left.left.value == 5
    assert rb.root.left.left.color == RBNode.RED

    assert_red_black_properties(tree)


# =====================================================
# Parent Pointer Tests
# =====================================================


def test_parent_pointers_after_insertion():
    tree = BinaryTreeImpl[int](LevelOrderIterator)
    rb = RedBlackImpl[int](tree)

    for value in (50, 30, 70, 20, 40, 60, 80):
        rb.insert(value)

    assert rb.root is not None
    assert rb.root.parent is None

    assert_parent_links(rb.root)


def test_parent_pointers_after_rotations():
    tree = BinaryTreeImpl[int](LevelOrderIterator)
    rb = RedBlackImpl[int](tree)

    rb.insert(30)
    rb.insert(20)
    rb.insert(10)

    assert rb.root is not None
    assert rb.root.value == 20

    assert rb.root.left is not None
    assert rb.root.left.parent is rb.root

    assert rb.root.right is not None
    assert rb.root.right.parent is rb.root

    assert_parent_links(rb.root)


# =====================================================
# Tree Properties
# =====================================================


def test_root_is_always_black():
    tree = BinaryTreeImpl[int](LevelOrderIterator)
    rb = RedBlackImpl[int](tree)

    for value in (10, 20, 30, 15, 25, 5, 1, 50, 60):
        rb.insert(value)

        assert rb.root is not None
        assert rb.root.color == RBNode.BLACK
        assert rb.root.parent is None


def test_no_red_red_relationship():
    tree = BinaryTreeImpl[int](LevelOrderIterator)
    rb = RedBlackImpl[int](tree)

    for value in (50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45, 55, 65, 75, 90):
        rb.insert(value)

    assert rb.root is not None
    assert_no_red_red(rb.root)


def test_equal_black_height():
    tree = BinaryTreeImpl[int](LevelOrderIterator)
    rb = RedBlackImpl[int](tree)

    for value in (50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45, 55, 65, 75, 90):
        rb.insert(value)

    assert rb.root is not None
    black_height(rb.root)


# =====================================================
# Larger Trees
# =====================================================


def test_insert_left_heavy_tree():
    tree = BinaryTreeImpl[int](LevelOrderIterator)
    rb = RedBlackImpl[int](tree)

    values = (50, 40, 30, 20, 10, 5, 1)

    for value in values:
        rb.insert(value)

    assert rb.size() == len(values)

    for value in values:
        assert rb.contains(value)

    assert_red_black_properties(tree)


def test_insert_right_heavy_tree():
    tree = BinaryTreeImpl[int](LevelOrderIterator)
    rb = RedBlackImpl[int](tree)

    values = (10, 20, 30, 40, 50, 60, 70)

    for value in values:
        rb.insert(value)

    assert rb.size() == len(values)

    for value in values:
        assert rb.contains(value)

    assert_red_black_properties(tree)


def test_insert_complex_tree():
    tree = BinaryTreeImpl[int](LevelOrderIterator)
    rb = RedBlackImpl[int](tree)

    values = (50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45, 55, 65, 75, 90)

    for value in values:
        rb.insert(value)

    assert rb.size() == len(values)

    for value in values:
        assert rb.contains(value)

    assert_red_black_properties(tree)


# =====================================================
# Duplicate Values
# =====================================================


def test_insert_duplicate_value():
    tree = BinaryTreeImpl[int](LevelOrderIterator)
    rb = RedBlackImpl[int](tree)

    rb.insert(10)
    rb.insert(10)

    # Adjust this assertion if your RB implementation
    # intentionally permits duplicate values.
    assert rb.size() == 1
    assert rb.contains(10)

    assert_red_black_properties(tree)


# =====================================================
# Delete - Basic Cases
# =====================================================


def test_delete_from_empty_tree():
    tree = BinaryTreeImpl[int](LevelOrderIterator)
    rb = RedBlackImpl[int](tree)

    result = rb.delete(10)

    assert result is False
    assert rb.is_empty()
    assert rb.size() == 0


def test_delete_single_node():
    tree = BinaryTreeImpl[int](LevelOrderIterator)
    rb = RedBlackImpl[int](tree)

    rb.insert(10)

    result = rb.delete(10)

    assert result is True
    assert rb.is_empty()
    assert rb.size() == 0
    assert rb.root is None


def test_delete_leaf():
    tree = BinaryTreeImpl[int](LevelOrderIterator)
    rb = RedBlackImpl[int](tree)

    for value in (20, 10, 30):
        rb.insert(value)

    assert rb.delete(10) is True

    assert rb.size() == 2
    assert not rb.contains(10)
    assert rb.contains(20)
    assert rb.contains(30)

    assert_red_black_properties(tree)


def test_delete_node_with_one_child():
    tree = BinaryTreeImpl[int](LevelOrderIterator)
    rb = RedBlackImpl[int](tree)

    for value in (20, 10, 30, 5):
        rb.insert(value)

    assert rb.delete(10) is True

    assert rb.size() == 3
    assert not rb.contains(10)

    for value in (5, 20, 30):
        assert rb.contains(value)

    assert_red_black_properties(tree)


def test_delete_node_with_two_children():
    tree = BinaryTreeImpl[int](LevelOrderIterator)
    rb = RedBlackImpl[int](tree)

    for value in (20, 10, 30, 5, 15, 25, 35):
        rb.insert(value)

    assert rb.delete(20) is True

    assert rb.size() == 6
    assert not rb.contains(20)

    for value in (5, 10, 15, 25, 30, 35):
        assert rb.contains(value)

    assert_red_black_properties(tree)


# =====================================================
# Delete - Larger Trees
# =====================================================


def test_delete_multiple_values():
    tree = BinaryTreeImpl[int](LevelOrderIterator)
    rb = RedBlackImpl[int](tree)

    values = (50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45, 55, 65, 75, 90)

    for value in values:
        rb.insert(value)

    for value in (10, 25, 35, 45, 55):
        assert rb.delete(value) is True
        assert_red_black_properties(tree)

    remaining = set(values) - {10, 25, 35, 45, 55}

    assert rb.size() == len(remaining)

    for value in remaining:
        assert rb.contains(value)


def test_delete_root_repeatedly():
    tree = BinaryTreeImpl[int](LevelOrderIterator)
    rb = RedBlackImpl[int](tree)

    values = (50, 30, 70, 20, 40, 60, 80)

    for value in values:
        rb.insert(value)

    while not rb.is_empty():
        root = rb.get_root()

        assert root is not None

        assert rb.delete(root.value) is True

        if not rb.is_empty():
            assert_red_black_properties(tree)


# =====================================================
# Tree Object Preservation
# =====================================================


def test_operations_use_same_tree_object():
    tree = BinaryTreeImpl[int](LevelOrderIterator)
    rb = RedBlackImpl[int](tree)

    rb.insert(30)
    rb.insert(20)
    rb.insert(40)

    assert rb.balance() is tree
    assert rb.get_root() is tree.root


def test_size_is_preserved_after_insertions_and_deletions():
    tree = BinaryTreeImpl[int](LevelOrderIterator)
    rb = RedBlackImpl[int](tree)

    values = (50, 30, 70, 20, 40, 60, 80)

    for index, value in enumerate(values, start=1):
        rb.insert(value)
        assert rb.size() == index

    for index, value in enumerate(values, start=1):
        rb.delete(value)
        assert rb.size() == len(values) - index


# =====================================================
# Final Invariant Test
# =====================================================


def test_red_black_invariants_after_many_operations():
    tree = BinaryTreeImpl[int](LevelOrderIterator)
    rb = RedBlackImpl[int](tree)

    insert_values = (50, 25, 75, 10, 30, 60, 90, 5, 15, 27, 35, 55, 65, 85, 100)

    for value in insert_values:
        rb.insert(value)
        assert_red_black_properties(tree)

    delete_values = (5, 15, 25, 75, 90, 50, 30)

    for value in delete_values:
        assert rb.delete(value) is True
        assert_red_black_properties(tree)
