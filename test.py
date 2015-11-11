#!/usr/bin/python3
import unittest
import test_lexer
import  test_parser

if __name__ == "__main__":
    test_lexer.TestLexer()

    ParserSuite = unittest.TestLoader().loadTestsFromTestCase(test_parser.TestParser)
    unittest.TextTestRunner(verbosity = 2).run(ParserSuite)