from random import Random

import pytest

from stepps.iterators.base_iterator import BinaryTreeIterator
from stepps.iterators.inorder import InOrderIterator
from stepps.iterators.morris import MorrisIterator
from stepps.iterators.morris_impl import MorrisIteratorImpl
from stepps.nodes.impl.binary_node_impl import BinaryNodeImpl

# =====================================================
# Tree Cases and Fixtures
# =====================================================


TREE_CASES = [
    pytest.param(([], [], []), id="empty"),
    pytest.param(([42], [], [0]), id="single"),
    pytest.param(([2, 1], [(0, "left", 1)], [1, 0]), id="left-child"),
    pytest.param(([1, 2], [(0, "right", 1)], [0, 1]), id="right-child"),
    pytest.param(
        (
            [4, 2, 6, 1, 3, 5, 7],
            [
                (0, "left", 1),
                (0, "right", 2),
                (1, "left", 3),
                (1, "right", 4),
                (2, "left", 5),
                (2, "right", 6),
            ],
            [3, 1, 4, 0, 5, 2, 6],
        ),
        id="balanced",
    ),
    pytest.param(
        ([9, 8, 7, 6], [(0, "left", 1), (1, "left", 2), (2, "left", 3)], [3, 2, 1, 0]),
        id="left-chain",
    ),
    pytest.param(
        (
            [9, 8, 7, 6],
            [(0, "right", 1), (1, "right", 2), (2, "right", 3)],
            [0, 1, 2, 3],
        ),
        id="right-chain-non-bst",
    ),
    pytest.param(
        (
            [1, 2, 3, 4, 5],
            [(0, "left", 1), (1, "right", 2), (2, "left", 3), (3, "right", 4)],
            [1, 3, 4, 2, 0],
        ),
        id="zigzag",
    ),
    pytest.param(
        (
            [None, 0, 0, None, 0],
            [(0, "left", 1), (1, "right", 2), (2, "right", 3), (0, "right", 4)],
            [1, 2, 3, 0, 4],
        ),
        id="duplicate-and-none-values",
    ),
    pytest.param(
        (
            [{"root": 1}, {"left": 2}, {"right": 3}],
            [(0, "left", 1), (0, "right", 2)],
            [1, 0, 2],
        ),
        id="unorderable-values",
    ),
]


@pytest.fixture(params=TREE_CASES)
def tree_case(request):
    values, edges, order = request.param
    nodes = [BinaryNodeImpl(value) for value in values]

    for parent, side, child in edges:
        setattr(nodes[parent], side, nodes[child])

    root = nodes[0] if nodes else None
    expected = [nodes[index] for index in order]

    return root, nodes, expected


# =====================================================
# Helper Functions
# =====================================================


def snapshot_tree(nodes):
    return [(node, node.left, node.right, node.value) for node in nodes]


def assert_tree_restored(original):
    # Inspect saved nodes directly so a leftover cycle cannot hide corruption.
    for node, left, right, value in original:
        assert node.left is left
        assert node.right is right
        assert node.value is value


def assert_iterator_exhausted(iterator):
    for _ in range(2):
        with pytest.raises(StopIteration):
            next(iterator)


# =====================================================
# Traversals
# =====================================================


def test_inorder_node_identity_and_restoration(tree_case):
    root, nodes, expected = tree_case
    original = snapshot_tree(nodes)
    iterator: MorrisIterator = MorrisIteratorImpl(root)

    assert isinstance(iterator, BinaryTreeIterator)
    assert iter(iterator) is iterator
    # Consume exactly the expected count to detect unwanted extra nodes.
    for node in expected:
        assert next(iterator) is node

    # Restoration must already be complete before requesting StopIteration.
    assert_tree_restored(original)
    assert_iterator_exhausted(iterator)
    assert_tree_restored(original)


# =====================================================
# Close and Tree Reuse
# =====================================================


def test_close_at_every_traversal_position(tree_case):
    root, nodes, expected = tree_case
    original = snapshot_tree(nodes)

    for count in range(len(expected) + 1):
        iterator: MorrisIterator = MorrisIteratorImpl(root)
        for node in expected[:count]:
            assert next(iterator) is node

        iterator.close()
        assert_tree_restored(original)
        assert_iterator_exhausted(iterator)
        iterator.close()
        assert_tree_restored(original)

        # The restored tree can be traversed again by a fresh iterator.
        assert list(MorrisIteratorImpl(root)) == expected
        assert_tree_restored(original)


# =====================================================
# Cleanup After Early Termination
# =====================================================


def test_close_restores_after_break(tree_case):
    root, nodes, expected = tree_case
    original = snapshot_tree(nodes)
    iterator: MorrisIterator = MorrisIteratorImpl(root)

    try:
        for node in iterator:
            assert node is expected[0]
            break
    finally:
        iterator.close()

    assert_tree_restored(original)
    assert_iterator_exhausted(iterator)


