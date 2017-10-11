# Python Pattern Matching

    from neatomatch import _, freevars, match

    _a, _b = freevars(2)

    def evaltree(tree):
        return match(tree,
                    ('+', _a, _b),
                        lambda: evaltree(~_a) + evaltree(~_b),
                    ('*', _a, _b),
                        lambda: evaltree(~_a) * evaltree(~_b),
                    _a,
                        lambda: ~_a)
    
    binarytree = ('+', 3, ('*', ('+', 1, 1), 5))
    assert 13 == evaltree(binarytree)
    
- Matches based on`__len__` and `__iter__` recursively checking for matching leaves. Actual types don't matter.
- Uses `_` to match anything
- The pattern `(_a, _a)` matches `(3, 3)` but not `(3, 4)`
- The implementation is tiny

It's mostly for fixed length sequences, but can operate on variable length things with the help of slices:

    def sum(xs):
        return match((xs[0], xs[1:]),
          (_a, []), lambda: ~_a,
          (_a, _b), lambda: ~_a + sum(~_b))
