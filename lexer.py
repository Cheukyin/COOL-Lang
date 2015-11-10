#!/usr/bin/python3

import sys, os
import ply.lex as lex
from ply.lex import TOKEN

class CoolLexer(object):
    keyword = {
        'inherits' : 'inherits',
        'isvoid'   : 'isvoid',
        'class'    : 'class',
        'Class'    : 'class',
        'while'    : 'while',
        'else'     : 'else',
        'false'    : 'false',
        'loop'     : 'loop',
        'pool'     : 'pool',
        'case'     : 'case',
        'esac'     : 'esac',
        'then'     : 'then',
        'true'     : 'true',
        'let'      : 'let',
        'new'      : 'new',
        'not'      : 'not',
        'if'       : 'if',
        'fi'       : 'fi',
        'in'       : 'in',
        'of'       : 'of',
    }

    #List of token names
    tokens = [
        'identifier',
        'integer',
        'string',
        'type',
        'plus',    # +
        'minus',   # -
        'times',   # *
        'divide',  # /
        'lparen',  # (
        'rparen',  # )
        'colon',   # :
        'lbrace',  # {
        'rbrace',  # }
        'semi',    # ;
        'larrow',  # <-
        'rarrow',  # =>
        'le',      # <=
        'lt',      # <
        'at',      # @
        'tilde',   # ~
        'dot',     # .
        'comma',   # ,
        'equals',  # =
    ] \
        + list(set( keyword.values() ))

    def __init__(self, src = '', debug = False):
        super(CoolLexer, self).__init__()
        if src != '':
            self.src = open(src, 'r')
        self.debug = debug
        if debug:
            self.LexOutput = open('lex-output-'
                                  + src.split('/')[-1] + '.txt', 'w')

    # A regular expression rule with some action code
    # Note addition of self parameter since we're in a class
    # No return value. Token discarded

    # block_comment doesn't support nesting
    line_comment = r'(--.*\n)'
    block_comment = r'(\(\*(.|\n)*?\*\))'
    comment = line_comment + r'|' + block_comment
    @TOKEN(comment)
    def t_comment(self, t):
        t.lexer.lineno += t.value.count('\n')

    def t_identifier(self, t):
        r'[a-z_][a-zA-Z_0-9]*'
        t.type = self.__class__.keyword.get(t.value, 'identifier')
        return t

    def t_type(self, t):
        r'[A-Z_][a-zA-Z_0-9]*'
        t.type = self.__class__.keyword.get(t.value, 'type')
        return t

    def t_string(self, t):
        r'"(\\"|.)*?"'
        t.value = t.value[1:-1] # strip the first and last "
        return t

    def t_integer(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    #Regular expression rules for simple tokens
    t_plus   = r'\+'
    t_minus  = r'-'
    t_times  = r'\*'
    t_divide = r'/'
    t_lparen = r'\('
    t_rparen = r'\)'
    t_colon  = r':'
    t_lbrace = r'\{'
    t_rbrace = r'\}'
    t_semi   = r';'
    t_larrow = r'<-'
    t_rarrow = r'=>'
    t_le     = r'<='
    t_lt     = r'<'
    t_at     = r'@'
    t_tilde  = r'~'
    t_dot    = r'\.'
    t_comma  = r','
    t_equals = r'='

    # A string containing ignored characters (spaces and tabs)
    t_ignore  = ' \t\v\f'

    # Error handling rule
    def t_error(self, t):
        print("ERROR: %d: Lexer: invalid character: %s" % (t.lexer.lineno, t.value))
        t.lexer.skip(1)

    # Build the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def debug_output(self, tok):
        self.LexOutput.write( str(tok.lineno) + "\n" )
        self.LexOutput.write( tok.type + "\n" )
        if tok.type in ['identifier', 'string', 'integer', 'type']:
            self.LexOutput.write( str(tok.value) + "\n" )

    def process(self):
        self.lexer.input( self.src.read() )
        # self.lexer.input('''
        # position <- 0
        # ''')
        if self.debug:
            for tok in self.lexer:
                    self.debug_output(tok)
            self.LexOutput.close()


if __name__ == '__main__':
    # Build the lexer and try it out
    lexer = CoolLexer( src = sys.argv[1], debug = True)
    lexer.build()   # Build the lexer
    lexer.process()
