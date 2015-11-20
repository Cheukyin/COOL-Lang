#!/usr/bin/python3

import sys, os
import AST
import lexer
import ply.yacc as yacc

class CoolParser(object):
    def __init__(self):
        super(CoolParser, self).__init__()
        self.program = AST.Program([], 0)

    precedence = (
        ('right', 'larrow'), # <-
        ('right', 'not'), # not
        ('nonassoc', 'lt', 'le', 'equals'), # <= < =
        ('left', 'plus', 'minus'), # + -
        ('left', 'times', 'divide'), # * /
        ('right', 'isvoid'), # isvoid
        ('right', 'tilde'), # tilde
        ('nonassoc', 'at'), # @
        ('left', 'dot'), # .
    )

    # Program := [class;]+
    def p_Program(self, p):
        '''Program : Class semi
                   | Class semi Program
        '''
        self.program = AST.Program( [ p[1] ], p.lineno(1) ) + self.program

    # Class := class TYPE [inherits TYPE] { feature }
    def p_Class(self, p):
        '''Class : class type inherits type lbrace Feature rbrace
                 | class type inherits type lbrace rbrace
                 | class type lbrace Feature rbrace
                 | class type lbrace rbrace
        '''
        if len(p) == 8:
            p[0] = AST.Class( name = p[2], superclass = p[4],
                              Attrs = p[6][0], Methods = p[6][1],
                              lineno = p.lineno(1) )
        elif len(p) == 7:
            p[0] = AST.Class( name = p[2], superclass = p[4],
                              Attrs = [], Methods = [],
                              lineno = p.lineno(1) )
        elif len(p) == 6:
            p[0] = AST.Class( name = p[2], superclass = None,
                              Attrs = p[4][0], Methods = p[4][1],
                              lineno = p.lineno(1) )
        else:
            p[0] = AST.Class( name = p[2], superclass = None,
                              Attrs = [], Methods = [],
                              lineno = p.lineno(1) )

    # Feature := id'('[ Formal ]')': TYPE { Expr }; Feature
    #          | id: TYPE [<- Expr]; Feature
    def p_Feature(self, p):
        '''Feature : Attribute Feature
                   | Method Feature
                   | Method
                   | Attribute
        '''
        if len(p) == 2:
            if type(p[1]) == AST.Attribute:
                p[0] = [ [ p[1] ], [] ]
            else:
                p[0] = [ [], [ p[1] ] ]
        else:
            if type(p[1]) == AST.Attribute:
                p[2][0] = [ p[1] ] + p[2][0]
            else:
                p[2][1] = [ p[1] ] + p[2][1]

            p[0] = p[2]

    def p_Attribute(self, p):
        '''Attribute : identifier colon type semi
                     | identifier colon type larrow Expr semi
        '''
        if len(p) == 5:
            p[0] = AST.Attribute( ID = p[1], Type = p[3], Value = None,
                                  lineno = p.lineno(1) )
        else:
            p[0] = AST.Attribute( ID = p[1], Type = p[3], Value = p[5],
                                  lineno = p.lineno(1) )

    def p_Method(self, p):
        '''Method : identifier lparen rparen colon type lbrace Expr rbrace semi
                  | identifier lparen Formal rparen colon type lbrace Expr rbrace semi
        '''
        if len(p) == 10:
            p[0] = AST.Method( ID = p[1], FormalList = [], Type = p[5],
                               Body = p[7], lineno = p.lineno(1) )
        else:
            p[0] = AST.Method( ID = p[1], FormalList = p[3], Type = p[6],
                               Body = p[8], lineno = p.lineno(1) )

    # Formal := id: TYPE
    #         | id: TYPE, Formal
    def p_Formal(self, p):
        '''Formal : identifier colon type
                  | identifier colon type comma Formal
        '''
        if len(p) == 4:
            p[0] = [ AST.Formal( ID = p[1], Type = p[3],
                                 lineno = p.lineno(1) ) ]
        else:
            p[0] = [ AST.Formal( ID = p[1], Type = p[3],
                                 lineno = p.lineno(1) )
                   ] + p[5]

    def p_Expr(self, p):
        '''Expr : Assignment
                | DynamicDispatch
                | StaticDispatch
                | SelfDispatch
                | Branch
                | Loop
                | Block
                | Let
                | Case
                | New
                | IsVoid
                | Add
                | Minus
                | Mul
                | Div
                | Negate
                | LessThan
                | LessEqual
                | Equal
                | Not
                | ParenExpr
                | Int
                | String
                | ID
                | True
                | False
        '''
        p[0] = p[1]

    def p_Assignment(self, p):
        '''Assignment : identifier larrow Expr'''
        p[0] = AST.Assignment( ID = p[1], Exp = p[3],
                               lineno = p.lineno(1) )

    def p_DynamicDispatch(self, p):
        '''DynamicDispatch : Expr dot identifier lparen rparen
                           | Expr dot identifier lparen MultiParam rparen
        '''
        if len(p) == 6:
            p[0] = AST.DynamicDispatch( Obj = p[1], MethodName = p[3],
                                        ParamList = [],
                                        lineno = p.lineno(1) )
        else:
            p[0] = AST.DynamicDispatch( Obj = p[1], MethodName = p[3],
                                        ParamList = p[5],
                                        lineno = p.lineno(1) )

    def p_StaticDispatch(self, p):
        '''StaticDispatch : Expr at type dot identifier lparen rparen
                          | Expr at type dot identifier lparen MultiParam rparen
        '''
        if len(p) == 8:
            p[0] = AST.StaticDispatch( Obj = p[1], Type = p[3],
                                       MethodName = p[5], ParamList = [],
                                       lineno = p.lineno(1) )
        else:
            p[0] = AST.StaticDispatch( Obj = p[1], Type = p[3],
                                       MethodName = p[5], ParamList = p[7],
                                       lineno = p.lineno(1) )

    def p_SelfDispatch(self, p):
        '''SelfDispatch : identifier lparen rparen
                        | identifier lparen MultiParam rparen
        '''
        if len(p) == 4:
            p[0] = AST.SelfDispatch( MethodName = p[1], ParamList = [],
                                     lineno = p.lineno(1) )
        else:
            p[0] = AST.SelfDispatch( MethodName = p[1], ParamList = p[3],
                                     lineno = p.lineno(1) )

    def p_Branch(self, p):
        '''Branch : if Expr then Expr else Expr fi'''
        p[0] = AST.Branch( Cond = p[2], Then = p[4], Else = p[6],
                           lineno = p.lineno(1) )

    def p_Loop(self, p):
        '''Loop : while Expr loop Expr pool'''
        p[0] = AST.Loop( Cond = p[2], Body = p[4],
                         lineno = p.lineno(1) )

    def p_Block(self, p):
        '''Block : lbrace MultiExpr rbrace'''
        p[0] = p[2]

    def p_Let(self, p):
        '''Let : let LetParam in Expr'''
        p[0] = AST.Let( BindingList = p[2], Body = p[4],
                        lineno = p.lineno(1) )

    def p_Case(self, p):
        '''Case : case Expr of PattenMatchExpr esac'''
        p[0] = AST.Case( CaseExp = p[2], PatternMatchList = p[4],
                         lineno = p.lineno(1) )

    def p_New(self, p):
        '''New : new type'''
        p[0] = AST.New( E = p[2], lineno = p.lineno(1) )

    def p_IsVoid(self, p):
        '''IsVoid : isvoid Expr'''
        p[0] = AST.IsVoid( E = p[2], lineno = p.lineno(1) )

    def p_Add(self, p):
        '''Add : Expr plus Expr'''
        p[0] = AST.Add( E1 = p[1], E2 = p[3],
                        lineno = p.lineno(1) )

    def p_Minus(self, p):
        '''Minus : Expr minus Expr'''
        p[0] = AST.Minus( E1 = p[1], E2 = p[3],
                          lineno = p.lineno(1) )

    def p_Mul(self, p):
        '''Mul : Expr times Expr'''
        p[0] = AST.Mul( E1 = p[1], E2 = p[3],
                        lineno = p.lineno(1) )

    def p_Div(self, p):
        '''Div : Expr divide Expr'''
        p[0] = AST.Div( E1 = p[1], E2 = p[3],
                        lineno = p.lineno(1) )

    def p_Negate(self, p):
        '''Negate : tilde Expr'''
        p[0] = AST.Negate( E = p[2], lineno = p.lineno(1) )

    def p_LessThan(self, p):
        '''LessThan : Expr lt Expr'''
        p[0] = AST.LessThan( E1 = p[1], E2 = p[3],
                             lineno = p.lineno(1) )

    def p_LessEqual(self, p):
        '''LessEqual : Expr le Expr'''
        p[0] = AST.LessEqual( E1 = p[1], E2 = p[3],
                              lineno = p.lineno(1) )

    def p_Equal(self, p):
        '''Equal : Expr equals Expr'''
        p[0] = AST.Equal( E1 = p[1], E2 = p[3],
                          lineno = p.lineno(1) )

    def p_Not(self, p):
        '''Not : not Expr'''
        p[0] = AST.Not( E = p[2], lineno = p.lineno(1) )

    def p_ParenExpr(self, p):
        '''ParenExpr : lparen Expr rparen'''
        p[0] = p[2]

    def p_Int(self, p):
        '''Int : integer'''
        p[0] = AST.INT( Value = p[1], lineno = p.lineno(1) )

    def p_String(self, p):
        '''String : string'''
        p[0] = AST.STRING( Value = p[1], lineno = p.lineno(1) )

    def p_ID(self, p):
        '''ID : identifier'''
        p[0] = AST.IDENTIFIER( Value = p[1], lineno = p.lineno(1) )

    def p_True(self, p):
        '''True : true'''
        p[0] = AST.TRUE( Value = p[1], lineno = p.lineno(1) )

    def p_False(self, p):
        '''False : false'''
        p[0] = AST.FALSE( Value = p[1], lineno = p.lineno(1) )

    # LetParam := id: TYPE [<- Expr] [, id: TYPE [<- Expr] ]*
    def p_LetParam(self, p):
        '''LetParam : identifier colon type
                    | identifier colon type larrow Expr
                    | identifier colon type LetParam
                    | identifier colon type larrow Expr LetParam
        '''
        if len(p) == 4:
            p[0] = [ AST.Binding( ID = p[1], Type = p[3],
                                  Value = None,
                                  lineno = p.lineno(1) ) ]
        elif len(p) == 6:
            p[0] = [ AST.Binding( ID = p[1], Type = p[3],
                                  Value = p[5],
                                  lineno = p.lineno(1) ) ]
        elif len(p) == 5:
            p[0] = [ AST.Binding( ID = p[1], Type = p[3],
                                  Value = None,
                                  lineno = p.lineno(1) )
                   ] + p[4]
        else:
            p[0] = [ AST.Binding( ID = p[1], Type = p[3],
                                  Value = p[5],
                                  lineno = p.lineno(1) )
                   ] + p[6]

    def p_PattenMatchExpr(self, p):
        '''PattenMatchExpr : identifier colon type rarrow Expr semi
                           | identifier colon type rarrow Expr semi PattenMatchExpr
        '''
        if len(p) == 7:
            p[0] = [ AST.PatternMatch( ID = p[1], Type = p[3],
                                       Exp = p[5],
                                       lineno = p.lineno(1) ) ]
        else:
            p[0] = [ AST.PatternMatch( ID = p[1], Type = p[3],
                                       Exp = p[5],
                                       lineno = p.lineno(1) )
                   ] + p[7]

    # MultiParam := Expr [, Expr]*
    def p_MultiParam(self, p):
        '''MultiParam : Expr
                      | Expr comma MultiParam
        '''
        if len(p) == 2:
            p[0] = [ p[1] ]
        else:
            p[0] = [ p[1] ] + p[3]

    # MultiExpr := [Expr;]+
    def p_MultiExpr(self, p):
        '''MultiExpr : Expr semi
                     | Expr semi MultiExpr
        '''
        if len(p) == 3:
            p[0] = AST.Block( [ p[1] ], lineno = p.lineno(1) )
        else:
            p[0] = AST.Block( [ p[1] ], lineno = p.lineno(1) ) + p[3]

    def p_error(self, p):
        print("Syntax error in input: %s" % p)

    # Build the parser
    def build(self):
        self.tokens = lexer.CoolLexer.tokens
        self.parser = yacc.yacc(module=self)

    def process(self, src):
        coollexer = lexer.CoolLexer()
        coollexer.build()   # Build the lexer
        self.parser.parse(src, coollexer.lexer)
        return self.program


if __name__ == '__main__':
    # Build the parser and try it out
    parser = CoolParser()
    parser.build()   # Build the lexer
    # parser.process( open(sys.argv[1], 'r').read() )
    parser.process(
        '''
        class Main inherits IO {
            i:Int;
        } ;
        '''
    )
    print(parser.program)