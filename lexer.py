import ply.lex as lex

# MAIN OBJECTIVES

#- Basic types (int and bool) and constants of these types (integers, true and false)  -->done
#- Arithmetic expressions: with +, -, *, /, **, and %; -->done
#- Variable declarations and simple assignments (var x : int and x = expr ); -->done
#- Comparison operators and Boolean expressions: with ==, !=, <, >, <=, >=; -->done
#- Conditional execution: if with or without else; -->done
#- Composite commands: { cmd 1 ; . . . ; cmd n}; -->done
#- While cycles; -->done
#- Return commands; -->done
#- I/O functions: read and print. -->done

#EXTRA OBJECTIVES 

#- Not, or and logical operators (10%)--> done
#- Other objectives deemed interesting by the students (20%)--(language now allows floting point numbers )-->done

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'read': 'READ',
    'print': 'PRINT',
    'true': 'TRUE',
    'false': 'FALSE',
    'var': 'VAR',
    'not': 'NOT',
    'or': 'OR',
    'program': 'PROGRAM',
    'and': 'AND',
    'return': 'RETURN',
    'break': 'BREAK',
    'float': 'FLOAT',
    'int': 'INT',
    'bool': 'BOOL',
    'for': 'FOR',
    'to': 'TO'
}

tokens = [
    'ID', 'PLUS', 'MINUS', 'MUL', 'DIV', 'POW', 'MOD',
    'EQ', 'NEQ', 'LT', 'GT', 'LE', 'GE', 'ASSIGN', 'LPAREN', 'RPAREN',
    'LCURLY', 'RCURLY', 'COMMA', 'SEMICOLON', 'COLON',
    'NUMBER', 'FLOATNUMB'
] + list(reserved.values())

t_PLUS = r'\+'
t_MINUS = r'-'
t_MUL = r'\*'
t_DIV = r'/'
t_POW = r'\*\*'
t_MOD = r'%'
t_EQ = r'=='
t_NEQ = r'!='
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_ASSIGN = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LCURLY = r'\{'
t_RCURLY = r'\}'
t_COMMA = r','
t_SEMICOLON = r';'
t_COLON = r':'






def t_FLOATNUMB(t):
    r'[0-9]+\.[0-9]+'
    t.value=float(t.value)
    return t
 
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):  #(intergers)
    r'\d+'
    t.value = int(t.value)
    return t


def t_COMMENT_SINGLE(t):
    r'\#.*'
    pass

t_ignore = ' \t\n'


def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
    t.lexer.skip(1)
 

lexer=lex.lex()

test_string="""
program my_program;

var x: int;
y: bool;
z: float;

x = 10;
y = true;
z=5.0;

if (x > 5) {
  print(x);
} else {
  read(y);
  while (y != false) {
    x = x - 1;
    y = not y;  
  }
}

return x;"""


lexer.input(test_string)

while True:
    tok = lexer.token()
    if not tok:
        break  
    print(tok.type, tok.value, tok.lineno, tok.lexpos)
