"Scientists were so preoccupied with whether or not they could, they didn’t stop to think if they should" - Dr Ian Malcolm

# Python Pattern Matching

    from neatomatch import _, freevars, match, lookup
    
    _a, _b = freevars(2)
    
    def evaltree(tree):
        return match(tree,
                    ('+', _a, _b),
                        lambda: evaltree(lookup(_a)) + evaltree(lookup(_b)),
                    ('*', _a, _b),
                        lambda: evaltree(lookup(_a)) * evaltree(lookup(_b)),
                    _a,
                        lambda: lookup(_a))
    
    binarytree = ('+', 3, ('*', ('+', 1, 1), 5))
    assert 13 == evaltree(binarytree)
    
- Matches based on`__len__` and `__iter__` recursively checking for matching leaves. Actual types don't matter.
- Uses `_` to match anything
- The pattern `(_a, _a)` matches `(3, 3)` but not `(3, 4)`
- The implementation is tiny

It's mostly for fixed length sequences, but can operate on variable length things with the help of slices:

    def sum(xs):
        return match((xs[0], xs[1:]),
          (_a, []), lambda: lookup(_a),
          (_a, _b), lambda: lookup(_a) + sum(lookup(_b)))
