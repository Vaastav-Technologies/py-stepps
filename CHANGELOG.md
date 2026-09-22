# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Date format: YYYY-MM-DD

## [0.2.0] - 2026-22-09

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