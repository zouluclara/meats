#!/usr/bin/env python

import sys

MARKED = '#'
EXCLUDED = 'X'
EMPTY = '.'


def main():
    if len(sys.argv) < 3:
        print('Usage: nonogram.py SIZE NUMBERS...')
        exit()

    size = int(sys.argv[1])
    numbers = list(map(int, sys.argv[2:]))

    if size <= 0 or any(x <= 0 for x in numbers):
        print('All parameters must be positive integers.')
        exit()

    if size < packed_size(numbers):
        print('Size too small to fit')
        exit()

    results = list(nonogram(size, numbers))
    was_marked = [False] * size
    was_empty = [False] * size
    print('There are {0} possibilities:'.format(len(results)))
    for result in results:
        assert len(result) == size
        print(result)
        was_empty = new_mask(result, EMPTY, was_empty)
        was_marked = new_mask(result, MARKED, was_marked)
    print('|'*size)
    suggested = sure_result(was_empty, was_marked)
    if suggested == EMPTY * size:
        print('Bad - no suggestions for any field')
        return
    print('Suggested squares:')
    print(suggested)
    print('Or vertically:')
    for c in suggested:
        print(c)


def sure_result(was_empty, was_marked):
    return ''.join(
        EMPTY if empty and marked else (
            EXCLUDED if empty else MARKED
            )
        for empty, marked in zip(was_empty, was_marked)
    )


def new_mask(result, character, prev_mask):
    return [ prev or current
            for prev, current in zip(
                    prev_mask,
                    [ x == character for x in result]
                )
            ]

def packed_size(elements):
    return sum(elements) + len(elements) - 1


def nonogram(size, elements, min_slack=0):
    if elements == []:
        yield EMPTY * size
        return
    
    max_slack = size - packed_size(elements)
    
    for slack in range(min_slack, max_slack+1):
        new_size = size - slack - elements[0]
        new_elements = elements[1:]
        prefix = EMPTY * slack + MARKED * elements[0]
        
        for result in nonogram(new_size, new_elements, 1):
            yield prefix + result


if __name__ == '__main__':
    main()