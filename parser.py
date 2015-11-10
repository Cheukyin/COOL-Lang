#!/usr/bin/python3

import sys, os
import lexer
import ply.yacc as yacc

class CoolParser(object):
    def __init__(self, src, debug = False):
        super(CoolParser, self).__init__()
        self.src = open(src, 'r')

        self.debug = debug
        if debug:
            self.ParseOutput = open('Parse-output-'
                                    + src.split('/')[-1] + '.txt', 'w')

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
        print(p.parser)

    def p_Empty(self, p):
        'Empty :'
        pass

    # Class := class TYPE [inherits TYPE] { feature }
    def p_Class(self, p):
        '''Class : class type inherits type lbrace Feature rbrace
                 | class type lbrace Feature rbrace
        '''
        print(p[1])

    # Feature := id'('[ Formal ]')': TYPE { Expr }; Feature
    #          | id: TYPE [<- Expr]; Feature
    #          | Empty
    def p_Feature(self, p):
        '''Feature : Attribute Feature
                   | Method Feature
                   | Empty
        '''
        print(p.parser)

    def p_Attribute(self, p):
        '''Attribute : identifier colon type semi
                     | identifier colon type larrow Expr semi
        '''
        print(p.parser)

    def p_Method(self, p):
        '''Method : identifier lparen rparen colon type lbrace Expr rbrace semi
                  | identifier lparen Formal rparen colon type lbrace Expr rbrace semi
        '''
        print(p.parser)

    # Formal := id: TYPE
    #         | id: TYPE, Formal
    def p_Formal(self, p):
        '''Formal : identifier colon type
                  | identifier colon type comma Formal
        '''
        print(p.parser)

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
        print(p.parser)

    def p_Assignment(self, p):
        '''Assignment : identifier larrow Expr'''
        print(p.parser)

    def p_DynamicDispatch(self, p):
        '''DynamicDispatch : Expr dot identifier lparen rparen
                           | Expr dot identifier lparen MultiParam rparen
        '''
        print(p.parser)

    def p_StaticDispatch(self, p):
        '''StaticDispatch : Expr at type dot identifier lparen rparen
                          | Expr at type dot identifier lparen MultiParam rparen
        '''
        print(p.parser)

    def p_SelfDispatch(self, p):
        '''SelfDispatch : identifier lparen rparen
                        | identifier lparen MultiParam rparen
        '''
        print(p.parser)

    def p_Branch(self, p):
        '''Branch : if Expr then Expr else Expr fi'''
        print(p.parser)

    def p_Loop(self, p):
        '''Loop : while Expr loop Expr pool'''
        print(p.parser)

    def p_Block(self, p):
        '''Block : lbrace MultiExpr rbrace'''
        print(p.parser)

    def p_Let(self, p):
        '''Let : let LetParam in Expr'''
        print(p.parser)

    def p_Case(self, p):
        '''Case : case Expr of PattenMatchExpr esac'''
        print(p.parser)

    def p_New(self, p):
        '''New : new type'''
        print(p[2])

    def p_IsVoid(self, p):
        '''IsVoid : isvoid Expr'''
        print(p.parser)

    def p_Add(self, p):
        '''Add : Expr plus Expr'''
        print(p.parser)

    def p_Minus(self, p):
        '''Minus : Expr minus Expr'''
        print(p.parser)

    def p_Mul(self, p):
        '''Mul : Expr times Expr'''
        print(p.parser)

    def p_Div(self, p):
        '''Div : Expr divide Expr'''
        print(p.parser)

    def p_Negate(self, p):
        '''Negate : tilde Expr'''
        print(p.parser)

    def p_LessThan(self, p):
        '''LessThan : Expr lt Expr'''
        print(p.parser)

    def p_LessEqual(self, p):
        '''LessEqual : Expr le Expr'''
        print(p.parser)

    def p_Equal(self, p):
        '''Equal : Expr equals Expr'''
        print(p.lexer)

    def p_Not(self, p):
        '''Not : not Expr'''
        print(p.parser)

    def p_ParenExpr(self, p):
        '''ParenExpr : lparen Expr rparen'''
        print(p.parser)

    def p_Int(self, p):
        '''Int : integer'''
        print(p.parser)

    def p_String(self, p):
        '''String : string'''
        print(p[1])

    def p_ID(self, p):
        '''ID : identifier'''
        print(p[1])

    def p_True(self, p):
        '''True : true'''
        print(p[1])

    def p_False(self, p):
        '''False : false'''
        print(p.parser)

    # LetParam := id: TYPE [<- Expr] [, id: TYPE [<- Expr] ]*
    def p_LetParam(self, p):
        '''LetParam : identifier colon type
                    | identifier colon type larrow Expr
                    | identifier colon type LetParam
                    | identifier colon type larrow Expr LetParam
        '''
        print(p.parser)

    def p_PattenMatchExpr(self, p):
        '''PattenMatchExpr : identifier colon type rarrow Expr semi
                           | identifier colon type rarrow Expr semi PattenMatchExpr
        '''
        print(p.parser)

    # MultiParam := Expr [, Expr]*
    def p_MultiParam(self, p):
        '''MultiParam : Expr
                      | Expr comma MultiParam
        '''
        print(p.parser)

    # MultiExpr := [Expr;]+
    def p_MultiExpr(self, p):
        '''MultiExpr : Expr semi
                     | Expr semi MultiExpr
        '''
        print(p.parser)

    def p_error(self, p):
        print("Syntax error in input: %s" % p)

    # Build the parser
    def build(self):
        self.tokens = lexer.CoolLexer.tokens
        self.parser = yacc.yacc(module=self)

    def process(self):
        coollexer = lexer.CoolLexer()
        coollexer.build()   # Build the lexer
        self.parser.parse(self.src.read(), coollexer.lexer)


if __name__ == '__main__':
    # Build the parser and try it out
    parser = CoolParser( src = sys.argv[1], debug = True)
    parser.build()   # Build the lexer
    parser.process()