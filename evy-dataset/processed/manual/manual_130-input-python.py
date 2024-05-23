from collections import deque

def right_side_view(tree_arr):
    """
    Finds the right side view of a binary tree represented as an array.

    Args:
        tree_arr: A list representing the binary tree in level order traversal.

    Returns:
        A list containing the values of nodes visible from the right side.
    """
    root = build_binary_tree(tree_arr)  # Build the binary tree
    queue = deque([root])  # Use a deque for efficient queue operations
    res = []

    while queue:
        size = len(queue)
        for i in range(size):
            node = queue.popleft()
            if node and i == size - 1:  # If it's the last node in the level
                res.append(node["val"])
            if node and node.get("left"):  # Check if left child exists
                queue.append(node["left"])
            if node and node.get("right"):  # Check if right child exists
                queue.append(node["right"])
    return res

def build_binary_tree(tree):
    """
    Builds a binary tree from a list representation.

    Args:
        tree: A list representing the binary tree in level order traversal.

    Returns:
        The root node of the constructed binary tree.
    """
    if not tree:  # Empty tree
        return None
    root = {"val": tree[0]}
    queue = deque([root])
    i = 1
    while queue and i < len(tree):
        node = queue.popleft()
        if tree[i] != "null":
            node["left"] = {"val": tree[i]}
            queue.append(node["left"])
        i += 1
        if i < len(tree) and tree[i] != "null":
            node["right"] = {"val": tree[i]}
            queue.append(node["right"])
        i += 1

    return root

def test():
    """Tests the right_side_view function."""
    assert right_side_view([1, 2, 3, "null", 5, "null", 4]) == [1, 3, 4]
    assert right_side_view([1, "null", 3]) == [1, 3]
    assert right_side_view([]) == []
    assert right_side_view([1, 2, 3, 4]) == [1, 3, 4]

test()

