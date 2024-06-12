import ply.yacc as yacc
from lexer import tokens

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'EQ', 'NEQ', 'LT', 'GT', 'LE', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MUL', 'DIV', 'MOD'),
    ('right', 'POW'),
)

start = 'Program'

def p_empty(p):
    '''empty :   '''
    pass

def p_Program(p):
    '''Program : ProgramHeader ProgramBody
               | ProgramHeader'''
    if len(p) == 3:
        p[0] = ('Program', p[1], p[2])
    else:
        p[0] = ('Program', p[1], None)  # No program body

def p_ProgramHeader(p):
    '''ProgramHeader : PROGRAM ID SEMICOLON'''
    p[0] = ('ProgramHeader', p[2])

def p_ProgramBody(p):
    '''ProgramBody : VarDecls Cmd'''
    p[0] = ('ProgramBody', p[1], p[2])

def p_Cmd(p):
    '''Cmd : CmdAtrib
           | CmdFor
           | CmdIf
           | CmdWhile
           | CmdBreak
           | CmdPrint
           | CmdReturn
           | CmdSeq'''
    p[0] = p[1]

def p_CmdAtrib(p):
    '''CmdAtrib : ID ASSIGN Expr SEMICOLON'''
    p[0] = ('Assign', p[1], p[3])

def p_CmdIf(p):
    '''CmdIf : IF Expr COLON Cmd
             | IF Expr COLON Cmd ELSE COLON Cmd'''
    if len(p) == 5:
        p[0] = ('If', p[2], p[4])
    else:
        p[0] = ('IfElse', p[2], p[4], p[7])

def p_CmdWhile(p):
    '''CmdWhile : WHILE Expr COLON CmdSeq'''
    p[0] = ('While', p[2], p[4])

def p_CmdFor(p):
    '''CmdFor : FOR ID ASSIGN Expr TO Expr COLON Cmd'''
    p[0] = ('For', p[2], p[4], p[6], p[8])

def p_CmdBreak(p):
    '''CmdBreak : BREAK SEMICOLON'''
    p[0] = ('Break',)

def p_CmdPrint(p):
    '''CmdPrint : PRINT LPAREN ExprList RPAREN'''
    p[0] = ('Print', p[3])

def p_CmdReturn(p):
    '''CmdReturn : RETURN Expr SEMICOLON'''
    p[0] = ('Return', p[2])

def p_CmdSeq(p):
    '''CmdSeq : LCURLY CmdList RCURLY
              | LCURLY CmdList1 RCURLY'''
    p[0] = ('Sequence', p[2])

def p_CmdList1(p):
    '''CmdList1 : Cmd CmdList1
               | empty'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

def p_CmdList(p):
    '''CmdList : Cmd SEMICOLON CmdList
               | Cmd'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_Expr(p):
    '''Expr : NUMBER
            | FLOAT
            | TRUE
            | FALSE
            | ID
            | Expr BinOp Expr
            | UnOp Expr
            | LPAREN Expr RPAREN
            | ID LPAREN ExprList RPAREN
            | READ LPAREN RPAREN'''
    if isinstance(p[1], int) or isinstance(p[1], float):
        p[0] = ('Literal', p[1])
    elif p[1] == 'true':
        p[0] = ('Bool', True)
    elif p[1] == 'false':
        p[0] = ('Bool', False)
    elif isinstance(p[1], str) and p[1] not in ('-', 'not'):
        p[0] = ('Variable', p[1])
    elif len(p) == 4 and p[2] in ('+', '-', '*', '/', '**', '%', '==', '!=', '<', '>', '<=', '>=', 'and', 'or'):
        p[0] = ('BinOp', p[2], p[1], p[3])
    elif len(p) == 3 and p[1] in ('-', 'not'):
        p[0] = ('UnOp', p[1], p[2])
    elif p[1] == '(':
        p[0] = p[2]
    elif p[2] == '(':
        p[0] = ('FuncCall', p[1], p[3])
    elif p[1] == 'read':
        p[0] = ('Read',)

