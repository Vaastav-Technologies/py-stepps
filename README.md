# Stepps

![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)
![License](https://img.shields.io/github/license/Vaastav-Technologies/py-stepps)
[![test](https://github.com/Vaastav-Technologies/py-stepps/actions/workflows/test.yml/badge.svg)](https://github.com/Vaastav-Technologies/py-stepps/actions/workflows/test.yml)
[![typecheck](https://github.com/Vaastav-Technologies/py-stepps/actions/workflows/typecheck.yml/badge.svg)](https://github.com/Vaastav-Technologies/py-stepps/actions/workflows/typecheck.yml)
[![lint](https://github.com/Vaastav-Technologies/py-stepps/actions/workflows/lint.yml/badge.svg)](https://github.com/Vaastav-Technologies/py-stepps/actions/workflows/lint.yml)
[![publish](https://github.com/Vaastav-Technologies/py-stepps/actions/workflows/python-publish.yml/badge.svg)](https://github.com/Vaastav-Technologies/py-stepps/actions/workflows/python-publish.yml)

---

**Fully typed, modular data structures and algorithms for binary trees in Python.**

`stepps` provides generic binary tree and binary search tree implementations,
tree traversal iterators, traversal-based tree builders, and tree visualization
utilities.

The project follows an interface-and-implementation architecture and uses
Python generics and static typing throughout its APIs.

---

## Features

- Generic binary tree data structures.
- Binary search tree implementation.
- Preorder, inorder, postorder, and level-order traversal iterators.
- Tree builders for preorder, inorder, postorder, and level-order sequences.
- Binary tree statistics and utility operations.
- CLI tree visualization.
- Generic type support.
- Interface-and-implementation architecture.
- Pytest-based test suite.
- MyPy static type checking.
- Ruff linting and formatting.

---

## Installation

```bash
pip install stepps
```

For local development:

```bash
git clone https://github.com/Vaastav-Technologies/py-stepps.git
cd py-stepps
pip install -e .
```

---

## Binary Tree

`BinaryTree` defines the binary tree interface and `BinaryTreeImpl` provides
the default implementation.

### Binary Tree Methods

| Method | Description |
|---|---|
| `insert(value)` | Inserts a value into the tree. |
| `delete(value)` | Deletes a value from the tree. |
| `find(value)` | Finds and returns the node containing the value. |
| `contains(value)` | Checks whether a value exists in the tree. |
| `__contains__(value)` | Supports the `value in tree` operation. |
| `clear()` | Removes all nodes from the tree. |
| `is_empty()` | Checks whether the tree is empty. |
| `size()` | Returns the number of nodes in the tree. |
| `height()` | Returns the height of the tree. |
| `count_leaves()` | Returns the number of leaf nodes. |
| `count_internal_nodes()` | Returns the number of internal nodes. |
| `invert_tree()` | Inverts the tree in-place. |

---

## Binary Search Tree

`BST` defines the binary search tree interface and `BSTImpl` provides the
implementation.

The binary search tree maintains the ordering property that values in the
left subtree are smaller than the node value and values in the right subtree
are greater.

### Binary Search Tree Methods

| Method | Description |
|---|---|
| `insert(value)` | Inserts a value while maintaining BST ordering. |
| `delete(value)` | Deletes a value while maintaining BST ordering. |
| `find(value)` | Searches for and returns the node containing the value. |
| `contains(value)` | Checks whether a value exists in the BST. |
| `__contains__(value)` | Supports the `value in tree` operation. |
| `minimum()` | Returns the node containing the minimum value. |
| `maximum()` | Returns the node containing the maximum value. |
| `min()` | Returns the minimum value in the BST. |
| `max()` | Returns the maximum value in the BST. |
| `clear()` | Removes all nodes from the tree. |
| `is_empty()` | Checks whether the tree is empty. |
| `size()` | Returns the number of nodes in the tree. |
| `height()` | Returns the height of the tree. |
| `count_leaves()` | Returns the number of leaf nodes. |
| `count_internal_nodes()` | Returns the number of internal nodes. |
| `invert_tree()` | Inverts the tree in-place. |

---

## Tree Traversal Iterators

`stepps` provides iterators implementing the standard binary tree traversal
orders.

### PreOrderIterator

Traverses the tree using:

`Root → Left → Right`

### InOrderIterator

Traverses the tree using:

`Left → Root → Right`

### PostOrderIterator

Traverses the tree using:

`Left → Right → Root`

### LevelOrderIterator

Traverses the tree level by level from left to right.

### Iterator API

All traversal iterators implement the common `BinaryTreeIterator` interface.

| Method | Description |
|---|---|
| `__iter__()` | Returns the iterator itself. |
| `__next__()` | Returns the next node in the traversal and raises `StopIteration` when complete. |

---

## Tree Builders

`TreeBuilder` defines the common interface for constructing a binary tree from
a sequence.

### TreeBuilder Method

| Method | Description |
|---|---|
| `build(sequence)` | Builds and returns a binary tree from the supplied sequence. Returns `None` for an empty sequence. |

The package provides the following builder interfaces and implementations:

- `LevelOrderTreeBuilder`
- `LevelOrderTreeBuilderImpl`
- `InOrderTreeBuilder`
- `InOrderTreeBuilderImpl`
- `PreOrderTreeBuilder`
- `PreOrderTreeBuilderImpl`
- `PostOrderTreeBuilder`
- `PostOrderTreeBuilderImpl`

Each builder constructs a tree whose corresponding traversal reproduces the
input sequence.

---

## Tree Visualization

The visualization package provides interfaces and implementations for
displaying binary trees in the CLI.

### Visualization Components

- `TreeVisualizer`
- `CliTreeVisualizer`
- `CliTreeVisualizerImpl`

### Visualization Method

| Method | Description |
|---|---|
| `treevisualizer(root)` | Displays the supplied binary tree in a CLI-friendly tree representation. |

---

## Binary Node

`BinaryNode[T]` is the generic node type used by the binary tree structures.

Each node provides:

| Attribute | Description |
|---|---|
| `value` | The value stored in the node. |
| `left` | Reference to the left child node or `None`. |
| `right` | Reference to the right child node or `None`. |

---

## Tree Statistics

The binary tree implementation provides the following statistics:

| Method | Description |
|---|---|
| `size()` | Returns the total number of nodes. |
| `height()` | Returns the height of the tree. |
| `count_leaves()` | Returns the number of leaf nodes. |
| `count_internal_nodes()` | Returns the number of internal nodes. |
| `is_empty()` | Returns whether the tree contains no nodes. |

The height convention is:

- Empty tree: `-1`
- Single-node tree: `0`

---

## Complexity

### Binary Search Tree

| Operation | Average | Worst Case |
|---|---:|---:|
| Search | `O(log n)` | `O(n)` |
| Insert | `O(log n)` | `O(n)` |
| Delete | `O(log n)` | `O(n)` |
| Minimum | `O(log n)` | `O(n)` |
| Maximum | `O(log n)` | `O(n)` |

### Tree Builders

All tree builders construct the tree in:

- Time: `O(n)`
- Total space: `O(n)`

The recursive builders use `O(log n)` auxiliary stack space for the balanced
trees they construct.

---


## Testing

The project uses `pytest` for testing.

Run the complete test suite:

```bash
python -m pytest
```

Run tests with output enabled:

```bash
python -m pytest -s
```
Run the test suite along with doctests:

```bash
pytest --cov --cov-branch --doctest-modules
```

Generate a coverage report:

```bash
python -m pytest --cov=stepps --cov-report=term-missing
```

The test suite covers:

- Binary tree operations.
- Binary search tree operations.
- Tree traversal iterators.
- Tree builders.
- Tree visualization.
- Empty and single-node trees.
- Different tree sizes and structures.
- Traversal sequence reconstruction.

---

## Type Checking

The project uses MyPy for static type checking.

```bash
mypy -p stepps
```

The public APIs use Python generic type parameters to provide type-safe
operations across nodes, trees, iterators, and tree builders.

---

## Linting and Formatting

The project uses Ruff for linting and formatting.

Check for linting issues:

```bash
ruff check .
```

Automatically fix supported linting issues:

```bash
ruff check --fix .
```

Format the project:

```bash
ruff format .
```

Check formatting without modifying files:

```bash
ruff format --check .
```

---

## Contributing

Clone the repository:

```bash
git clone https://github.com/Vaastav-Technologies/py-stepps.git
cd py-stepps
```

Install the project in editable mode:

```bash
pip install -e .
```

Before submitting changes, run:

```bash
python -m pytest
python -m mypy .
ruff check .
ruff format --check .
```

Please add or update tests when modifying existing functionality or adding
new functionality.

---

## License

See [LICENSE](./LICENSE) for the license under which this project is
distributed.

---

## Links

- GitHub: https://github.com/Vaastav-Technologies/py-stepps
