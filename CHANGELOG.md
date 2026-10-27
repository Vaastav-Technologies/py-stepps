# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Date format: YYYY-MM-DD

## [0.5.0.post2] - 2026-10-27

A post-release was needed to update the author contact information on PyPI.

### Changed
- Updated package author metadata in `pyproject.toml` to include the Vaastav Technologies contact email (`info@vaastav.tech`).

## [0.5.0.post1] - 2026-10-27

a post release was needed to satisfy author/maintainer identity on PyPI

### Changed
- Updated package author metadata in pyproject.toml to display both Suhas Krishna Srivastava and Trinay Mitra on PyPI.
- Updated package maintainer metadata to include Vaastav Technologies.

## [0.5.0] - 2026-10-27

### Added

- Added Morris inorder traversal for visiting binary tree nodes in left-root-right order using constant auxiliary space, without a stack or recursion.
- Added automatic restoration of temporary tree links when Morris traversal finishes, with `close()` and `with` block support for restoring the tree when traversal stops early.

## [0.4.0] - 2026-10-13

### Added

- Added red-black trees that automatically maintain balance when values are inserted or deleted.
- Added support for creating a red-black tree from an existing binary tree, with search, membership checks, minimum, and maximum operations.
- Added `get_binary_node(value)` in `stepps.nodes` for creating binary nodes.

### Changed

- Changed node creation to use `get_binary_node(value)`, with `BinaryNode` defining the node interface.
- Moved `AVL` and `AVLImpl` imports to `stepps.trees.balanced.avl_tree`.
- Moved the `Comparable` type to `stepps.comparable`.

## [0.3.0] - 2026-09-28

**### Added**

- Added protected `_set_left_subtree` and `_set_right_subtree` operations for setting the left and right subtrees of a binary tree.
- Added AVL tree support for maintaining balanced binary trees.
- Added automatic balancing after AVL tree insert and delete operations.
- Added support for LL, RR, LR, and RL AVL balancing cases.
- Added configurable AVL balance factor support.

## [0.2.0] - 2026-09-22

### Added

- Added `get_root` to the common `Tree` interface.
- Added left and right subtree access to the `BinaryTree` interface.
- Added left and right tree rotation operations to the `BinaryTree` interface.
- Implemented tree root access, subtree access, and rotation operations in `BinaryTreeImpl`.
- Added tests covering tree root access, subtree access, and left and right rotations.
- Added support for using tree rotations as the foundation for future tree balancing algorithms. 

## [0.1.0] - 2026-09-09

### Added

- Added binary tree and binary search tree implementations.
- Added binary node support for tree construction.
- Added binary search tree operations, including insert, find, delete, minimum, and maximum.
- Added preorder, inorder, postorder, and level-order tree iterators.
- Added a common `TreeBuilder` interface for constructing binary trees from sequences.
- Added tree builders for level-order, inorder, preorder, and postorder sequences.
- Ensured that traversing a constructed tree using its corresponding iterator reproduces the original sequence.
- Added CLI-based tree visualization support.
- Added tests for binary trees, binary search trees, tree builders, and tree visualization.

## [0.0.0.dev0] - 2026-08-04

### Added

- Introduced initial Changelog.
- Introduced skeleton project.