from random import Random

import pytest

from stepps.iterators.inorder import InOrderIterator
from stepps.iterators.levelorder import LevelOrderIterator
from stepps.nodes import BinaryNode
from stepps.nodes.impl.binary_node_impl import BinaryNodeImpl
from stepps.trees.balanced.rb_tree.rb_node import RBNode
from stepps.trees.balanced.rb_tree.rb_node_impl import RBNodeImpl
from stepps.trees.balanced.rb_tree.red_black_impl import RedBlackImpl
from stepps.trees.binary_tree_impl import BinaryTreeImpl
from stepps.trees.bst_impl import BSTImpl


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
        assert tree.size() == len(tree) == 0
        return

    seen: set[int] = set()
    stack: list[tuple[BinaryNode[int], int | None, int | None]] = [(root, None, None)]
    while stack:
        node, lower, upper = stack.pop()
        assert id(node) not in seen, "Cycle or shared child node"
        seen.add(id(node))
        assert isinstance(node, RBNodeImpl)
        assert node.color in (RBNode.RED, RBNode.BLACK), "Invalid node color"
        value = node.value
        assert value is not None
        assert lower is None or lower < value, "BST lower bound violated"
        assert upper is None or value < upper, "BST upper bound violated"
        if node.right is not None:
            stack.append((node.right, value, upper))
        if node.left is not None:
            stack.append((node.left, lower, value))

    assert tree.size() == len(tree) == len(seen), "Node count disagrees with size"
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


# =====================================================
# Delete - Fix-Up Cases
# =====================================================


@pytest.mark.parametrize("side", ["left", "right"])
@pytest.mark.parametrize(
    "case", ["red_sibling", "black_children", "near_red", "far_red"]
)
def test_delete_black_leaf_fixup(case, side):
    """
    Check each deletion fix-up case with a left or right missing replacement.
    """
    sign = 1 if side == "left" else -1

    def node(value, color):
        result = RBNodeImpl(value * sign)
        result.color = color
        return result

    def attach(parent, near, far):
        if side == "left":
            parent.left, parent.right = near, far
        else:
            parent.right, parent.left = near, far

    root = node(10, RBNode.BLACK)
    leaf = node(5, RBNode.BLACK)
    sibling = node(20, RBNode.RED if case == "red_sibling" else RBNode.BLACK)
    attach(root, leaf, sibling)
    size = 3
    if case == "red_sibling":
        attach(sibling, node(15, RBNode.BLACK), node(25, RBNode.BLACK))
        size += 2
    elif case == "near_red":
        attach(sibling, node(15, RBNode.RED), None)
        size += 1
    elif case == "far_red":
        attach(sibling, None, node(25, RBNode.RED))
        size += 1

    tree = create_tree(root, size)
    rb = RedBlackImpl[int](tree)
    assert_red_black_properties(tree)
    expected = {n.value for n in InOrderIterator(tree.root)} - {leaf.value}

    assert rb.delete(5 * sign) is True

    assert_red_black_properties(tree)
    assert [n.value for n in InOrderIterator(tree.root)] == sorted(expected)
    expected_root = {
        "red_sibling": 20,
        "black_children": 10,
        "near_red": 15,
        "far_red": 20,
    }
    assert rb.root.value == expected_root[case] * sign
    assert rb.root is tree.root
    assert rb.size() == size - 1


def test_delete_missing_value_from_nonempty_tree():
    tree = BinaryTreeImpl[int](LevelOrderIterator)
    rb = RedBlackImpl[int](tree)
    for value in (20, 10, 30):
        rb.insert(value)
    nodes = list(InOrderIterator(tree.root))

    assert rb.delete(999) is False

    assert list(InOrderIterator(tree.root)) == nodes
    assert rb.root is tree.root
    assert_red_black_properties(tree)


