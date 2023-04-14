# LL(1) parser that used the lexer's output to parse the input according to grammar.txt's rules

import sys
from colorama import Fore, Style, init
import argparse
from collections import deque
import traceback

def print_fancy(text, width=80, fill_char='-'):
    print(text.center(width, fill_char))

class Token:
    def __init__(self, token):
        self.token_type = token[0]
        self.token_value = token[1]
        self.token_line = token[2]
        self.token_column = token[3]

    def __str__(self):
        return f'token type: {self.token_type} with token value: {self.token_value}'
    
    def __eq__(self, expected_token_type):
        if type(expected_token_type) == str:
            return self.token_type == expected_token_type
        raise TypeError('Expected token type must be a string')
    
class TokenStream:
    def __init__(self, source):
        self.source = source
        # open the file
        file_stream = open(self.source, 'r')
        token_stream = deque([])
        # read every line in the file, create a token for that line and put it in the queue
        for line in file_stream:
            curr = line.strip().split()
            if curr[0] == 'COMMENT':
                continue
            token_stream.append(Token(curr))
        # add an EOF token to the end of the queue
        token_stream.append(Token(['EOF', 'EOF', 'EOF', 'EOF']))
        
        self.token_stream = token_stream
        
    def pop(self):
        # return the first token in the queue
        return self.token_stream.popleft()
    
    def peek(self):
        return self.token_stream[0]

class TreeNode:
    '''
    Define a node in the CST
    The CST is an N-ary tree
    '''
    def __init__(self, val, token=None, parent=None):
        self.children = []
        self.val = val
        self.parent = parent
        self.token = token if token else None
        # if the node has a token, it means it is terminal, so it has no children
        self.children = [] if not self.token else None
        self.depth = 0 if not self.parent else self.parent.depth + 1

    def add_child(self, child):
        if self.token:
            print('Error: Cannot add child to a leaf node')
            sys.exit(1)
        self.children.append(child)
        if not child.parent:
            child.parent = self
            child.depth = self.depth + 1

    def __str__(self):
        '''
        printing the tree in a way that looks like the folder structure of a file system:
        mySite
        ├──css
        │   └──page.css
        ├──images
        │   └──img.svg
        ├──index.html
        ├──js
        │   └──empty.js
        ├──other
        │   └──folder
        │       └──page.html
        ├──page1.html
        └──sub
            └──page2.html
        '''
        if not self.children:
            return self.val
        # if the node is not a leaf node, return the token and return the representation of the children
        

        result = self.val + '\n'
        for i, child in enumerate(self.children):
            if i == len(self.children) - 1:
                result += '└───' + str(child).replace('\n', '\n    ') + '\n'
            else:
                result += '├───' + str(child).replace('\n', '\n│   ') + '\n'
        return result
    
class ExpectationError(Exception):
    def __init__(self, token, expected):
        self.token = token
        self.expected = expected
        self.message = f'Expected {self.expected} but got {self.token.token_type} on line {self.token.token_line}'
        super().__init__(self.message)

class MissingTokenError(Exception):
    def __init__(self, expected):
        self.expected = expected
        self.message = f'Expected {self.expected} is Missing'
        super().__init__(self.message)

'''Terminal functions'''


def ID(token_stream):
    # if the current token is an ID
    token = token_stream.peek()
    if token.token_type == 'ID':
        # create a node with the token as the value
        node = TreeNode('ID', token=token)
        # return the node
        token_stream.pop()
        return node
    return None

def INTEGER(token_stream):
    # if the current token is an INTEGER
    token = token_stream.peek()
    if token.token_type == 'INTEGER':
        # create a node with the token as the value
        node = TreeNode('INTEGER', token=token)
        # return the node
        token_stream.pop()
        return node
    return None

def BOOLEAN(token_stream):
    # if the current token is a BOOLEAN
    token = token_stream.peek()
    if token.token_type == 'BOOLEAN':
        # create a node with the token as the value
        node = TreeNode('BOOLEAN', token=token)
        # return the node
        token_stream.pop()
        return node
    return None

def PLUS(token_stream):
    # if the current token is a PLUS
    token = token_stream.peek()
    if token.token_type == 'PLUS':
        # create a node with the token as the value
        node = TreeNode('PLUS', token=token)
        # return the node
        token_stream.pop()
        return node
    return None

def MINUS(token_stream):
    # if the current token is a MINUS
    token = token_stream.peek()
    if token.token_type == 'MINUS':
        # create a node with the token as the value
        node = TreeNode('MINUS', token=token)
        # return the node
        token_stream.pop()
        return node
    return None

def MULTIPLY(token_stream):
    # if the current token is a MULTIPLY
    token = token_stream.peek()
    if token.token_type == 'MULTIPLY':
        # create a node with the token as the value
        node = TreeNode('MULTIPLY', token=token)
        # return the node
        token_stream.pop()
        return node
    return None

def DIVIDE(token_stream):
    # if the current token is a DIVIDE
    token = token_stream.peek()
    if token.token_type == 'DIVIDE':
        # create a node with the token as the value
        node = TreeNode('DIVIDE', token=token)
        # return the node
        token_stream.pop()
        return node
    return None

