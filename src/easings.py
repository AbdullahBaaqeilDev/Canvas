import math
from typing import Callable, Dict

# Type alias for clarity
easing_function = Callable[[float], float]

# Constants
PI = math.pi
c1 = 1.70158
c2 = c1 * 1.525
c3 = c1 + 1
c4 = (2 * PI) / 3
c5 = (2 * PI) / 4.5


def bounce_out(x: float) -> float:
    n1 = 7.5625
    d1 = 2.75

    if x < 1 / d1:
        return n1 * x * x
    elif x < 2 / d1:
        x -= 1.5 / d1
        return n1 * x * x + 0.75
    elif x < 2.5 / d1:
        x -= 2.25 / d1
        return n1 * x * x + 0.9375
    else:
        x -= 2.625 / d1
        return n1 * x * x + 0.984375


# Dictionary of easing functions (keys are now shorter and snake_case)
easings_functions: Dict[str, easing_function] = {
    "linear": lambda x: x,
    "quad_in": lambda x: x * x,
    "quad_out": lambda x: 1 - (1 - x) * (1 - x),
    "quad_in_out": lambda x: 2 * x * x if x < 0.5 else 1 - math.pow(-2 * x + 2, 2) / 2,
    "cubic_in": lambda x: x * x * x,
    "cubic_out": lambda x: 1 - math.pow(1 - x, 3),
    "cubic_in_out": lambda x: 4 * x * x * x
    if x < 0.5
    else 1 - math.pow(-2 * x + 2, 3) / 2,
    "quart_in": lambda x: x**4,
    "quart_out": lambda x: 1 - math.pow(1 - x, 4),
    "quart_in_out": lambda x: 8 * x**4 if x < 0.5 else 1 - math.pow(-2 * x + 2, 4) / 2,
    "quint_in": lambda x: x**5,
    "quint_out": lambda x: 1 - math.pow(1 - x, 5),
    "quint_in_out": lambda x: 16 * x**5 if x < 0.5 else 1 - math.pow(-2 * x + 2, 5) / 2,
    "sine_in": lambda x: 1 - math.cos((x * PI) / 2),
    "sine_out": lambda x: math.sin((x * PI) / 2),
    "sine_in_out": lambda x: -(math.cos(PI * x) - 1) / 2,
    "expo_in": lambda x: 0 if x == 0 else math.pow(2, 10 * x - 10),
    "expo_out": lambda x: 1 if x == 1 else 1 - math.pow(2, -10 * x),
    "expo_in_out": lambda x: (
        0
        if x == 0
        else 1
        if x == 1
        else math.pow(2, 20 * x - 10) / 2
        if x < 0.5
        else (2 - math.pow(2, -20 * x + 10)) / 2
    ),
    "circ_in": lambda x: 1 - math.sqrt(1 - x * x),
    "circ_out": lambda x: math.sqrt(1 - (x - 1) ** 2),
    "circ_in_out": lambda x: (
        (1 - math.sqrt(1 - (2 * x) ** 2)) / 2
        if x < 0.5
        else (math.sqrt(1 - (-2 * x + 2) ** 2) + 1) / 2
    ),
    "back_in": lambda x: c3 * x**3 - c1 * x**2,
    "back_out": lambda x: 1 + c3 * math.pow(x - 1, 3) + c1 * math.pow(x - 1, 2),
    "back_in_out": lambda x: (
        (math.pow(2 * x, 2) * ((c2 + 1) * 2 * x - c2)) / 2
        if x < 0.5
        else (math.pow(2 * x - 2, 2) * ((c2 + 1) * (2 * x - 2) + c2) + 2) / 2
    ),
    "elastic_in": lambda x: (
        0
        if x == 0
        else 1
        if x == 1
        else -math.pow(2, 10 * x - 10) * math.sin((x * 10 - 10.75) * c4)
    ),
    "elastic_out": lambda x: (
        0
        if x == 0
        else 1
        if x == 1
        else math.pow(2, -10 * x) * math.sin((x * 10 - 0.75) * c4) + 1
    ),
    "elastic_in_out": lambda x: (
        0
        if x == 0
        else 1
        if x == 1
        else -(math.pow(2, 20 * x - 10) * math.sin((20 * x - 11.125) * c5)) / 2
        if x < 0.5
        else (math.pow(2, -20 * x + 10) * math.sin((20 * x - 11.125) * c5)) / 2 + 1
    ),
    "bounce_in": lambda x: 1 - bounce_out(1 - x),
    "bounce_out": bounce_out,
    "bounce_in_out": lambda x: (
        (1 - bounce_out(1 - 2 * x)) / 2 if x < 0.5 else (1 + bounce_out(2 * x - 1)) / 2
    ),
}
