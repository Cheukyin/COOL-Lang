class Expr:
    def __eq__(self, E):
        if type(self) != type(E):
            return false

        for (attr, val) in self.__dict__.items():
            if attr == 'lineno':
                continue

            if val != E.__dict__[attr]:
                return False

        return True

        # return type(self) == type(E) \
        #        and self.__dict__ == E.__dict__


class ListType(list):
    def __init__(self, L, lineno):
        super(ListType, self).__init__(L)
        self.lineno = lineno

    def __eq__(self, L):
        return type(self) == type(L) \
               and super(ListType, self).__eq__(L) \
               and self.__dict__ == L.__dict__

    def __repr__(self):
        return "%s(%s, %s)" \
                % (str(self.__class__).split('.')[1].split("'")[0],
                   super(ListType, self).__repr__(),
                   self.lineno)

class Program(ListType): pass

class Formal(Expr):
    def __init__(self, ID, Type, lineno):
        self.ID = ID
        self.Type = Type
        self.lineno = lineno

    def __repr__(self):
        return "Formal(%s, %s, %s)" \
                % (self.ID, self.Type, self.lineno)

class Attribute(Expr):
    def __init__(self, ID, Type, Value, lineno):
        self.ID = ID
        self.Type = Type
        self.Value = Value
        self.lineno = lineno

    def __repr__(self):
        return "%s(%s, %s, %s, %s)" \
                % (str(self.__class__).split('.')[1].split("'")[0],
                   self.ID, self.Type, self.Value, self.lineno)

class Method(Expr):
    def __init__(self, ID, FormalList, Type, Body, lineno):
        self.ID = ID
        self.FormalList = FormalList
        self.Type = Type
        self.Body = Body
        self.lineno = lineno

    def __repr__(self):
        return "Method(%s, %s, %s, %s, %s)" \
                % (self.ID, self.FormalList,
                   self.Type, self.Body,
                   self.lineno)

class Class(Expr):
    def __init__(self, name, superclass, Attrs, Methods, lineno):
        self.Name = name
        self.Superclass = superclass
        self.AttributeList = Attrs
        self.MethodList = Methods
        self.lineno = lineno

    def __repr__(self):
        return "Class(%s, %s, %s, %s, %s)" \
                % (self.Name, self.Superclass,
                   self.AttributeList, self.MethodList,
                   self.lineno)

class Assignment(Expr):
    def __init__(self, ID, Exp, lineno):
        self.ID = ID
        self.Exp = Exp
        self.lineno = lineno

    def __repr__(self):
        return "Assignment(%s, %s, %s)" \
                % (self.ID, self.Exp, self.lineno)

class DynamicDispatch(Expr):
    def __init__(self, Obj, MethodName, ParamList, lineno):
        self.Obj = Obj
        self.MethodName = MethodName
        self.ParamList = ParamList
        self.lineno = lineno

    def __repr__(self):
        return "DynamicDispatch(%s, %s, %s, %s)" \
                % (self.Obj, self.MethodName, self.ParamList,
                   self.lineno)

class StaticDispatch(Expr):
    def __init__(self, Obj, Type, MethodName, ParamList, lineno):
        self.Obj = Obj
        self.Type = Type
        self.MethodName = MethodName
        self.ParamList = ParamList
        self.lineno = lineno

    def __repr__(self):
        return "StaticDispatch(%s, %s, %s, %s, %s)" \
                % (self.Obj, self.Type,
                   self.MethodName, self.ParamList,
                   self.lineno)

class SelfDispatch(Expr):
    def __init__(self, MethodName, ParamList, lineno):
        self.MethodName = MethodName
        self.ParamList = ParamList
        self.lineno = lineno

    def __repr__(self):
        return "SelfDispatch(%s, %s, %s)" \
                % (self.MethodName, self.ParamList,
                   self.lineno)

class Branch(Expr):
    def __init__(self, Cond, Then, Else, lineno):
        self.Cond = Cond
        self.Then = Then
        self.Else = Else
        self.lineno = lineno

    def __repr__(self):
        return "Branch(%s, %s, %s, %s)" \
                % (self.Cond, self.Then, self.Else,
                   self.lineno)

class Loop(Expr):
    def __init__(self, Cond, Body, lineno):
        self.Cond = Cond
        self.Body = Body
        self.lineno = lineno

    def __repr__(self):
        return "Loop(%s, %s, %s, %s)" \
                % (self.Cond, self.Body, self.lineno)

class Block(ListType): pass

class Binding(Attribute): pass

class Let(Expr):
    def __init__(self, BindingList, Body, lineno):
        self.BindingList = BindingList
        self.Body = Body
        self.lineno = lineno

    def __repr__(self):
        return "Let(%s, %s, %s)" \
                % (self.BindingList, self.Body,
                   self.lineno)

class PatternMatch(Expr):
    def __init__(self, ID, Type, Exp, lineno):
        self.ID = ID
        self.Type = Type
        self.Exp = Exp
        self.lineno = lineno

    def __repr__(self):
        return "PatternMatch(%s, %s, %s, %s)" \
                % (self.ID, self.Type, self,Exp,
                   self.lineno)

class Case(Expr):
    def __init__(self, CaseExp, PatternMatchList, lineno):
        self.CaseExp = CaseExp
        self.PatternMatchList = PatternMatchList
        self.lineno = lineno

    def __repr__(self):
        return "Case(%s, %s, %s)" \
                % (self.CaseExp, self.PatternMatchList,
                   self.lineno)

class UnaryOp(Expr):
    def __init__(self, E, lineno):
        self.E = E
        self.lineno = lineno

    def __repr__(self):
        return "%s(%s, %s)" \
                % (str(self.__class__).split('.')[1].split("'")[0],
                   self.E, self.lineno)

class New(UnaryOp): pass
class IsVoid(UnaryOp): pass
class Negate(UnaryOp): pass
class Not(UnaryOp): pass

class BinaryOp(Expr):
    def __init__(self, E1, E2, lineno):
        self.E1 = E1
        self.E2 = E2
        self.lineno = lineno

    def __repr__(self):
        return "%s(%s, %s, %s)" \
                % (self.__class__, self.E1, self.E2,
                   self.lineno)

class Add(BinaryOp): pass
class Minus(BinaryOp): pass
class Mul(BinaryOp): pass
class Div(BinaryOp): pass
class LessThan(BinaryOp): pass
class LessEqual(BinaryOp): pass
class Equal(BinaryOp): pass

class ATOM(Expr):
    def __init__(self, Value, lineno):
        self.Value = Value
        self.lineno = lineno

class INT(ATOM): pass
class STRING(ATOM): pass
class IDENTIFIER(ATOM): pass
class TRUE(ATOM): pass
class FALSE(ATOM): pass