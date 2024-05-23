def backtrack(nums, current, ans):
    """Recursive backtracking function to generate subsets."""
    if not nums:  # Base case: empty input list
        ans.append(current[:])  # Append a copy of the current subset
        return

    for i in range(len(nums)):
        backtrack(nums[i+1:], current, ans)  # Exclude the current element
        current.append(nums[i])  # Include the current element
        if len(nums) > 1:  # If there are more elements
            backtrack(nums[i+1:], current, ans)  # Backtrack again
        else:
            backtrack([], current, ans)  # Special case for last element
        current.pop()  # Remove the current element (backtracking step)

def subsets(nums):
    """Generates all subsets of a given set.

    Args:
        nums: A list of numbers representing the set.

    Returns:
        A list of lists, where each inner list is a subset of the input set.
    """
    current, ans = [], []
    backtrack(nums, current, ans)
    return ans

# Testing
fails = 0
total = 0

def assert_equal_same_elements(want, got):
    """Asserts that two lists of lists contain the same elements regardless of order."""
    global fails, total

    want_set = set(tuple(x) for x in want)  # Convert to sets for easier comparison
    got_set = set(tuple(x) for x in got)

    missing_elements = want_set - got_set
    extra_elements = got_set - want_set

    if missing_elements or extra_elements:
        fails += 1
        print(f"Expected: {want}, Got: {got}")
        if missing_elements:
            print(f"Missing elements: {missing_elements}")
        if extra_elements:
            print(f"Extra elements: {extra_elements}")

    total += 1

def test():
    """Tests the subsets function."""
    assert_equal_same_elements([[1, 2, 3], [1, 2], [1, 3], [1], [2, 3], [2], [3], []], subsets([1, 2, 3]))
    assert_equal_same_elements([[0], []], subsets([0]))
    assert_equal_same_elements([[]], subsets([]))

test()