def test_close_restores_after_exception(tree_case):
    root, nodes, expected = tree_case
    original = snapshot_tree(nodes)
    error = RuntimeError("consumer failed")

    for count in range(len(expected) + 1):
        iterator: MorrisIterator = MorrisIteratorImpl(root)
        with pytest.raises(RuntimeError) as caught:
            try:
                for node in expected[:count]:
                    assert next(iterator) is node
                raise error
            finally:
                iterator.close()

        assert caught.value is error
        assert_tree_restored(original)
        assert_iterator_exhausted(iterator)


def test_close_after_full_traversal(tree_case):
    root, nodes, expected = tree_case
    original = snapshot_tree(nodes)

    iterator: MorrisIterator = MorrisIteratorImpl(root)
    assert list(iterator) == expected
    assert_iterator_exhausted(iterator)
    iterator.close()

    assert_tree_restored(original)
    assert_iterator_exhausted(iterator)


# =====================================================
# Context Manager
# =====================================================


def test_context_manager_restores_after_break(tree_case):
    root, nodes, expected = tree_case
    original = snapshot_tree(nodes)
    iterator: MorrisIterator = MorrisIteratorImpl(root)

    with iterator as entered:
        assert entered is iterator
        for node in entered:
            assert node is expected[0]
            break

    assert_tree_restored(original)
    assert_iterator_exhausted(iterator)


def test_context_manager_restores_after_exception(tree_case):
    root, nodes, expected = tree_case
    original = snapshot_tree(nodes)
    error = RuntimeError("consumer failed")

    for count in range(len(expected) + 1):
        iterator: MorrisIterator = MorrisIteratorImpl(root)
        with pytest.raises(RuntimeError) as caught, iterator:
            for node in expected[:count]:
                assert next(iterator) is node
            raise error

        assert caught.value is error
        assert_tree_restored(original)
        assert_iterator_exhausted(iterator)


def test_context_manager_after_full_traversal(tree_case):
    root, nodes, expected = tree_case
    original = snapshot_tree(nodes)

    with MorrisIteratorImpl(root) as iterator:
        assert list(iterator) == expected

    assert_tree_restored(original)
    assert_iterator_exhausted(iterator)


# =====================================================
# Temporary Links and Tree Structure Preservation
# =====================================================


def test_morris_threads_use_existing_predecessor_links():
    root = BinaryNodeImpl(4)
    left = BinaryNodeImpl(1)
    middle = BinaryNodeImpl(2)
    predecessor = BinaryNodeImpl(3)
    root.left = left
    left.right = middle
    middle.right = predecessor
    original = snapshot_tree([root, left, middle, predecessor])

    iterator: MorrisIterator = MorrisIteratorImpl(root)
    try:
        assert next(iterator) is left
        # Morris must thread the rightmost node, preserving real right edges.
        assert predecessor.right is root
        assert left.right is middle
        assert middle.right is predecessor
        assert next(iterator) is middle
        assert next(iterator) is predecessor
        assert next(iterator) is root
        assert predecessor.right is None
    finally:
        iterator.close()

    assert_tree_restored(original)


# =====================================================
# Larger Trees
# =====================================================


@pytest.mark.parametrize("side", ["left", "right", "alternating"])
def test_deep_tree_without_recursion(side):
    nodes = [BinaryNodeImpl(index) for index in range(5000)]
    for index in range(len(nodes) - 1):
        child_side = side
        if side == "alternating":
            child_side = "left" if index % 2 else "right"
        setattr(nodes[index], child_side, nodes[index + 1])

    original = snapshot_tree(nodes)
    expected = list(InOrderIterator(nodes[0]))
    assert list(MorrisIteratorImpl(nodes[0])) == expected
    assert_tree_restored(original)

    iterator = MorrisIteratorImpl(nodes[0])
    assert next(iterator) is expected[0]
    iterator.close()
    assert_tree_restored(original)
    assert_iterator_exhausted(iterator)


# =====================================================
# Randomized Traversals
# =====================================================


@pytest.mark.parametrize("seed", range(20))
def test_random_tree_matches_stack_based_inorder(seed):
    """
    Check inorder traversal and link restoration for seeded random trees.
    """
    random = Random(seed)
    nodes = [BinaryNodeImpl(random.randrange(5)) for _ in range(100)]
    slots = [(nodes[0], "left"), (nodes[0], "right")]
    for node in nodes[1:]:
        parent, side = slots.pop(random.randrange(len(slots)))
        setattr(parent, side, node)
        slots.extend([(node, "left"), (node, "right")])

    original = snapshot_tree(nodes)
    expected = list(InOrderIterator(nodes[0]))
    assert list(MorrisIteratorImpl(nodes[0])) == expected
    assert_tree_restored(original)

    iterator = MorrisIteratorImpl(nodes[0])
    try:
        for node in expected[: random.randrange(1, len(nodes))]:
            assert next(iterator) is node
    finally:
        iterator.close()

    assert_tree_restored(original)
    assert_iterator_exhausted(iterator)