def LEFTBRACKET(token_stream):
    # if the current token is a LEFTBRACKET
    token = token_stream.peek()
    if token.token_type == 'LEFTBRACKET':
        # create a node with the token as the value
        node = TreeNode('LEFTBRACKET', token=token)
        # return the node
        token_stream.pop()
        return node
    return None

def RIGHTBRACKET(token_stream):
    # if the current token is a RIGHTBRACKET
    token = token_stream.peek()
    if token.token_type == 'RIGHTBRACKET':
        # create a node with the token as the value
        node = TreeNode('RIGHTBRACKET', token=token)
        # return the node
        token_stream.pop()
        return node
    return None

def LPAREN(token_stream):
    # if the current token is a LPAREN
    token = token_stream.peek()
    if token.token_type == 'LPAREN':
        # create a node with the token as the value
        node = TreeNode('LPAREN', token=token)
        # return the node
        token_stream.pop()
        return node
    return None

def RPAREN(token_stream):
    # if the current token is a RPAREN
    token = token_stream.peek()
    if token.token_type == 'RPAREN':
        # create a node with the token as the value
        node = TreeNode('RPAREN', token=token)
        # return the node
        token_stream.pop()
        return node
    return None

def COMPARISON(token_stream):
    # if the current token is a COMPARISON
    token = token_stream.peek()
    if token.token_type == 'COMPARISON':
        # create a node with the token as the value
        node = TreeNode('COMPARISON', token=token)
        # return the node
        token_stream.pop()
        return node
    return None

def LBRACE(token_stream):
    # if the current token is a LBRACE
    token = token_stream.peek()
    if token.token_type == 'LBRACE':
        # create a node with the token as the value
        node = TreeNode('LBRACE', token=token)
        # return the node
        token_stream.pop()
        return node
    return None

def RBRACE(token_stream):
    # if the current token is a RBRACE
    token = token_stream.peek()
    if token.token_type == 'RBRACE':
        # create a node with the token as the value
        node = TreeNode('RBRACE', token=token)
        # return the node
        token_stream.pop()
        return node
    return None

def LOGIC(token_stream):
    # if the current token is a LOGIC
    token = token_stream.peek()
    if token.token_type == 'LOGIC':
        # create a node with the token as the value
        node = TreeNode('LOGIC', token=token)
        # return the node
        token_stream.pop()
        return node
    return None

def RETURN(token_stream):
    # if the current token is a RETURN
    token = token_stream.peek()
    if token.token_type == 'RETURN':
        # create a node with the token as the value
        node = TreeNode('RETURN', token=token)
        # return the node
        token_stream.pop()
        return node
    return None

def ASSIGNMENT(token_stream):
    # if the current token is a ASSIGNMENT
    token = token_stream.peek()
    if token.token_type == 'ASSIGNMENT':
        # create a node with the token as the value
        node = TreeNode('ASSIGNMENT', token=token)
        # return the node
        token_stream.pop()
        return node
    return None

def WHILE(token_stream):
    # if the current token is a WHILE
    token = token_stream.peek()
    if token.token_type == 'WHILE':
        # create a node with the token as the value
        node = TreeNode('WHILE', token=token)
        # return the node
        token_stream.pop()
        return node
    return None

def IF(token_stream):
    # if the current token is a IF
    token = token_stream.peek()
    if token.token_type == 'IF':
        # create a node with the token as the value
        node = TreeNode('IF', token=token)
        # return the node
        token_stream.pop()
        return node
    return None

def ELSE(token_stream):
    # if the current token is a ELSE
    token = token_stream.peek()
    if token.token_type == 'ELSE':
        # create a node with the token as the value
        node = TreeNode('ELSE', token=token)
        # return the node
        token_stream.pop()
        return node
    return None

def NORTH(token_stream):
    # if the current token is a NORTH
    token = token_stream.peek()
    if token.token_type == 'NORTH':
        # create a node with the token as the value
        node = TreeNode('NORTH', token=token)
        # return the node
        token_stream.pop()
        return node
    return None

def SOUTH(token_stream):
    # if the current token is a SOUTH
    token = token_stream.peek()
    if token.token_type == 'SOUTH':
        # create a node with the token as the value
        node = TreeNode('SOUTH', token=token)
        # return the node
        token_stream.pop()
        return node
    return None

def EAST(token_stream):
    # if the current token is a EAST
    token = token_stream.peek()
    if token.token_type == 'EAST':
        # create a node with the token as the value
        node = TreeNode('EAST', token=token)
        # return the node
        token_stream.pop()
        return node
    return None

def WEST(token_stream):
    # if the current token is a WEST
    token = token_stream.peek()
    if token.token_type == 'WEST':
        # create a node with the token as the value
        node = TreeNode('WEST', token=token)
        # return the node
        token_stream.pop()
        return node
    return None

def PRINT_POSITION(token_stream):
    # if the current token is a PRINT_POSITION
    token = token_stream.peek()
    if token.token_type == 'PRINT_POSITION':
        # create a node with the token as the value
        node = TreeNode('PRINT_POSITION', token=token)
        # return the node
        token_stream.pop()
        return node
    return None

def SENSE_GLITTER(token_stream):
    # if the current token is a SENSE_GLITTER
    token = token_stream.peek()
    if token.token_type == 'SENSE_GLITTER':
        # create a node with the token as the value
        node = TreeNode('SENSE_GLITTER', token=token)
        # return the node
        token_stream.pop()
        return node
    return None