@pytest.mark.parametrize("sign", [1, -1])
def test_delete_propagates_black_height_deficit_to_root(sign):
    """
    Check that deletion fix-up can recolor through more than one ancestor.
    """
    nodes = {value: RBNodeImpl(value * sign) for value in (20, 10, 30, 5, 15, 25, 35)}
    for node in nodes.values():
        node.color = RBNode.BLACK
    for parent, left, right in ((20, 10, 30), (10, 5, 15), (30, 25, 35)):
        if sign == 1:
            nodes[parent].left, nodes[parent].right = nodes[left], nodes[right]
        else:
            nodes[parent].right, nodes[parent].left = nodes[left], nodes[right]
    tree = create_tree(nodes[20], 7)
    rb = RedBlackImpl[int](tree)
    assert_red_black_properties(tree)

    assert rb.delete(5 * sign) is True

    assert_red_black_properties(tree)
    assert rb.root is nodes[20]
    assert nodes[15].color == nodes[30].color == RBNode.RED
    assert nodes[10].color == nodes[20].color == RBNode.BLACK
    assert [n.value for n in InOrderIterator(tree.root)] == sorted(
        value * sign for value in (20, 10, 30, 15, 25, 35)
    )


# =====================================================
# Balance - Public API
# =====================================================


@pytest.mark.parametrize("values", [(), (10,), (20, 10, 30, 5, 15, 25, 35)])
def test_balance_preserves_valid_tree(values):
    """
    Check that balancing a valid tree preserves nodes, values, and tree identity.
    """
    tree = BinaryTreeImpl[int](LevelOrderIterator)
    rb = RedBlackImpl[int](tree)
    for value in values:
        rb.insert(value)
    nodes = list(InOrderIterator(tree.root))

    assert rb.balance() is tree
    assert rb.balance() is tree

    assert list(InOrderIterator(tree.root)) == nodes
    assert rb.root is tree.root
    assert_red_black_properties(tree)


def test_balance_blackens_red_root():
    tree = BinaryTreeImpl[int](LevelOrderIterator)
    rb = RedBlackImpl[int](tree)
    rb.insert(10)
    rb.root.color = RBNode.RED

    assert rb.balance() is tree

    assert_red_black_properties(tree)


# =====================================================
# Initialization, Clear, and Mixed Mutations
# =====================================================


def test_initialize_from_plain_binary_tree():
    root = BinaryNodeImpl(30)
    root.left = BinaryNodeImpl(20)
    root.left.left = BinaryNodeImpl(10)
    tree = BinaryTreeImpl[int](LevelOrderIterator)
    tree.root = root
    tree._size = 3

    rb = RedBlackImpl[int](tree)

    assert rb.tree is tree
    assert rb.root is tree.root
    assert [n.value for n in InOrderIterator(tree.root)] == [10, 20, 30]
    assert_red_black_properties(tree)


def test_initialize_from_valid_rb_tree_repairs_parent_links():
    root = RBNodeImpl(20)
    root.color = RBNode.BLACK
    root.left = RBNodeImpl(10)
    root.right = RBNodeImpl(30)
    tree = create_tree(root, 3)

    rb = RedBlackImpl[int](tree)

    assert rb.root is root
    assert_red_black_properties(tree)


def test_clear_and_reuse():
    tree = BinaryTreeImpl[int](LevelOrderIterator)
    rb = RedBlackImpl[int](tree)
    for value in (20, 10, 30):
        rb.insert(value)
    rb.clear()
    rb.clear()

    assert rb.root is tree.root is None
    assert rb.is_empty() and not rb
    assert rb.find(20) is None
    assert rb.delete(20) is False
    assert rb.height() == -1
    assert rb.count_leaves() == rb.count_internal_nodes() == 0
    assert_red_black_properties(tree)

    rb.insert(40)
    assert rb.find(40) is rb.root
    assert 40 in rb
    assert rb.height() == 0
    assert rb.count_leaves() == 1
    assert rb.count_internal_nodes() == 0
    assert_red_black_properties(tree)


