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
    case1 = '''
            class Main inherits IO {
                i:Int;
                b: Int <- (1+2)*3;
            } ;
            '''
    exp1 = Program([Class('Main', 'IO',
                          [Attribute('b', 'Int', Mul(Add(INT(1, 3),
                                                         INT(2,3),
                                                         3),
                                                     INT(3, 3),
                                                     3), 3),
                           Attribute('i', 'Int', None, 3),
                       ],
                          [],
                          2)],
                   0)
    AssertEq(testparser.process(case1), exp1)

    # Case 2


if __name__ == "__main__":
    TestParser()