def SENSE_BREEZE(token_stream):
    # if the current token is a SENSE_BREEZE
    token = token_stream.peek()
    if token.token_type == 'SENSE_BREEZE':
        # create a node with the token as the value
        node = TreeNode('SENSE_BREEZE', token=token)
        # return the node
        token_stream.pop()
        return node
    return None

def SENSE_STENCH(token_stream):
    # if the current token is a SENSE_STENCH
    token = token_stream.peek()
    if token.token_type == 'SENSE_STENCH':
        # create a node with the token as the value
        node = TreeNode('SENSE_STENCH', token=token)
        # return the node
        token_stream.pop()
        return node
    return None

def GRAB(token_stream):
    # if the current token is a GRAB
    token = token_stream.peek()
    if token.token_type == 'GRAB':
        # create a node with the token as the value
        node = TreeNode('GRAB', token=token)
        # return the node
        token_stream.pop()
        return node
    return None

def SHOOT(token_stream):
    # if the current token is a SHOOT
    token = token_stream.peek()
    if token.token_type == 'SHOOT':
        # create a node with the token as the value
        node = TreeNode('SHOOT', token=token)
        # return the node
        token_stream.pop()
        return node
    return None


def MOVE(token_stream):
    # if the current token is a MOVE
    token = token_stream.peek()
    if token.token_type == 'MOVE':
        # create a node with the token as the value
        node = TreeNode('MOVE', token=token)
        # return the node
        token_stream.pop()
        return node
    return None

def PLAY(token_stream):
    # if the current token is a PLAY
    token = token_stream.peek()
    if token.token_type == 'PLAY':
        # create a node with the token as the value
        node = TreeNode('PLAY', token=token)
        # return the node
        token_stream.pop()
        return node
    return None

def PLACE_GOLD(token_stream):
    # if the current token is a PLACE_GOLD
    token = token_stream.peek()
    if token.token_type == 'PLACE_GOLD':
        # create a node with the token as the value
        node = TreeNode('PLACE_GOLD', token=token)
        # return the node
        token_stream.pop()
        return node
    return None

def PLACE_WUMPUS(token_stream):
    # if the current token is a PLACE_WUMPUS
    token = token_stream.peek()
    if token.token_type == 'PLACE_WUMPUS':
        # create a node with the token as the value
        node = TreeNode('PLACE_WUMPUS', token=token)
        # return the node
        token_stream.pop()
        return node
    return None

def PLACE_PIT(token_stream):
    # if the current token is a PLACE_PIT
    token = token_stream.peek()
    if token.token_type == 'PLACE_PIT':
        # create a node with the token as the value
        node = TreeNode('PLACE_PIT', token=token)
        # return the node
        token_stream.pop()
        return node
    return None

def PLACE_AGENT(token_stream):
    # if the current token is a PLACE_AGENT
    token = token_stream.peek()
    if token.token_type == 'PLACE_AGENT':
        # create a node with the token as the value
        node = TreeNode('PLACE_AGENT', token=token)
        # return the node
        token_stream.pop()
        return node
    return None

def GRID_SIZE(token_stream):
    # if the current token is a GRID_SIZE
    token = token_stream.peek()
    if token.token_type == 'GRID_SIZE':
        # create a node with the token as the value
        node = TreeNode('GRID_SIZE', token=token)
        # return the node
        token_stream.pop()
        return node
    return None

def INIT(token_stream):
    # if the current token is a INIT
    token = token_stream.peek()
    if token.token_type == 'INIT':
        # create a node with the token as the value
        node = TreeNode('INIT', token=token)
        # return the node
        token_stream.pop()
        return node
    return None

def CONSTANT(token_stream):
    # if the current token is a CONSTANT
    token = token_stream.peek()
    if token.token_type == 'CONSTANT':
        # create a node with the token as the value
        node = TreeNode('CONSTANT', token=token)
        # return the node
        token_stream.pop()
        return node
    return None

def VARIABLE(token_stream):
    # if the current token is a VARIABLE
    token = token_stream.peek()
    if token.token_type == 'VARIABLE':
        # create a node with the token as the value
        node = TreeNode('VARIABLE', token=token)
        # return the node
        token_stream.pop()
        return node
    return None

def INTDTYPE(token_stream):
    # if the current token is a INTDTYPE
    token = token_stream.peek()
    if token.token_type == 'INTDTYPE':
        # create a node with the token as the value
        node = TreeNode('INTDTYPE', token=token)
        # return the node
        token_stream.pop()
        return node
    return None

def BOOLDTYPE(token_stream):
    # if the current token is a BOOLDTYPE
    token = token_stream.peek()
    if token.token_type == 'BOOLDTYPE':
        # create a node with the token as the value
        node = TreeNode('BOOLDTYPE', token=token)
        # return the node
        token_stream.pop()
        return node
    return None

def VOID(token_stream):
    # if the current token is a VOID
    token = token_stream.peek()
    if token.token_type == 'VOID':
        # create a node with the token as the value
        node = TreeNode('VOID', token=token)
        # return the node
        token_stream.pop()
        return node
    return None

