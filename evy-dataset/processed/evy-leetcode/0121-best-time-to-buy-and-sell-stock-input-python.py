def max_profit(prices):
    """Calculates the maximum profit from buying and selling a stock.

    Args:
        prices: A list of integers representing the stock prices each day.

    Returns:
        The maximum profit that can be achieved.
    """
    max_profit = 0       # Initialize maximum profit to 0
    lowest_price = prices[0]  # Start with the first price as the lowest

    for price in prices:
        max_profit = max(max_profit, price - lowest_price)  # Update max profit if we find a better one
        lowest_price = min(lowest_price, price)  # Update the lowest price so far

    return max_profit

# Test Cases
def test_max_profit():
    assert max_profit([7, 1, 5, 3, 6, 4]) == 5
    assert max_profit([7, 6, 4, 3, 1]) == 0

# Run the tests if this script is executed directly
if __name__ == "__main__":
    test_max_profit()
