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


import cmath  # Import the complex math module for handling complex roots


# def third_order():
#     # Coefficients of the cubic polynomial ax^3 + bx^2 + cx + d
#     a = 6.815215
#     b = -28.85605239
#     c = 17.79369809
#     d = 182.68658296758696
#
#     # Calculate discriminant and intermediate values
#     discriminant = 18 * a * b * c * d - 4 * b ** 3 * d + b ** 2 * c ** 2 - 4 * a * c ** 3 - 27 * a ** 2 * d ** 2
#     C = (discriminant + cmath.sqrt(discriminant)) / 2
#     D = (discriminant - cmath.sqrt(discriminant)) / 2
#
#     # Calculate cube roots
#     root1 = -1 / 2 * (b + (C + D) ** (1 / 3) + (C - D) ** (1 / 3))
#     root2 = -1 / 2 * (b + (cmath.exp(2j * cmath.pi / 3) * C + cmath.exp(-2j * cmath.pi / 3) * D) ** (1 / 3) +
#                       (cmath.exp(-2j * cmath.pi / 3) * C + cmath.exp(2j * cmath.pi / 3) * D) ** (1 / 3))
#     root3 = -1 / 2 * (b + (cmath.exp(-2j * cmath.pi / 3) * C + cmath.exp(2j * cmath.pi / 3) * D) ** (1 / 3) +
#                       (cmath.exp(2j * cmath.pi / 3) * C + cmath.exp(-2j * cmath.pi / 3) * D) ** (1 / 3))
#
#     print("Root 1:", root1)
#     print("Root 2:", root2)
#     print("Root 3:", root3)
#
# third_order()


import numpy as np


def third_order_real_roots(coefficients, y_value):
    # Subtract y_value from the constant term (a0) in the polynomial coefficients
    coefficients[-1] -= y_value

    # Use np.roots to find the roots of the modified polynomial
    roots = np.roots(coefficients)

    # Filter out the real roots
    real_roots = roots[np.isreal(roots)].real
    real_roots = abs(real_roots[0])

    return real_roots


