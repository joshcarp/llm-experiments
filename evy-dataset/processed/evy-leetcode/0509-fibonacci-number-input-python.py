def fibonacci(n):
    """Calculates the nth Fibonacci number iteratively."""
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(n - 1):  # Loop n - 1 times since we already have the first two numbers
        a, b = b, a + b   # Elegant simultaneous assignment for updating
    return b


def test():
    """Tests the fibonacci function."""
    assert fibonacci(2) == 1
    assert fibonacci(3) == 2
    assert fibonacci(4) == 3

test()