"""
Indian Number Format Parser
Handles conversion of Indian numeric format (e.g., "5,47,284") to integers/floats
"""

import re
from typing import Union


def parse_indian_number(value: Union[str, int, float]) -> Union[int, float]:
    """
    Convert Indian formatted number string to numeric type.

    Indian format uses commas every 2 digits (from right, after first 3):
    1 lakh = 1,00,000
    1 crore = 1,00,00,000

    Args:
        value: String ("5,47,284"), int (547284), or float (547284.5)

    Returns:
        Converted numeric value (int or float)

    Examples:
        >>> parse_indian_number("5,47,284")
        547284
        >>> parse_indian_number("1,23,45,678")
        12345678
        >>> parse_indian_number("1,00,000.50")
        100000.5
        >>> parse_indian_number(547284)
        547284
    """
    # If already numeric, return as-is
    if isinstance(value, (int, float)):
        return value

    # If empty or NaN string, return NaN
    if value is None or value == "" or str(value).lower() == "nan":
        return float("nan")

    # Convert to string and strip whitespace
    value_str = str(value).strip()

    # If all commas and digits, it's Indian format
    if re.match(r"^-?\d{1,3}(,\d{2})*(\.\d+)?$", value_str):
        # Remove all commas
        value_str = value_str.replace(",", "")

    # Try to convert to int first, then float if decimal point exists
    try:
        if "." in value_str:
            return float(value_str)
        else:
            return int(value_str)
    except ValueError:
        # If conversion fails, return NaN
        return float("nan")


def parse_indian_number_column(series):
    """
    Apply parse_indian_number to a pandas Series.

    Args:
        series: pandas Series with Indian formatted numbers

    Returns:
        pandas Series with numeric values

    Example:
        >>> df['applications'] = parse_indian_number_column(df['applications'])
    """
    return series.apply(parse_indian_number)


if __name__ == "__main__":
    # Test cases
    test_cases = [
        "5,47,284",
        "1,23,45,678",
        "12,34,567.50",
        "100",
        "1,00,000",
        547284,
        100000.5,
        "",
        "nan",
    ]

    for test in test_cases:
        result = parse_indian_number(test)
        print(f"parse_indian_number({test!r}) = {result}")
