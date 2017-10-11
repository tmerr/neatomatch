# A successful match binds variables to a dictionary that maps numeric IDs to
# values. These dictionaries are pushed onto a stack to support a match calling
# a match, like during recursion.
envstack = []

class FreeVar:
    def __init__(self, id):
        self.freevarid = id

    def __invert__(self):
        # This squiggly operator ~ feels like a dereference
        try:
            return envstack[-1][self.freevarid]
        except KeyError:
            raise UnboundVariable("tried to look up variable; not bound in pattern")


# Wildcard
_ = FreeVar(-1)


def freevars(n):
    return tuple([FreeVar(i) for i in range(n)])


class NoMatch(Exception):
    pass


class UnboundVariable(Exception):
    pass


def bindfreevars(pat, arg, env):
    """Bind free variables to the environment"""
    if pat == arg:
        pass
    elif hasattr(pat, 'freevarid'):
        if pat.freevarid == _.freevarid:
            pass
        if pat.freevarid in env and env[pat.freevarid] != arg:
            raise NoMatch
        else:
            env[pat.freevarid] = arg
    else:
        try:
            if len(pat) != len(arg):
                raise NoMatch
        except TypeError:
            raise NoMatch
        else:
            for p, a in zip(pat, arg):
                if a == arg:
                    # don't infinitely recurse
                    # for one char strings
                    raise NoMatch
                bindfreevars(p, a, env)


def match(arg, *arms):
    """Pattern match and throw an exception upon failure"""
    for (pat, func) in zip(arms[0::2], arms[1::2]):
        envstack.append({})
        try:
            bindfreevars(pat, arg, envstack[-1])
            return func()
        except NoMatch:
            continue
        finally:
            envstack.pop()
    raise NoMatch


def maybematch(arg, *arms):
    """Pattern match and return None upon failure"""
    try:
        return match(arg, *arms)
    except NoMatch:
        pass
