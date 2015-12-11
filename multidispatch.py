#!/usr/bin/python3

fn_dict = {}

class Name2fn:
    def __init__(self, name):
        self.type2fn = {}

    def register(self, types, fn):
        if types in self.type2fn:
            raise TypeError("duplicate registration")
        self.type2fn[types] = fn

    def __call__(self, *args):
        types = tuple(arg.__class__ for arg in args)
        fn = self.type2fn.get(types)
        if fn is not None:
            return fn(*args)

        for i in range(1, len(args)):
            types = tuple(arg.__class__ for arg in args[0:-i])
            fn = self.type2fn.get(types)
            if fn is not None:
                return fn(*args)

        raise TypeError("no match")



def MultiDispatch(*args):
    def register(fn):
        fn_name = fn.__name__
        fn_map = fn_dict.get(fn_name)

        if fn_map is None:
            fn_map = fn_dict[fn_name] = Name2fn(fn_name)

        fn_map.register(args, fn)
        return fn_map

    return register


if __name__ == "__main__":
    @MultiDispatch(int, int)
    def f(a, b):
        print(a+b)

    @MultiDispatch(int, str)
    def f(a, b):
        print(a, b)

    @MultiDispatch(int, int, str)
    def f(a, b, c):
        print(a+b, c)

    @MultiDispatch(str, int)
    def f(a, b, c):
        print(a, b+c)

    @MultiDispatch(int, int)
    def h(a, b):
        print(a*b)

    @MultiDispatch(int)
    def h(a, b):
        print(a, b)

    f(1, 2)
    f(1, 's')
    f(2, 4, 'f')
    f('w', 3, 3)
    h(3, 5)
    h(3, 'a')