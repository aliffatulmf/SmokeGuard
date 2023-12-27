import collections


class DataChecker:
    """
    This class provides methods for checking the type of a value.

    Examples:

    ```python
    # Create an instance of the class
    data_checker = DataChecker()

    # Check if the value has a value
    value = 10
    if data_checker.has_value(value):
        print(f"The value '{value}' has a value.")

    # Check if the value is of a specific type
    value = "Hello"
    if data_checker.is_type(value, "str"):
        print(f"The value '{value}' is a string.")

    # Define a custom data type
    def is_positive_integer(value):
        return isinstance(value, int) and value > 0

    # Add the custom data type to the data checker
    data_checker.custom_types["positive_int"] = is_positive_integer

    # Check if the value is of the custom data type
    value = 5
    if data_checker.is_type(value, "positive_int"):
        print(f"The value '{value}' is a positive integer.")
    """

    def __init__(self, custom_types=None):
        """
        Initializes the class with a dictionary of custom data types.

        Args:
            custom_types: A dictionary where the keys are the names of the custom data types
                          and the values are functions that take a single argument (the value to be checked)
                          and return True if the value is of the custom type, False otherwise.

        Examples:

        ```python
        data_checker = DataChecker({
            "positive_int": lambda value: isinstance(value, int) and value > 0,
            "non_empty_string": lambda value: isinstance(value, str) and len(value) > 0,
        })
        ```
        """
        self.default_types = {
            "int": int,
            "float": float,
            "bool": bool,
            "str": str,
            "list": list,
            "tuple": tuple,
            "dict": dict,
            "set": set,
        }
        self.custom_types = custom_types or {}

    def has_value(self, value):
        """
        Checks if the given value has a value.

        Args:
            value: The value to be checked.

        Returns:
            True if the value has a value, False otherwise.
        """
        
        # Check for custom data types
        for name, func in self.custom_types.items():
            if func(value):
                return True

        if isinstance(value, (int, float, complex)):
            return value != 0
        elif isinstance(value, str):
            return value != "" and value is not None
        elif isinstance(value, collections.abc.Sequence):
            return len(value) > 0
        elif isinstance(value, collections.abc.Mapping):
            return len(value) > 0
        elif isinstance(value, bool):
            return value
        # Check for any object with a __len__ attribute
        elif hasattr(value, "__len__"):
            return len(value) > 0
        # Fallback for unknown types
        else:
            return False

    def is_type(self, value, type_name):
        """
        Checks if the given value has a value.

        Args:
            value: The value to be checked.

        Returns:
            True if the value has a value, False otherwise.

        Examples:

        ```python
        value = 10
        if data_checker.has_value(value):
            print(f"The value '{value}' has a value.")

        value = ""
        if not data_checker.has_value(value):
            print(f"The value '{value}' has no value.")
        ```
        """
        if type_name in self.default_types:
            return isinstance(value, self.default_types[type_name])
        elif type_name in self.custom_types:
            return self.custom_types[type_name](value)
        else:
            raise ValueError(f"Unknown type: {type_name}")

