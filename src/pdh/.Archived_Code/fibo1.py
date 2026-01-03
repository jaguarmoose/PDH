def fib(n: int) -> None:    # write Fibonacci series up to n
    """fib."""
    a, b = 0, 1
    while b < n:
        print(b, end=' ')
        a, b = b, a+b
    print()

def fib2(n: int) -> list[int]:   # return Fibonacci series up to n
    """fib2."""
    result = []
    a, b = 0, 1
    while b < n:
        result.append(b)
        a, b = b, a+b
    return result
