def rob(nums):
    """
    Calculates the maximum amount of money a robber can steal from a row of houses
    without robbing adjacent houses.

    Args:
        nums: A list of non-negative integers representing the amount of money in each house.

    Returns:
        The maximum amount of money the robber can steal.
    """
    n = len(nums)
    if n == 0:
        return 0  # Handle the case of an empty house list
    if n == 1:
        return nums[0]  # If there's only one house, take it

    # Initialize variables to track the maximum amount stolen at the previous two houses
    prev_max = nums[0]
    curr_max = max(nums[0], nums[1])

    for i in range(2, n):
        # Update current max using previous two max values
        temp = curr_max
        curr_max = max(curr_max, prev_max + nums[i])
        prev_max = temp

    return curr_max  # Return the maximum amount stolen


def test():
    assert rob([1, 2, 3, 1]) == 4
    assert rob([2, 7, 9, 3, 1]) == 12

test()
