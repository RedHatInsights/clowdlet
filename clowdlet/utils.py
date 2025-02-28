"""Miscellaneous utility functions."""
import re

TEMPLATE_VAR_PATTERN = re.compile(r"(\$\{\{?(\w+)\}?\})")


def replace_vars(input_s: str, params: dict[str, str]) -> str:
    """Replace all variables found in input_s with values from params dict."""
    for variable, param_name in TEMPLATE_VAR_PATTERN.findall(input_s):
        input_s = input_s.replace(variable, params[param_name])
    return input_s