def FUNCTION(token_stream):
    # if the current token is a FUNCTION
    token = token_stream.peek()
    if token.token_type == 'FUNCTION':
        # create a node with the token as the value
        node = TreeNode('FUNCTION', token=token)
        # return the node
        token_stream.pop()
        return node
    return None

def CLEAR_ROOM(token_stream):
    # if the current token is a CLEAR_ROOM
    token = token_stream.peek()
    if token.token_type == 'CLEAR_ROOM':
        # create a node with the token as the value
        node = TreeNode('CLEAR_ROOM', token=token)
        # return the node
        token_stream.pop()
        return node
    return None

def COMMA(token_stream):
    # if the current token is a COMMA
    token = token_stream.peek()
    if token.token_type == 'COMMA':
        # create a node with the token as the value
        node = TreeNode('COMMA', token=token)
        # return the node
        token_stream.pop()
        return node
    return None


def var(token_stream):
    # This is for the production <var> ::= ID [LEFTBRACKET <expr> RIGHTBRACKET]
    node = TreeNode('var')
    print(node)
    # add the var's children'
    try:
        node.add_child(ID(token_stream))
        if token_stream.peek() == 'LEFTBRACKET':
            node.add_child(LEFTBRACKET(token_stream))
            try:
                node.add_child(expr(token_stream))
            except Exception as e:
                raise e
            node.add_child(RIGHTBRACKET(token_stream))
    except Exception as e:
        raise e
    # return the node
    return node

def exprbase(token_stream):
    # This is for the production <exprbase> ::= <var> | INTEGER | BOOLEAN | LPAREN <expr> RPAREN | MINUS <exprbase>
    node = TreeNode('exprbase')
    print(node)
    # add the exprbase's children'
    try:
        if token_stream.peek() == 'ID':
            node.add_child(var(token_stream))
        elif token_stream.peek() == 'INTEGER':
            node.add_child(INTEGER(token_stream))
        elif token_stream.peek() == 'BOOLEAN':
            node.add_child(BOOLEAN(token_stream))
        elif token_stream.peek() == 'LPAREN':
            node.add_child(LPAREN(token_stream))
            try:
                node.add_child(expr(token_stream))
            except Exception as e:
                raise e
            node.add_child(RPAREN(token_stream))
        elif token_stream.peek() == 'MINUS':
            node.add_child(MINUS(token_stream))
            node.add_child(exprbase(token_stream))
    except Exception as e:
        raise e
    return node




    
def exprfac(token_stream):
    # create a node for the exprfac
    # <exprfac> ::= <exprbase> [ (MULTIPLY | DIVIDE) <exprbase> ]
    node = TreeNode('exprfac')
    print(node)
    # add the exprfac's children
    try:
        node.add_child(exprbase(token_stream))
    except Exception as e:
        raise e
    if token_stream.peek() == 'MULTIPLY':
        node.add_child(MULTIPLY(token_stream))
    elif token_stream.peek() == 'DIVIDE':
        node.add_child(DIVIDE(token_stream))
    else:
        return node
    try:
        node.add_child(exprbase(token_stream))
    except Exception as e:
        raise e
    return node

def expr(token_stream):
    # This is for the production <expr> ::= <exprfac> [ (PLUS | MINUS) <expr> ]
    # create a node for the expr
    node = TreeNode('expr')
    print(node)
    # add the expr's children
    try:
        node.add_child(exprfac(token_stream))
    except Exception as e:
        raise e
    if token_stream.peek() == 'PLUS':
        node.add_child(PLUS(token_stream))
    elif token_stream.peek() == 'MINUS':
        node.add_child(MINUS(token_stream))
    else:
        return node
    node.add_child(expr(token_stream))
    return node

def element(token_stream):
    # This is for the production <element> ::= <sense> | <expr>
    # create a node for the element
    node = TreeNode('element')
    # add the element's children
    try:
        if token_stream.peek() in ['SENSE_STENCH', 'SENSE_BREEZE', 'SENSE_GLITTER']:
            node.add_child(sense(token_stream))
        else:
            node.add_child(expr(token_stream))
    except Exception as e:
        raise e
    # return the node
    return node


def term(token_stream):
    # This is for the production <term> ::= <element> { COMPARISON <element>}
    # create a node for the term
    node = TreeNode('term')
    # add the term's children
    try:
        node.add_child(element(token_stream))
    except Exception as e:
        raise e
    while token_stream.peek() == 'COMPARISON':
        node.add_child(COMPARISON(token_stream))
        node.add_child(element(token_stream))
    # return the node
    return node

def conditional_expression(token_stream):
    # This is for the production <conditional_expression> ::= <term> { LOGIC <term>}
    # Create a node for the conditional_expression
    node = TreeNode('conditional_expression')
    # Add the conditional_expression's children
    try:
        node.add_child(term(token_stream))
    except Exception as e:
        raise e
    while token_stream.peek() == 'LOGIC':
        node.add_child(LOGIC(token_stream))
        node.add_child(term(token_stream))
    # return the node
    return node


