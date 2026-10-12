from stepps.nodes.binary_node import BinaryNode
from stepps.nodes.impl.binary_node_impl import BinaryNodeImpl

__all__ = ["BinaryNode", "get_binary_node"]


def get_binary_node[T](value: T) -> BinaryNode[T]:
    """
    Create a binary node implementation.

    :param value: The value to store in the node.
    :return: A binary node implementation.
    """
    return BinaryNodeImpl(value)
