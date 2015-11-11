#!/usr/bin/python3

import lexer
import os
import glob


def TestLexer():
    print('============================================================================')
    print("Lexer Test:")

    src_dir = 'cool-examples'
    for cl_path in glob.glob( src_dir+os.sep+"*.cl" ):
        cllex = lexer.CoolLexer( src = cl_path, debug = True)
        cllex.build()   # Build the lexer
        cllex.process()

        cl = cl_path.split(os.sep)[-1]
        cool_lex_output = cl + '.cl-lex'
        my_lex_output = 'lex-output-' + cl + '.txt'
        os.system('./cool --out ' + cl + ' --lex ' + cl_path)
        compared_result = os.popen('diff -s ' + my_lex_output + ' ' + cool_lex_output)
        compared_result = compared_result.read().split('\n')[0]

        if 'are identical' in compared_result:
            print(cl + ': ' + 'OK')
            os.system('rm ' + cool_lex_output + ' ' + my_lex_output)
        else:
            print(cl + ': ' + 'Error')
    print('============================================================================')

if __name__ == '__main__':
    TestLexer()