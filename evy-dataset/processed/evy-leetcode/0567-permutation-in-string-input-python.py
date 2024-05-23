def check_inclusion(s1, s2):
    """
    Checks if one string (s1) is a permutation of a substring of another string (s2).

    Args:
        s1: The potential permutation string.
        s2: The string to search within.

    Returns:
        True if s1 is a permutation of a substring of s2, False otherwise.
    """
    if len(s1) > len(s2):
        return False

    s1_count = {}
    s2_count = {}

    # Initialize character counts for the first window
    for i in range(len(s1)):
        s1_count[s1[i]] = s1_count.get(s1[i], 0) + 1
        s2_count[s2[i]] = s2_count.get(s2[i], 0) + 1

    l = 0  # Left pointer of the sliding window

    for r in range(len(s1), len(s2)):  # Iterate with the right pointer
        if s1_count == s2_count:
            return True  # Permutation found

        # Update counts for the sliding window
        s2_count[s2[r]] = s2_count.get(s2[r], 0) + 1  # Add the new character
        s2_count[s2[l]] -= 1                         # Remove the old character
        if s2_count[s2[l]] == 0:
            del s2_count[s2[l]]
        l += 1  # Move the window

    return s1_count == s2_count  # Check one last time after the loop


def test():
    assert check_inclusion("ab", "ab") == True
    assert check_inclusion("ab", "eidbaooo") == True
    assert check_inclusion("ab", "eidboaoo") == False
    assert check_inclusion("ab", "a") == False
    # Additional test case to catch the issue
    assert check_inclusion("adc", "dcda") == True

test()
