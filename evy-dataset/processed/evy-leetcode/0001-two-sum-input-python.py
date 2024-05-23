def two_sum(nums, target):
    num_dict = {}
    for i, v in enumerate(nums):
        if str(target - v) in num_dict:
            return [num_dict[str(v)], i]
        num_dict[str(v)] = i
    return []

def test():
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]
    assert two_sum([3, 2, 4], 6) == [1, 2]
    assert two_sum([3, 3], 6) == [0, 1]