def p_BinOp(p):
    '''BinOp : PLUS
             | ASSIGN
             | DIV
             | MINUS
             | MUL
             | POW
             | MOD
             | EQ
             | NEQ
             | LT
             | GT
             | LE
             | GE
             | AND
             | OR'''
    p[0] = p[1]

def p_UnOp(p):
    '''UnOp : MINUS
            | NOT'''
    p[0] = p[1]

def p_ExprList(p):
    '''ExprList : empty
                | ExprList1'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1]

def p_ExprList1(p):
    '''ExprList1 : Expr
                 | Expr COMMA ExprList1'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_VarDecls(p):
    '''VarDecls : VarDecl VarDecls
                | empty'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

def p_VarDecl(p):
    '''VarDecl : VAR ID COLON Type SEMICOLON'''
    p[0] = ('VarDecl', p[2], p[4])

def p_Type(p):
    '''Type : INT
            | BOOL
            | FLOAT'''
    p[0] = p[1]

def p_error(p):
    if p:
        print(f"Syntax error at token '{p.value}' (type: {p.type}) at line {p.lineno}")
    else:
        print("Syntax error: unexpected end of input")

parser = yacc.yacc()

class BreakException(Exception):
    pass

variables = {}

def execute(node):
    if node is None:
        return
    if node[0] == 'Program':
        execute(node[2])
    elif node[0] == 'ProgramBody':
        for var_decl in node[1]:
            execute(var_decl)
        execute(node[2])
    elif node[0] == 'VarDecl':
        variables[node[1]] = 0  # Initialize variable with a default value
    elif node[0] == 'Assign':
        variables[node[1]] = evaluate(node[2])
    elif node[0] == 'If':
        condition = evaluate(node[1])
        if condition:
            execute(node[2])
    elif node[0] == 'IfElse':
        condition = evaluate(node[1])
        if condition:
            execute(node[2])
        else:
            execute(node[3])
    elif node[0] == 'While':
        while evaluate(node[1]):
            try:
                execute(node[2])
            except BreakException:
                break
    elif node[0] == 'For':
        variables[node[1]] = evaluate(node[2])
        end = evaluate(node[3])
        while variables[node[1]] <= end:
            try:
                execute(node[4])
            except BreakException:
                break
            variables[node[1]] += 1
    elif node[0] == 'Break':
        raise BreakException()
    elif node[0] == 'Print':
        values = [evaluate(expr) for expr in node[1]]
        print(*values)
    elif node[0] == 'Return':
        return evaluate(node[1])
    elif node[0] == 'Sequence':
        for cmd in node[1]:
            execute(cmd)

def evaluate(node):
    if node[0] == 'Literal':
        return node[1]
    elif node[0] == 'Bool':
        return node[1]
    elif node[0] == 'Variable':
        return variables[node[1]]
    elif node[0] == 'BinOp':
        left, op, right = evaluate(node[2]), node[1], evaluate(node[3])
        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            return left / right
        elif op == '**':
            return left ** right
        elif op == '%':
            return left % right
        elif op == '==':
            return left == right
        elif op == '!=':
            return left != right
        elif op == '<':
            return left < right
        elif op == '>':
            return left > right
        elif op == '<=':
            return left <= right
        elif op == '>=':
            return left >= right
        elif op == 'and':
            return left and right
        elif op == 'or':
            return left or right
    elif node[0] == 'UnOp':
        op, expr = node[1], evaluate(node[2])
        if op == '-':
            return -expr
        elif op == 'not':
            return not expr
    elif node[0] == 'FuncCall':
        func_name, args = node[1], [evaluate(arg) for arg in node[2]]
        if func_name == 'read':
            return input(*args)

# Test string 1
test_string1 = '''
program count;
var i: int;
{
    i = 1;
    while i <= 10: {
        print(i);
        i = i + 1;
    }
}
'''

# Test string 2
test_string2 = '''
program count_for;
for i = 1 to 10 :
   print(i)
'''

print("Output for test_string1:")
ast1 = parser.parse(test_string1)
execute(ast1)

print("\nOutput for test_string2:")
ast2 = parser.parse(test_string2)
execute(ast2)

