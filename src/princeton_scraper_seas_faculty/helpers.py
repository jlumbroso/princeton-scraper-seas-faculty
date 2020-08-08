
import typing


__author__ = "Jérémie Lumbroso <lumbroso@cs.princeton.edu>"

__all__ = [
    "split_name",
]


def split_name(name: str) -> typing.Tuple[str, str]:
    """
    Returns a likely `(first, last)` split given a full name. This uses
    very simple heuristics, and assumes Western usage.

    :param name: A full name (first and last name).
    :return: A split pair with the first names, and the last name.
    """
    words = name.split()

    first_bits = words[:-1]
    last_bits = words[-1:]
    while len(first_bits) > 0 and first_bits[-1][0].islower():
        last_bits = [first_bits[-1]] + last_bits
        first_bits = first_bits[:-1]

    first_joined = " ".join(first_bits)
    last_joined = " ".join(last_bits)

    return first_joined, last_joined
