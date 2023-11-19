import numpy as np


def second_order(y, a, b, c):
    # Calculate the discriminant
    c = c - y
    discriminant = b ** 2 - 4 * a * c

    # Check if the discriminant is non-negative for real solutions
    if discriminant >= 0:
        # Calculate the two solutions for x
        x1 = (-b + np.sqrt(discriminant)) / (2 * a)
        x2 = (-b - np.sqrt(discriminant)) / (2 * a)
        print("Real Solutions for x:")
        print("x1:", x1)
        print("x2:", x2)
        if x2 < x1 < 100:
            return x1
        elif x2 < 100:
            return x2
    else:
        print("Complex Solutions: No real solutions for x.")
        return y
