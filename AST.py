class ListType(list):
    def __init__(self, L, lineno):
        super(ListType, self).__init__(L)
        self.lineno = lineno

class Program(ListType): pass

class Formal:
    def __init__(self, ID, Type, lineno):
        self.ID = ID
        self.Type = Type
        self.lineno = lineno

class Attribute:
    def __init__(self, ID, Type, Value, lineno):
        self.ID = ID
        self.Type = Type
        self.Value = Value
        self.lineno = lineno

class Method:
    def __init__(self, ID, FormalList, Type, Body, lineno):
        self.ID = ID
        self.FormalList = FormalList
        self.Type = Type
        self.Body = Body
        self.lineno = lineno

class Class:
    def __init__(self, name, superclass, Attrs, Methods, lineno):
        self.Name = name
        self.Superclass = superclass
        self.AttributeList = Attrs
        self.MethodList = Methods
        self.lineno = lineno

class Assignment:
    def __init__(self, ID, Exp, lineno):
        self.ID = ID
        self.Exp = Exp
        self.lineno = lineno

class DynamicDispatch:
    def __init__(self, Obj, MethodName, ParamList, lineno):
        self.Obj = Obj
        self.MethodName = MethodName
        self.ParamList = ParamList
        self.lineno = lineno

class StaticDispatch:
    def __init__(self, Obj, Type, MethodName, ParamList, lineno):
        self.Obj = Obj
        self.Type = Type
        self.MethodName = MethodName
        self.ParamList = ParamList
        self.lineno = lineno

class SelfDispatch:
    def __init__(self, MethodName, ParamList, lineno):
        self.MethodName = MethodName
        self.ParamList = ParamList
        self.lineno = lineno

class Branch:
    def __init__(self, Cond, Then, Else, lineno):
        self.Cond = Cond
        self.Then = Then
        self.Else = Else
        self.lineno = lineno

class Loop:
    def __init__(self, Cond, Body, lineno):
        self.Cond = Cond
        self.Body = Body
        self.lineno = lineno

class Block(ListType): pass

class Binding(Attribute): pass

class Let:
    def __init__(self, BindingList, Body, lineno):
        self.BindingList = BindingList
        self.Body = Body
        self.lineno = lineno

class PatternMatch:
    def __init__(self, ID, Type, Exp, lineno):
        self.ID = ID
        self.Type = Type
        self.Exp = Exp
        self.lineno = lineno

class Case:
    def __init__(self, CaseExp, PatternMatchList, lineno):
        self.CaseExp = CaseExp
        self.PatternMatchList = PatternMatchList
        self.lineno = lineno

class UnaryOp:
    def __init__(self, E, lineno):
        self.E = E
        self.lineno = lineno

class New(UnaryOp): pass
class IsVoid(UnaryOp): pass
class Negate(UnaryOp): pass
class Not(UnaryOp): pass

class BinaryOp:
    def __init__(self, E1, E2, lineno):
        self.E1 = E1
        self.E2 = E2
        self.lineno = lineno

class Add(BinaryOp): pass
class Minus(BinaryOp): pass
class Mul(BinaryOp): pass
class Div(BinaryOp): pass
class LessThan(BinaryOp): pass
class LessEqual(BinaryOp): pass
class Equal(BinaryOp): pass

class ATOM:
    def __init__(self, Value, lineno):
        self.Value = Value
        self.lineno = lineno

class INT(ATOM): pass
class STRING(ATOM): pass
class IDENTIFIER(ATOM): pass
class TRUE(ATOM): pass
class FALSE(ATOM): pass