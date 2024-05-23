#START:PROMPT


def max_element(l: list):
    """Return maximum element in the list.
    >>> max_element([1, 2, 3])
    3
    >>> max_element([5, 3, -5, 2, -3, 3, 9, 0, 123, 1, -10])
    123
    """

#END:PROMPT
#START:SOLUTION
    m = l[0]
    for e in l:
        if e > m:
            m = e
    return m

#END:SOLUTION
#START:TEST


METADATA = {}


def check(candidate):
    assert candidate([1, 2, 3]) == 3
    assert candidate([5, 3, -5, 2, -3, 3, 9, 0, 124, 1, -10]) == 124

#END:TEST
#START:CHECK
check(max_element)
#END:CHECK