def block(token_stream):
    # This is for the production <block> ::= LBRACE <statement> { <statement> } RBRACE
    # create a node for the block
    node = TreeNode('block')
    # add the block's children
    LBRACE_node = LBRACE(token_stream)
    if LBRACE_node is not None:
        node.add_child(LBRACE_node)
        try:
            node.add_child(statement(token_stream))
        except Exception as e:
            raise e
        while token_stream.peek() != 'RBRACE':
            try:
                node.add_child(statement(token_stream))
            except Exception as e:
                raise e
        RBRACE_node = RBRACE(token_stream)
        if RBRACE_node is not None:
            node.add_child(RBRACE_node)
            return node
        if token_stream.peek() == 'EOF':
            raise MissingTokenError('RBRACE')
        else:
            raise ExpectationError('RBRACE', token_stream.peek())
        
def return_statement(token_stream):
    # This is for the production <return_statement> ::= RETURN <expr>
    # create a node for the return_statement
    node = TreeNode('return_statement')
    # add the return_statement's children
    try:
        node.add_child(RETURN(token_stream))
    except Exception as e:
        raise e
    try:
        node.add_child(expr(token_stream))
    except Exception as e:
        raise e
    # return the node
    return node

def action_assignment(token_stream):
    # This is for the production <action_assignment> ::= <var> ASSIGNMENT (<element> | ID LPAREN [ID {COMMA ID}] RPAREN)

    # create a node for the action_assignment
    node = TreeNode('action_assignment')
    # add the action_assignment's children
    try:
        node.add_child(var(token_stream))
        node.add_child(ASSIGNMENT(token_stream))
        if token_stream.peek() == 'ID':
            node.add_child(ID(token_stream))
            node.add_child(LPAREN(token_stream))
            if token_stream.peek() == 'ID':
                node.add_child(ID(token_stream))
                while token_stream.peek() == 'COMMA':
                    node.add_child(COMMA(token_stream))
                    node.add_child(ID(token_stream))
            node.add_child(RPAREN(token_stream))
        else:
            node.add_child(element(token_stream))
    except Exception as e:
        raise e
    # return the node
    return node


def while_statement(token_stream):
    # This is for the production <while_statement> ::= WHILE LPAREN <conditional_expression> RPAREN <block>
    # create a node for the while_statement
    node = TreeNode('while_statement')
    # add the while_statement's children
    try:
        node.add_child(WHILE(token_stream))
    except Exception as e:
        raise e
    try:
        node.add_child(LPAREN(token_stream))
    except Exception as e:
        raise e
    try:
        node.add_child(conditional_expression(token_stream))
    except Exception as e:
        raise e
    try:
        node.add_child(RPAREN(token_stream))
    except Exception as e:
        raise e
    try:
        node.add_child(block(token_stream))
    except Exception as e:
        raise e
    # return the node
    return node

def if_statement(token_stream):
    # This is for the production <if_statement> ::= IF LPAREN <conditional_expression> RPAREN <block> [ELSE <block>]
    # create a node for the if_statement
    node = TreeNode('if_statement')
    # add the if_statement's children
    try:
        node.add_child(IF(token_stream))
    except Exception as e:
        raise e
    try:
        node.add_child(LPAREN(token_stream))
    except Exception as e:
        raise e
    try:
        node.add_child(conditional_expression(token_stream))
    except Exception as e:
        raise e
    try:
        node.add_child(RPAREN(token_stream))
    except Exception as e:
        raise e
    try:
        node.add_child(block(token_stream))
    except Exception as e:
        raise e
    if token_stream.peek() == 'ELSE':
        node.add_child(ELSE(token_stream))
        try:
            node.add_child(block(token_stream))
        except Exception as e:
            raise e
    # return the node
    return node

def direction(token_stream):
    # This is for the production <direction ::= NORTH | SOUTH | EAST | WEST
    # create a node for the direction
    node = TreeNode('direction')
    # add the direction's children
    if token_stream.peek() == 'NORTH':
        node.add_child(NORTH(token_stream))
    elif token_stream.peek() == 'SOUTH':
        node.add_child(SOUTH(token_stream))
    elif token_stream.peek() == 'EAST':
        node.add_child(EAST(token_stream))
    elif token_stream.peek() == 'WEST':
        node.add_child(WEST(token_stream))
    else:
        raise ExpectationError('direction', token_stream.peek())
    # return the node
    return node

def print_position_statement(token_stream):
    # This is for the production <print_position_statement> ::= PRINT_POSITION LPAREN RPAREN
    # create a node for the print_position_statement
    node = TreeNode('print_position_statement')
    # add the print_position_statement's children
    try:
        node.add_child(PRINT_POSITION(token_stream))
    except Exception as e:
        raise e
    try:
        node.add_child(LPAREN(token_stream))
    except Exception as e:
        raise e
    try:
        node.add_child(RPAREN(token_stream))
    except Exception as e:
        raise e
    # return the node
    return node

def sense_glitter_statement(token_stream):
    # This is for the production <sense_glitter_statement> ::= SENSE_GLITTER LPAREN RPAREN
    # create a node for the sense_glitter_statement
    node = TreeNode('sense_glitter_statement')
    # add the sense_glitter_statement's children
    try:
        node.add_child(SENSE_GLITTER(token_stream))
    except Exception as e:
        raise e
    try:
        node.add_child(LPAREN(token_stream))
    except Exception as e:
        raise e
    try:
        node.add_child(RPAREN(token_stream))
    except Exception as e:
        raise e
    # return the node