@pytest.mark.parametrize("seed", [0, 1, 2, 3, 4])
def test_randomized_insert_delete_sequences(seed):
    """
    Check ordering, node counts, and RB invariants after every seeded mutation.
    """
    random = Random(seed)
    tree = BinaryTreeImpl[int](LevelOrderIterator)
    rb = RedBlackImpl[int](tree)
    expected = set()
    for _ in range(300):
        value = random.randrange(60)
        if random.random() < 0.55:
            previous = rb.find(value)
            inserted = rb.insert(value)
            assert inserted.value == value
            if previous is not None:
                assert inserted is previous
            expected.add(value)
        else:
            assert rb.delete(value) == (value in expected)
            expected.discard(value)

        assert rb.root is tree.root
        assert_red_black_properties(tree)
        assert [n.value for n in InOrderIterator(tree.root)] == sorted(expected)
        assert rb.size() == len(expected)
        assert rb.contains(value) == (value in expected)
        assert rb.count_leaves() + rb.count_internal_nodes() == len(expected)

    for value in sorted(expected):
        assert rb.delete(value) is True
        assert_red_black_properties(tree)
    assert rb.root is tree.root is None
    assert rb.is_empty()


@pytest.mark.parametrize(
    ("defect", "message"),
    [
        ("cycle", "Cycle or shared child"),
        ("shared_child", "Cycle or shared child"),
        ("color", "Invalid node color"),
        ("ancestor_ordering", "BST upper bound"),
        ("size", "Node count disagrees"),
    ],
)
def test_invariant_helper_rejects_invalid_structure(defect, message):
    """
    Check that invariant validation rejects malformed structures safely.
    """
    root = RBNodeImpl(10)
    root.color = RBNode.BLACK
    root.left = RBNodeImpl(5)
    root.right = RBNodeImpl(15)
    tree = create_tree(root, 3)
    RedBlackImpl[int](tree)
    assert_red_black_properties(tree)

    if defect == "cycle":
        root.left.left = root
    elif defect == "shared_child":
        root.right = root.left
    elif defect == "color":
        root.left.color = 2
    elif defect == "ancestor_ordering":
        root.left.right = RBNodeImpl(12)
        tree._size = 4
    else:
        tree._size = 4

    with pytest.raises(AssertionError, match=message):
        assert_red_black_properties(tree)


# =====================================================
# Inherited BST Operations
# =====================================================


def test_bst_extrema_after_rb_mutations():
    """
    Check inherited BST extrema against the root updated by RB balancing.
    """
    tree = BinaryTreeImpl[int](LevelOrderIterator)
    rb = RedBlackImpl[int](tree)
    bst = rb
    assert isinstance(rb, BSTImpl)
    assert bst.minimum() is bst.maximum() is bst.min() is bst.max() is None

    expected: set[int] = set()
    for value in (30, 20, 10, 40, 50, 25, 5):
        rb.insert(value)
        expected.add(value)
        assert bst.minimum() is bst.min() is rb.find(min(expected))
        assert bst.maximum() is bst.max() is rb.find(max(expected))
        assert rb.root is tree.root
        assert_red_black_properties(tree)

    for value in (5, 50, 30, 10, 40, 20, 25):
        assert bst.delete(value) is True
        expected.remove(value)
        if expected:
            assert bst.minimum() is bst.min() is rb.find(min(expected))
            assert bst.maximum() is bst.max() is rb.find(max(expected))
        else:
            assert bst.minimum() is bst.maximum() is bst.min() is bst.max() is None
        assert_red_black_properties(tree)


def test_bst_extrema_for_subtree_and_after_clear():
    tree = BinaryTreeImpl[int](LevelOrderIterator)
    rb = RedBlackImpl[int](tree)
    for value in (20, 10, 30, 5, 15, 25, 35):
        rb.insert(value)
    root = rb.get_root()
    assert root is not None

    assert rb.minimum(root.left) is rb.find(5)
    assert rb.maximum(root.left) is rb.find(15)
    assert rb.minimum(root.right) is rb.find(25)
    assert rb.maximum(root.right) is rb.find(35)

    rb.clear()
    assert rb.minimum() is rb.maximum() is rb.min() is rb.max() is None
    node = rb.insert(40)
    assert rb.minimum() is rb.maximum() is rb.min() is rb.max() is node
    assert_red_black_properties(tree)
