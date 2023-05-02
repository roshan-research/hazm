## Coding guideline

- All our code should currently compaitable with [python 3.6](https://docs.python.org/3/whatsnew/3.6.html) and higher.

- Whenever possible, utilize the latest language features available in python 3.6. For example instead of using older style `"Hello %s" % name` use f-strings `f"Hello {name}"`.

- Use type hints for parameters and return values. Built-in types like `str` and `float` can be used directly and specific types like `Dict` and `List` need to be imported from the `typing` module:

```py
from typing import Dict

def count_letters(word: str) -> Dict[str, int]:
    ...
```

- The type hint for a function without return value is `None`:

```py
class Person:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age
    ...
```

- The type hints for third-party libraries are often provided by the library itself:

```py
import numpy as np

def square_array(arr: np.ndarray) -> np.ndarray:
    return arr ** 2
```

- Provide documentation for your modules, classes and functions following the [google style format](https://google.github.io/styleguide/pyguide.html).

```py
def calculate_average(numbers: list) -> float:
    """
    Calculates the average of a given list of numbers.

    Args:
        numbers: A list of integers or floats to be averaged.

    Returns:
        The arithmetic mean (float) of the numbers in the input list.

    Raises:
        TypeError: If `numbers` is not a list.
        ValueError: If `numbers` is an empty list.

    Examples:
        >>> calculate_average([1, 2, 3, 4, 5])
        3.0

        >>> calculate_average([2.5, 3.75, 4.25, 5.5])
        4.0
    """
    if not isinstance(numbers, list):
        raise TypeError("`numbers` must be a list.")

    if len(numbers) == 0:
        raise ValueError("`numbers` cannot be an empty list.")

    total = sum(numbers)
    average = total / len(numbers)
    return average
```
Check out a more complete example [here]( https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html).

- Follow [pep8](https://peps.python.org/pep-0008/) coding guidline. The [persian version](https://pep8.ir/).