def sense_breeze_statement(token_stream):
    # This is for the production <sense_breeze_statement> ::= SENSE_BREEZE LPAREN RPAREN
    # create a node for the sense_breeze_statement
    node = TreeNode('sense_breeze_statement')
    # add the sense_breeze_statement's children
    try:
        node.add_child(SENSE_BREEZE(token_stream))
    except Exception as e:
        raise e
    try:
        node.add_child(LPAREN(token_stream))
    except Exception as e:
        raise e
    try:
        node.add_child(RPAREN(token_stream))
    except Exception as e:
        raise e
    # return the node
    return node

def sense_stench_statement(token_stream):
    # This is for the production <sense_stench_statement> ::= SENSE_STENCH LPAREN RPAREN
    # create a node for the sense_stench_statement
    node = TreeNode('sense_stench_statement')
    # add the sense_stench_statement's children
    try:
        node.add_child(SENSE_STENCH(token_stream))
    except Exception as e:
        raise e
    try:
        node.add_child(LPAREN(token_stream))
    except Exception as e:
        raise e
    try:
        node.add_child(RPAREN(token_stream))
    except Exception as e:
        raise e
    # return the node
    return node

def sense(token_stream):
    # This is for the production <sense> ::= <sense_stench_statement> | <sense_breeze_statement> | <sense_glitter_statement>
    # create a node for the sense
    node = TreeNode('sense')
    # add the sense's children
    if token_stream.peek() == 'SENSE_STENCH':
        node.add_child(sense_stench_statement(token_stream))
    elif token_stream.peek() == 'SENSE_BREEZE':
        node.add_child(sense_breeze_statement(token_stream))
    elif token_stream.peek() == 'SENSE_GLITTER':
        node.add_child(sense_glitter_statement(token_stream))
    else:
        raise ExpectationError('sense', token_stream.peek())
    # return the node
    return node

def grab_statement(token_stream):
    # This is for the production <grab_statement> ::= GRAB LPAREN RPAREN
    # create a node for the grab_statement
    node = TreeNode('grab_statement')
    # add the grab_statement's children
    try:
        node.add_child(GRAB(token_stream))
    except Exception as e:
        raise e
    try:
        node.add_child(LPAREN(token_stream))
    except Exception as e:
        raise e
    try:
        node.add_child(RPAREN(token_stream))
    except Exception as e:
        raise e
    # return the node
    return node

def shoot_statement(token_stream):
    # This is for the production <shoot_statement> ::= SHOOT LPAREN <direction> RPAREN
    # create a node for the shoot_statement
    node = TreeNode('shoot_statement')
    # add the shoot_statement's children
    try:
        node.add_child(SHOOT(token_stream))
    except Exception as e:
        raise e
    try:
        node.add_child(LPAREN(token_stream))
    except Exception as e:
        raise e
    try:
        node.add_child(direction(token_stream))
    except Exception as e:
        raise e
    try:
        node.add_child(RPAREN(token_stream))
    except Exception as e:
        raise e
    # return the node
    return node

def move_statement(token_stream):
    # This is for the production <move_statement> ::= MOVE LPAREN <direction> RPAREN
    # create a node for the move_statement
    node = TreeNode('move_statement')
    # add the move_statement's children
    try:
        node.add_child(MOVE(token_stream))
    except Exception as e:
        raise e
    try:
        node.add_child(LPAREN(token_stream))
    except Exception as e:
        raise e
    try:
        node.add_child(direction(token_stream))
    except Exception as e:
        raise e
    try:
        node.add_child(RPAREN(token_stream))
    except Exception as e:
        raise e
    # return the node
    return node

def statement(token_stream):
    # This is for the production <statement> ::= <move_statement> | <shoot_statement> | <grab_statement> | <print_position_statement> | <if_statement> | <while_statement> | <action_assignment> | <return_statement>
    # create a node for the statement
    node = TreeNode('statement')
    # add the statement's children
    if token_stream.peek() == 'MOVE':
        node.add_child(move_statement(token_stream))
    elif token_stream.peek() == 'SHOOT':
        node.add_child(shoot_statement(token_stream))
    elif token_stream.peek() == 'GRAB':
        node.add_child(grab_statement(token_stream))
    elif token_stream.peek() == 'PRINT_POSITION':
        node.add_child(print_position_statement(token_stream))
    elif token_stream.peek() == 'IF':
        node.add_child(if_statement(token_stream))
    elif token_stream.peek() == 'WHILE':
        node.add_child(while_statement(token_stream))
    elif token_stream.peek() == 'ID':
        node.add_child(action_assignment(token_stream))
    elif token_stream.peek() == 'RETURN':
        node.add_child(return_statement(token_stream))
    else:
        raise ExpectationError('statement', token_stream.peek())


def play_block(token_stream):
    # This is for the production <play_block> ::= PLAY LBRACE <statement> { <statement> } RBRACE
    # create a node for the play_block
    node = TreeNode('play_block')
    # add the play_block's children

    try:
        node.add_child(PLAY(token_stream))
        node.add_child(LBRACE(token_stream))
        node.add_child(statement(token_stream))
        while token_stream.peek() in ['MOVE', 'SHOOT', 'GRAB', 'PRINT_POSITION', 'IF', 'WHILE', 'ID', 'RETURN', 'INTDTYPE', 'BOOLDTYPE']:
            node.add_child(statement(token_stream))
        node.add_child(RBRACE(token_stream))
    except Exception as e:
        raise e
    
    # return the node
    return node

