from stepps.iterators.postorder import PostOrderIterator
from stepps.TreeBuilder.postorder_tree_builder_impl import PostOrderTreeBuilderImpl


def test_build_empty_sequence():
    builder = PostOrderTreeBuilderImpl[int]()

    root = builder.build([])

    assert root is None


def test_build_single_element():
    sequence = [50]
    builder = PostOrderTreeBuilderImpl[int]()

    root = builder.build(sequence)

    assert root is not None
    assert root.value == 50

    result = [node.value for node in PostOrderIterator(root)]

    assert result == sequence


def test_build_odd_length_sequence():
    sequence = [3, 4, 2, 6, 7, 5, 1]
    builder = PostOrderTreeBuilderImpl[int]()

    root = builder.build(sequence)

    assert root is not None
    assert root.value == 1

    result = [node.value for node in PostOrderIterator(root)]

    assert result == sequence


def test_build_even_length_sequence():
    sequence = [3, 2, 5, 6, 4, 1]
    builder = PostOrderTreeBuilderImpl[int]()

    root = builder.build(sequence)

    assert root is not None
    assert root.value == 1

    result = [node.value for node in PostOrderIterator(root)]

    assert result == sequence


def test_build_long_sequence():
    sequence = list(range(1, 16))
    builder = PostOrderTreeBuilderImpl[int]()

    root = builder.build(sequence)

    assert root is not None

    result = [node.value for node in PostOrderIterator(root)]

    assert result == sequence


def test_build_tree_structure():
    sequence = [3, 4, 2, 6, 7, 5, 1]
    builder = PostOrderTreeBuilderImpl[int]()

    root = builder.build(sequence)

    assert root is not None
    assert root.value == 1

    assert root.left is not None
    assert root.left.value == 2

    assert root.right is not None
    assert root.right.value == 5

    assert root.left.left is not None
    assert root.left.left.value == 3

    assert root.left.right is not None
    assert root.left.right.value == 4

    assert root.right.left is not None
    assert root.right.left.value == 6

    assert root.right.right is not None
    assert root.right.right.value == 7
