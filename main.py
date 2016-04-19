#!/usr/bin/env python
# -*- coding: utf8 -*-

from __future__ import print_function

import sys
import json

INDENT = 4


def load_file(filename):
    with open(filename, "r") as f:
        # return f.readlines()
        lines = f.readlines()
        for i in xrange(len(lines)):
            if lines[i][-1] == "\n":
                # del lines[i][-1]
                lines[i] = lines[i][:-1]
        return lines


def replace_tab_with_space(line):
    start = None
    for i in xrange(len(line)):
        if not line[i].isspace():
            start = i
            break

    if start is None:
        return line

    line = line[:start].replace("\t", " " * INDENT) + line[start:]
    return line


def depth(line):
    for i in xrange(len(line)):
        c = line[i]
        if not c.isspace():
            assert i % INDENT == 0
            return i / INDENT
    return None


def create_map(lines):
    d = []
    stack = [d]
    last_depth = 0
    for line in lines:
        line_depth = depth(line)
        if line_depth is None:
            continue
        elif line_depth == last_depth:
            stack[-1].append(line.lstrip())
        elif line_depth == last_depth + 1:
            last_depth += 1
            next_level = [line.lstrip()]
            stack[-1].append(next_level)
            stack.append(next_level)
            # pointer = stack[-1]
            # pointer.append(next_level)
        elif line_depth < last_depth:
            for i in xrange(last_depth - line_depth):
                stack = stack[:-1]
            stack[-1].append(line.lstrip())
            last_depth = line_depth
        else:
            raise RuntimeError("Improper indentation for '{}'. Last depth: {}. Depth: {}".format(line, last_depth, line_depth))
    return d


def dictify(mapping):
    d = {}
    i = 0
    # for i in xrange(len(mapping) - 1):
    while i < len(mapping) - 1:
        line = mapping[i]
        next_line = mapping[i + 1]
        if isinstance(next_line, list):
            d[line] = dictify(next_line)
            i += 2
        else:
            d[line] = None
            i += 1
    return d


def main():
    lines = load_file(sys.argv[1])
    for i in xrange(len(lines)):
        lines[i] = replace_tab_with_space(lines[i])

    x = create_map(lines)
    y = dictify(x)
    print(json.dumps(y, indent=4))

    return 0


if __name__ == "__main__":
    sys.exit(main())
