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
    def __init__(self, ID, Type, Init, lineno):
        self.ID = ID
        self.Type = Type
        self.Init = Init
        self.lineno = lineno

class Method:
    def __init__(self, ID, FormalList, Body, lineno):
        self.ID = ID
        self.FormalList = FormalList
        self.Body = Body
        self.lineno = lineno

class Class:
    def __init__(self, name, superclass, Attrs, Methods, lineno):
        self.Name = name
        self.Superclass = superclass
        self.Attributes = Attrs
        self.Methods = Methods
        self.lineno = lineno

class Assignment:
    def __init__(self, ID, Exp):
        self.ID = ID
        self.Exp = Exp

class DynamicDispatch:
    def __init__(self, Obj, MethodName, ParamList):
        self.Obj = Obj
        self.MethodName = MethodName
        self.ParamList = ParamList

class StaticDispatch:
    def __init__(self, Obj, Type, MethodName, ParamList):
        self.Obj = Obj
        self.Type = Type
        self.MethodName = MethodName
        self.ParamList = ParamList

class SelfDispatch:
    def __init__(self, MethodName, ParamList):
        self.MethodName = MethodName
        self.ParamList = ParamList

class Branch:
    def __init__(self, Cond, Then, Else):
        self.Cond = Cond
        self.Then = Then
        self.Else = Else

class Loop:
    def __init__(self, Cond, Body):
        self.Cond = Cond
        self.Body = Body

class Block(ListType): pass

class Binding(Attribute): pass

class Let:
    def __init__(self, BindingList, Body):
        self.BindingList = BindingList
        self.Body = Body

class PatternMatch:
    def __init__(self, ID, Type, Exp):
        self.ID = ID
        self.Type = Type
        self.Exp = Exp

class Case:
    def __init__(self, CaseExp, PatternMatchList):
        self.CaseExp = CaseExp
        self.PattenMatchList = PattenMatchExprList

class UnaryOp:
    def __init__(self, E):
        self.E = E

class New(UnaryOp): pass
class IsVoid(UnaryOp): pass
class Negate(UnaryOp): pass
class Not(UnaryOp): pass

class BinaryOp:
    def __init__(self, E1, E2):
        self.E1 = E1
        self.E2 = E2

class Add(BinaryOp): pass
class Minus(BinaryOp): pass
class Mul(BinaryOp): pass
class Div(BinaryOp): pass
class LessThan(BinaryOp): pass
class LessEqual(BinaryOp): pass
class Equal(BinaryOp): pass

class ATOM:
    def __init__(self, Value):
        self.Value = Value

class INT(ATOM): pass
class STRING(ATOM): pass
class IDENTIFIER(ATOM): pass
class TRUE(ATOM): pass
class FALSE(ATOM): pass