def location(token_stream):
    # This is for the production <location> ::= INTEGER COMMA INTEGER
    # create a node for the location
    node = TreeNode('location')
    # add the location's children
    try:
        node.add_child(INTEGER(token_stream))
    except Exception as e:
        raise e
    try:
        node.add_child(COMMA(token_stream))
    except Exception as e:
        raise e
    try:
        node.add_child(INTEGER(token_stream))
    except Exception as e:
        raise e
    # return the node
    return node

def init_statement(token_stream):
    # This is for the production <init_statement> ::= PLACE_PIT LPAREN <location> RPAREN | CLEAR_ROOM LPAREN <location> RPAREN | CLEAR_ROOM LPAREN <location> RPAREN
    # create a node for the init_statement
    node = TreeNode('init_statement')
    # add the init_statement's children
    if token_stream.peek() == 'PLACE_PIT':
        try:
            node.add_child(PLACE_PIT(token_stream))
        except Exception as e:
            raise e
        try:
            node.add_child(LPAREN(token_stream))
        except Exception as e:
            raise e
        try:
            node.add_child(location(token_stream))
        except Exception as e:
            raise e
        try:
            node.add_child(RPAREN(token_stream))
        except Exception as e:
            raise e
    elif token_stream.peek() == 'CLEAR_ROOM':
        try:
            node.add_child(CLEAR_ROOM(token_stream))
        except Exception as e:
            raise e
        try:
            node.add_child(LPAREN(token_stream))
        except Exception as e:
            raise e
        try:
            node.add_child(location(token_stream))
        except Exception as e:
            raise e
        try:
            node.add_child(RPAREN(token_stream))
        except Exception as e:
            raise e
    # return the node
    return node


def mandatory_gold(token_stream):
    # This is for the production <mandatory_gold> ::= PLACE_GOLD LPAREN <location> RPAREN
    
    # create a node for the mandatory_gold
    node = TreeNode('mandatory_gold')
    # add the mandatory_gold's children
    try:
        node.add_child(PLACE_GOLD(token_stream))
        node.add_child(LPAREN(token_stream))
        node.add_child(location(token_stream))
        node.add_child(RPAREN(token_stream))
    except Exception as e:
        raise e
    # return the node
    return node

def mandatory_wumpus(token_stream):
    # This is for the production <mandatory_wumpus> ::= PLACE_WUMPUS LPAREN <location> RPAREN

    # create a node for the mandatory_wumpus
    node = TreeNode('mandatory_wumpus')
    # add the mandatory_wumpus's children
    try:
        node.add_child(PLACE_WUMPUS(token_stream))
        node.add_child(LPAREN(token_stream))
        node.add_child(location(token_stream))
        node.add_child(RPAREN(token_stream))
    except Exception as e:
        raise e
    # return the node
    return node

def mandatory_agent(token_stream):
    # This is for the production <mandatory_agent> ::= PLACE_AGENT LPAREN <location> RPAREN

    # create a node for the mandatory_agent
    node = TreeNode('mandatory_agent')
    # add the mandatory_agent's children
    try:
        node.add_child(PLACE_AGENT(token_stream))
        node.add_child(LPAREN(token_stream))
        node.add_child(location(token_stream))
        node.add_child(RPAREN(token_stream))
    except Exception as e:
        raise e
    # return the node
    return node

def grid_size(token_stream):
    # This is for the production <grid_size> ::= GRID_SIZE LPAREN <location> RPAREN
    
    # create a node for the grid_size
    node = TreeNode('grid_size')
    # add the grid_size's children
    try:
        node.add_child(GRID_SIZE(token_stream))
        node.add_child(LPAREN(token_stream))
        node.add_child(location(token_stream))
        node.add_child(RPAREN(token_stream))
    except Exception as e:
        raise e
    # return the node
    return node

def init_block(token_stream):
    # This is for the production INIT LBRACE <grid_size> <mandatory_agent> <mandatory_wumpus> <mandatory_gold> {<init_statement>} RBRACE

    # create a node for the init_block
    node = TreeNode('init_block')
    # add the init_block's children
    try:
        node.add_child(INIT(token_stream))
        node.add_child(LBRACE(token_stream))
        node.add_child(grid_size(token_stream))
        node.add_child(mandatory_agent(token_stream))
        node.add_child(mandatory_wumpus(token_stream))
        node.add_child(mandatory_gold(token_stream))
        while token_stream.peek() in ['PLACE_PIT', 'CLEAR_ROOM']:
            node.add_child(init_statement(token_stream))
        node.add_child(RBRACE(token_stream))
        
    except Exception as e:
        raise e
    # return the node
    return node
def declarations(token_stream):
    # This is for the production <declarations> ::= { <function_declaration> | <constant_declaration> }
    # create a node for the declarations
    node = TreeNode('declarations')
    # add the declarations's children
    while token_stream.peek() in ['CONSTANT', 'FUNCTION']:
        if token_stream.peek() == 'CONSTANT':
            try:
                node.add_child(constant_declaration(token_stream))
            except Exception as e:
                raise e
        elif token_stream.peek() == 'FUNCTION':
            try:
                node.add_child(function_declaration(token_stream))
            except Exception as e:
                raise e
    # return the node
    return node

