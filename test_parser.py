#!/usr/bin/python3

import parser
from AST import *

TestNum = 1

def AssertEq(E1, E2):
    global TestNum
    if E1 == E2:
        print("Case %s: OK" % TestNum)
        TestNum += 1
    else:
        print()
        print("Case %s: ERROR!!!" % TestNum)
        print("Parsed Result: ")
        print(E1)
        print("Expected Result: ")
        print(E2)
        print()

def TestParser():
    print("Lexer Test:")

    testparser = parser.CoolParser()
    testparser.build()

    # Case 1
    case = r'''
            class Main inherits IO {
                i:Int;
                main() : Object {
                  out_string("\"Hello, world.\"\n")
                } ;
                b: Int <- (1+2)*3;
            } ;
            '''
    exp = Program([Class('Main', 'IO',
                         [ Attribute('i', 'Int', None, 3),
                           Attribute('b', 'Int', Mul(Add(INT(1, 3),
                                                         INT(2,3),
                                                         3),
                                                     INT(3, 3),
                                                     3), 3),
                       ],
                         [Method('main', [], 'Object',
                                 SelfDispatch('out_string', [STRING(r'\"Hello, world.\"\n', 5)],
                                              5),
                                 4)
                      ],
                         2)],
                  0)
    AssertEq(testparser.process(case), exp)

    testparser.program = Program([], 0)

    # Case 2
    case += r'''
              class A {
                 var : Int <- 0;

                 value() : Int { var };

                 set_var(num : Int) : SELF_TYPE {
                    {
                       var <- num;
                       self;
                    }
                 };

                 method2(num1 : Int, num2 : Int) : B {  -- plus
                    (let x : Int in
                       {
                          x <- num1 + num2;
                          (new B).set_var(x);
                       }
                    )
                 };

                 method4(num1 : Int, num2 : Int) : D {  -- diff
                          if num2 < num1 then
                             (let x : Int in
                                {
                                   x <- num1 - num2;
                                   (new D).set_var(x);
                                }
                             )
                          else
                             (let x : Int in
                                {
                                   x <- num2 - num1;
                                   (new D).set_var(x);
                                }
                             )
                          fi
                 };

                 method5(num : Int) : E {  -- factorial
                    (let x : Int <- 1 in
                       {
                          (let y : Int <- 1 in
                             while y <= num loop
                                {
                                   x <- x * y;
                                   y <- y + 1;
                                }
                             pool
                          );
                          (new E).set_var(x);
                       }
                    )
                 };

              };
             '''
    exp += [Class('A', None,
                  [ Attribute('var', 'Int', INT(0, 0), 0)
                ],
                  [ Method('value', [], 'Int', IDENTIFIER('var', 0), 0),
                    Method('set_var', [Formal('num', 'Int', 0)], 'SELF_TYPE',
                           Block([Assignment('var', IDENTIFIER('num', 0), 0),
                                  IDENTIFIER('self', 0)], 0), 0),
                    Method('method2', [Formal('num1', 'Int', 0),
                                       Formal('num2', 'Int', 0)],
                           'B',
                           Let([Binding('x', 'Int', None, 0)],
                               Block([Assignment('x', Add(IDENTIFIER('num1', 0),
                                                          IDENTIFIER('num2', 0),
                                                          0), 0),
                                      DynamicDispatch(New('B', 0),
                                                      'set_var',
                                                      [IDENTIFIER('x', 0)],
                                                      0)], 0), 0), 0),
                    Method('method4', [Formal('num1', 'Int', 0),
                                       Formal('num2', 'Int', 0)],
                           'D',
                           Branch(LessThan(IDENTIFIER('num2', 0),
                                           IDENTIFIER('num1', 0),
                                           0),
                                  Let([Binding('x', 'Int', None, 0)],
                                      Block([Assignment('x', Minus(IDENTIFIER('num1', 0),
                                                                   IDENTIFIER('num2', 0),
                                                                   0), 0),
                                             DynamicDispatch(New('D', 0),
                                                             'set_var',
                                                             [IDENTIFIER('x', 0)],
                                                             0)], 0), 0),
                                  Let([Binding('x', 'Int', None, 0)],
                                      Block([Assignment('x', Minus(IDENTIFIER('num2', 0),
                                                                   IDENTIFIER('num1', 0),
                                                                   0), 0),
                                             DynamicDispatch(New('D', 0),
                                                             'set_var',
                                                             [IDENTIFIER('x', 0)],
                                                             0)], 0), 0), 0),
                           '0'),
                    Method('method5', [Formal('num', 'Int', 49)],
                           'E',
                           Let([Binding('x', 'Int', INT(1, 50), 50)],
                               Block([Let([Binding('y', 'Int', INT(1, 52), 52)],
                                          Loop(LessEqual(IDENTIFIER('y', 53),
                                                         IDENTIFIER('num', 53),
                                                         0),
                                               Block([Assignment('x', Mul(IDENTIFIER('x', 55),
                                                                          IDENTIFIER('y', 55),
                                                                          0),
                                                                 55),
                                                      Assignment('y', Add(IDENTIFIER('y', 56),
                                                                          INT(1, 56),
                                                                          0),
                                                                 56)],
                                                     0),
                                               53),
                                          52),
                                      DynamicDispatch(New('E', 60),
                                                      'set_var',
                                                      [IDENTIFIER('x', 60)],
                                                      0)],
                                     0),
                               50),
                           49),
                ],
                  10)]
    AssertEq(testparser.process(case), exp)


if __name__ == "__main__":
    TestParser()