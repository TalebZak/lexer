# LL(1) parser that used the lexer's output to parse the input according to grammar.txt's rules

import sys
from colorama import Fore, Style, init
import argparse

def print_fancy(text, width=80, fill_char='-'):
    print(text.center(width, fill_char))

class Token:
    def __init__(self, token):
        self.token_type = token[0]
        self.token_value = token[1]
        self.token_line = token[2]
        self.token_column = token[3]

    def __str__(self):
        return f'{self.token_value}'
    
class TokenStream:
    def _init__(self, source):
        self.source = source
        # open the file
        self.stream = open(self.source, 'r')

    def get_token(self):
        # get the following line in the file
        line = self.stream.readline().strip()
        # if the line is empty, return None
        if line == '':
            return None
        # split the line into a list of tokens
        token = Token(line.split())
        token_type = token.token_type
        # if the token is a comment, call get token again
        if token_type == 'COMMENT':
            return self.get_token()
        # return the token
        return token
    

class TreeNode:
    '''
    Define a node in the CST
    The CST is an N-ary tree
    '''
    def __init__(self, val, parent=None, token=None):
        self.children = []
        self.parent = parent
        self.token = token
        self.val = val
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
            return self.token
        # if the node is not a leaf node, return the token and return the representation of the children
        result = self.token[0] + '\n'
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

def ID(token_stream, parent):
    # if the current token is an ID
    token = token_stream.get_token()
    if token.token_type == 'ID':
        # create a node with the token as the value
        node = TreeNode('ID', token=token)
        # return the node
        return node
    if token.token_type == 'EOF':
        raise MissingTokenError('ID')
    # if the current token is not an ID, raise an error
    raise ExpectationError(token, 'ID')

def INTEGER(token_stream):
    # if the current token is an INT
    token = token_stream.get_token()
    if token.token_type == 'INTEGER':
        # create a node with the token as the value
        node = TreeNode('INTEGER', token=token)
        # return the node
        return node
    if token.token_type == 'EOF':
        raise MissingTokenError('INTEGER')
    raise ExpectationError(token, 'INTEGER')

def BOOLEAN(token_stream):
    # if the current token is a BOOLEAN
    token = token_stream.get_token()
    if token.token_type == 'BOOLEAN':
        # create a node with the token as the value
        node = TreeNode('BOOLEAN', token=token)
        # return the node
        return node
    if token.token_type == 'EOF':
        raise MissingTokenError('BOOLEAN')
    raise ExpectationError(token, 'BOOLEAN')

def direction(token_stream):
    # a direction is either a token EAST, WEST, NORTH, SOUTH
    
def parse(token_stream):
    print("Parsing...")
    # create the root node, aka the program node
    root = TreeNode('<program>')


def run(token_stream, output_file):
    # parse the token stream
    cst = parse(token_stream)
    # print the CST
    print(cst)
    # write the CST to the output file
    output_file.write(str(cst))
def main():
    parse = argparse.ArgumentParser()
    parse.add_argument('-d', '--debug', help='Activate debug mode', action='store_true')
    parse.add_argument('-o', '--output', help='Add file path to the output file', type=str)

    args = parse.parse_args()

    # if no source code file is provided

    if args.file is None:
        # set color to red and bright
        print_fancy("")
        print_fancy("Error: Input file missing", fill_char='*')
        print_fancy("")

        print("Usage:")
        print_fancy("python3 wumpus_parser.py", fill_char='.')

        print("Parameters:")
        print_fancy(Fore.CYAN + Style.BRIGHT + "-d, --debug" + Style.RESET_ALL, fill_char='=')
        print("\tExecute the program in debug mode")
        print_fancy(Fore.CYAN + Style.BRIGHT + "-o, --output" + Style.RESET_ALL, fill_char='=')
        print("\tSpecify the output file path")

        print_fancy("", fill_char='-')
        exit(1)
    source_code = args.file
    # if no output file is provided 
    if(args.output is None):
        print("No output file provided. Using ./output.txt")
        args.output = "parser_output.txt"

    output_file = open(args.output, "w", encoding="utf8")
    # create a token stream
    token_stream = TokenStream(source_code)
    # create a CST
    run(token_stream)
