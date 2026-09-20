from typing import Tuple, Dict, List
from enum import Enum
import re


class BfresOutput(Enum):
    START = 1
    ELEMENT = 2
    END = 3


delim_start = re.compile(r'^Processing (?P<name>.*)\.\.\.$')
element = re.compile(r'^Saved texture (?P<name>.*)$')
delim_end = re.compile(r'^Saved model (?P<name>.*)$')

HandleBfresResult = Tuple[BfresOutput, str]


def handle_bfres_line(line: str) -> HandleBfresResult | None:
    m = delim_start.match(line)
    if m is not None:
        return BfresOutput.START, m.group('name')

    m = element.match(line)
    if m is not None:
        return BfresOutput.ELEMENT, m.group('name')

    m = delim_end.match(line)
    if m is not None:
        return BfresOutput.END, m.group('name')

    return None


BfresTaskResult = Dict[str, List[str]]


def parse_bfres_stdout(stdout: str) -> Dict[str, List[str]]:
    lines = stdout.strip().split('\n')

    result = {}
    current = None

    for line in lines:
        elem_type, elem = handle_bfres_line(line)

        if elem_type is None:
            continue

        if elem_type is BfresOutput.START:
            current = elem
            result[elem] = []

        if elem_type is BfresOutput.ELEMENT:
            result[current].append(elem)

        if elem_type is BfresOutput.END:
            current = None

    return result
