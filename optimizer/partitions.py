"""Generate all partitions of a list of elements.

Adapted from: https://stackoverflow.com/a/20530130/6605349
"""
from typing import Iterable, TypeVar

T = TypeVar('T')

def tuple_partitions(elements: list[T]) -> Iterable[tuple[list[T], list[T]]]:
    if len(elements) < 2:
        return
    for pattern in range(1, 1 << (len(elements) - 1)):
        result_sets: tuple[list[T]] = ([elements[0]], [])
        for i in range(1, len(elements)):
            result_sets[(pattern >> (i - 1)) & 1].append(elements[i])
        yield result_sets

def all_partitions(fixed_parts: list[list[T]],
                   suffix_elements: list[T]) -> Iterable[list[list[T]]]:
    yield fixed_parts + [suffix_elements]
    suffix_partitions = tuple_partitions(suffix_elements)
    for suffix_partition in suffix_partitions:
        yield from all_partitions(fixed_parts + [suffix_partition[0]],
                                  suffix_partition[1])

def partitions(elements: list[T]) -> Iterable[list[list[T]]]:
    return all_partitions([], elements)