def function_declaration(token_stream):
    # This is for the production <function_declaration> ::= FUNCTION <return_type> ID LPAREN [<formal_params> {COMMA <formal_params>}] RPAREN <block>
    # create a node for the function_declaration
    node = TreeNode('function_declaration')
    # add the function_declaration's children
    try:
        node.add_child(FUNCTION(token_stream))
        node.add_child(return_type(token_stream))
        node.add_child(ID(token_stream))
        node.add_child(LPAREN(token_stream))
        if token_stream.peek() in ['INTDTYPE', 'BOOLDTYPE']:
            node.add_child(formal_params(token_stream))
            while token_stream.peek() == 'COMMA':
                node.add_child(COMMA(token_stream))
                node.add_child(formal_params(token_stream))
        node.add_child(RPAREN(token_stream))
        node.add_child(block(token_stream))
    except Exception as e:
        raise e
    # return the node
    return node

def formal_params(token_stream):
    # This is for the production <formal_params> ::= (INTDTYPE | BOOLDTYPE) ID
    # create a node for the formal_params
    node = TreeNode('formal_params')
    # add the formal_params's children
    try:
        if token_stream.peek() == 'INTDTYPE':
            node.add_child(INTDTYPE(token_stream))
        elif token_stream.peek() == 'BOOLDTYPE':
            node.add_child(BOOLDTYPE(token_stream))
        node.add_child(ID(token_stream))
    except Exception as e:
        raise e
    # return the node
    return node

def return_type(token_stream):
    # This is for the production <return_type> ::= INTDTYPE | BOOLDTYPE | VOID
    # create a node for the return_type
    
    node = TreeNode('return_type')
    # add the return_type's children
    try:
        if token_stream.peek() == 'INTDTYPE':
            node.add_child(INTDTYPE(token_stream))
        elif token_stream.peek() == 'BOOLDTYPE':
            node.add_child(BOOLDTYPE(token_stream))
        elif token_stream.peek() == 'VOID':
            node.add_child(VOID(token_stream))
    except Exception as e:
        raise e
    # return the node
    return node

def constant_declaration(token_stream):
    # This is for the production <constant_declaration> ::= CONSTANT (INTDTYPE|BOOLDTYPE) ID ASSIGNMENT (INTEGER | BOOLEAN)
    
    # create a node for the constant_declaration
    node = TreeNode('constant_declaration')
    # add the constant_declaration's children
    try:
        node.add_child(CONSTANT(token_stream))
        if token_stream.peek() == 'INTDTYPE':
            node.add_child(INTDTYPE(token_stream))
        elif token_stream.peek() == 'BOOLDTYPE':
            node.add_child(BOOLDTYPE(token_stream))
        node.add_child(ID(token_stream))
        node.add_child(ASSIGNMENT(token_stream))
        if token_stream.peek() == 'INTEGER':
            node.add_child(INTEGER(token_stream))
        elif token_stream.peek() == 'BOOLEAN':
            node.add_child(BOOLEAN(token_stream))
    except Exception as e:
        raise e
    # return the node
    return node

def var_declaration(token_stream):
    # This is for the production <var_declaration> ::= (INTDTYPE|BOOLDTYPE) ID {LEFTBRACKET INTEGER RIGHTBRACKET}
    # create a node for the var_declaration
    node = TreeNode('var_declaration')
    # add the var_declaration's children
    try:
        if token_stream.peek() == 'INTDTYPE':
            node.add_child(INTDTYPE(token_stream))
        elif token_stream.peek() == 'BOOLDTYPE':
            node.add_child(BOOLDTYPE(token_stream))
        node.add_child(ID(token_stream))
        while token_stream.peek() == 'LEFTBRACKET':
            node.add_child(LEFTBRACKET(token_stream))
            node.add_child(INTEGER(token_stream))
            node.add_child(RIGHTBRACKET(token_stream))
    except Exception as e:
        raise e
    # return the node
    return node

def program(token_stream):
    # This is for the production <program> ::= <declarations> <init_block> <play_block>
    # create a node for the program
    node = TreeNode('program')
    # add the program's children
    try:
        node.add_child(declarations(token_stream))
        node.add_child(init_block(token_stream))
        
        node.add_child(play_block(token_stream))
        '''if token_stream.peek() != 'EOF':
            return node'''
    except Exception as e:
        print(node)
        print(e)
        sys.exit(1)
    # return the node
    return node


def run(token_stream, output_file):
    # parse the token stream
    cst = program(token_stream)
    # print the CST
    print(cst)
    # write the CST to the output file
    output_file.write(str(cst))


def main():
    parse = argparse.ArgumentParser()
    parse.add_argument('-o', '--output', help='Add file path to the output file', type=str)

    args = parse.parse_args()

    source_code = "output.txt"
    # if no output file is provided 
    if(args.output is None):
        print("No output file provided. Using ./output.txt")
        args.output = "parser_output.txt"

    output_file = open(args.output, "w", encoding="utf8")
    # create a token stream
    token_stream = TokenStream(source_code)
    # create a CST
    run(token_stream, output_file)

if __name__ == '__main__':
    main()