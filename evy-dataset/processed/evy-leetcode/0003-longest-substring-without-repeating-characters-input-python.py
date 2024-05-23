def length_of_longest_substring(s):
    seen = {}
    longest_substring = 0
    start_idx = 0
    for i, elem in enumerate(s):
        if elem in seen:
            start_idx = max(start_idx, seen[elem] + 1)
        seen[elem] = i
        longest_substring = max(longest_substring, i - start_idx + 1)
    return longest_substring

def test():
    assert length_of_longest_substring("abcabcbb") == 3
    assert length_of_longest_substring("bbbbb") == 1
    assert length_of_longest_substring("pwwkew") == 3

test()