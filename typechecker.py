#!/usr/bin/python3

from AST import *

class TypeChecker:
    def __init__(self, ast):
        self.ast = ast

        # [attr type, lineno]
        self.class2attr = {}

        # [[result type, [formal type]], lineno]
        self.class2method = \
        {
            'Object':
            {
                'abort':     [['Object',    []], 0],
                'type_name': [['String',    []], 0],
                'copy':      [['SELF_TYPE', []], 0],
            },
            'IO':
            {
                'out_string': [['SELF_TYPE', ['String']], 0],
                'out_int':    [['SELF_TYPE', ['Int']],    0],
                'in_string':  [['String',    []],         0],
                'in_int':     [['Int',       []],         0],
            },
            'String':
            {
                'length': [['Int',    []],             0],
                'concat': [['String', ['String']],     0],
                'substr': [['String', ['Int', 'Int']], 0],
            }
        }

        self.inheritance_graph = \
        {
            'Object': None,
            'IO':     'Object',
            'Int':    'Object',
            'String': 'Object',
            'Bool':   'Object',
        }

        # [class name, lineno]
        self.class2lineno = \
        {
            'Object': 0,
            'IO':     0,
            'String': 0,
            'Int':    0,
            'Bool':   0,
        }

        self.final_class = set(['Int', 'String', 'Bool'])


    def attr_collect(self, clsname, attrlist):
        attr_dict = self.class2attr[clsname] = {}

        for attr in attrlist:
            name = attr.ID

            if name in attr_dict:
                raise TypeError( "attr redefined: %s.%s in lineno %s"
                                 % (clsname, name, attr.lineno) )

            attr_dict[name] = [attr.Type, attr.lineno]

    def method_collect(self, clsname, methodlist):
        method_dict = self.class2method[clsname] = {}

        for method in methodlist:
            name = method.ID
            result_type = method.Type

            if name in method_dict:
                raise TypeError( "method redefined: %s.%s in lineno %s"
                                 % (clsname, name, method.lineno) )

            formal_type = [formal.Type for formal in method.FormalList]
            method_dict[name] = [[result_type, formal_type], method.lineno]

    def type_collect(self):
        for cls in self.ast:
            name = cls.Name
            superclass = cls.Superclass
            attrlist = cls.AttributeList
            methodlist = cls.MethodList

            if name in self.class2lineno:
                raise TypeError( "class redefined: %s in lineno %s"
                                 % (name, cls.lineno) )

            self.class2lineno[name] = cls.lineno
            self.inheritance_graph[name] = superclass or 'Object'
            self.attr_collect(name, attrlist)
            self.method_collect(name, methodlist)


    def detect_inheritance_validation(self):
        inherit_final_err = []
        inherit_undeclared_err = []

        for cls, inherit_cls in self.inheritance_graph.items():
            if inherit_cls in self.final_class:
                inherit_final_err.append([cls, inherit_cls])

            if inherit_cls not in self.class2lineno:
                inherit_undeclared_err.append([cls, inherit_cls])

        if inherit_final_err != []:
            raise TypeError( "inherit from final class %s"
                             + str(inherit_final_err) )

        if inherit_undeclared_err != []:
            raise TypeError("inherit from undeclared class "
                            + str(inherit_undeclared_err))


    def detect_inheritance_cycle(self):
        is_visited = {}
        for cls in self.inheritance_graph:
            is_visited[cls] = False

        for cls in self.inheritance_graph:
            if is_visited[cls]:
                continue

            inherit_path = [cls]

            # collision point: y = f^n(x) = f^(2n+1)(x)
            slow = cls
            fast = self.inheritance_graph[cls]

            is_visited[slow] = True
            inherit_path.append(fast)

            is_cyclic = True
            while fast != slow:
                slow = self.inheritance_graph[slow]

                if fast is None or is_visited[fast]:
                    is_cyclic = False
                    break

                is_visited[fast] = True
                fast = self.inheritance_graph[fast]
                inherit_path.append(fast)

                if fast is None or is_visited[fast]:
                    is_cyclic = False
                    break

                is_visited[fast] = True
                fast = self.inheritance_graph[fast]
                inherit_path.append(fast)

            if not is_cyclic:
                continue

            raise TypeError("inheritance cycle: "
                            + str(inherit_path))


    def check_main_validation(self):
        if 'Main' not in self.inheritance_graph:
            raise TypeError("class Main not defined")
        if 'main' not in self.class2method['Main']:
            raise TypeError("Main.main is not defined")
        if self.class2method['Main']['main'][0][1] != []:
            raise TypeError("Main.main should not take any formals")