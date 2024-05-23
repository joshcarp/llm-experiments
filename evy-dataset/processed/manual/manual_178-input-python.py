def greet(name):
    print("Hello,", name)
greet("Alice")

def concat(a: str, b: str) -> str:
    return a + b

def calculate_area(length, width):
    area = length * width
    return area


a = "foo"
b = "bar"
print(concat(a, b))
result = calculate_area(5, 8)
print("Area of the rectangle:", result)

