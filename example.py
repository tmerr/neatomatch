from neatomatch import _, freevars, match

_a, _b, _c, _d = freevars(4)

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


def clean(text):
    return text.replace('.', '').split()


def symmetric_action(text):
    return match(clean(text),
                (_a, _b, _c, _c, _b, _a), lambda: True,
                _, lambda: False)

def transitive_action(text):
    return match(clean(text),
                (_a, _b, _c, _c, _b, _), lambda: True,
                _, lambda: False)

def reflexive_action(text):
    return match(clean(text),
                (_a, _b, _a), lambda: True,
                _, lambda: False)

assert symmetric_action('Bob slapped Zach. Zach slapped Bob.')
assert not symmetric_action('Bob slapped Zach. Zach slapped Jim')
assert transitive_action('Bob poked Zach. Zach poked Jim')
assert not transitive_action('Bob poked Zach. Bob poked Jim')
assert reflexive_action('Bob poked Bob')
assert not reflexive_action('Bob poked Jim')
