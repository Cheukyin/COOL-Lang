#!/usr/bin/python3

import unittest
import parser
from AST import *

class TestParser(unittest.TestCase):
    def setUp(self):
        # Build the parser
        self.parser = parser.CoolParser()
        self.parser.build()

    def testClass(self):
        self.assertEqual
        (
            self.parser.process(
                    '''
                    class Main inherits IO {
                        i:Int;
                    } ;
                    '''
            ),
            Program([Class('Main', 'IO',
                           [Attribute('i', 'Int', None, 3)],
                           [], 2)],
                    0)
        )

if __name__ == "__main__":
    ParserSuite = unittest.TestLoader().loadTestsFromTestCase(TestParser)
    unittest.TextTestRunner(verbosity = 2).run(ParserSuite)