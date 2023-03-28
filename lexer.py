import ply.lex as lex
from prettytable import PrettyTable
import os
from colorama import Fore, Style, init
import argparse


init(autoreset=True)

def print_fancy(text, width=80, fill_char='-'):
    print(text.center(width, fill_char))

# List of token names that the lexer should recognize
reserved = {
    'function': 'FUNCTION',
    'return': 'RETURN',
    'init': 'INIT',
    'play': 'PLAY',
    'move': 'MOVE',
    'shoot': 'SHOOT',
    'place_wumpus': 'PLACE_WUMPUS',
    'place_pit': 'PLACE_PIT',
    'place_gold': 'PLACE_GOLD',
    'clear_room': 'CLEAR_ROOM',
    'north': 'NORTH',
    'south': 'SOUTH',
    'east': 'EAST',
    'west': 'WEST',
    'true': 'BOOLEAN',
    'false': 'BOOLEAN',
    'and': 'LOGIC',
    'or': 'LOGIC',
    'const': 'CONSTANT',
    'while': 'WHILE',
    'if': 'IF',
    'else': 'ELSE',
    'bool': 'DATATYPE',
    'int': 'DATATYPE',
    'grab': 'GRAB',
    'grid_size': 'GRID_SIZE',
    'sense_stench': 'SENSE_STENCH',
    'sense_breeze': 'SENSE_BREEZE',
    'sense_glitter': 'SENSE_GLITTER',
    'print_position': 'PRINT_POSITION',
    'void': 'VOID',

}
# List of token names
tokens = (
    'ID', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'COMMA', 'INTEGER', 'FUNCTION',
    'RETURN', 'INIT', 'PLAY', 'MOVE', 'SHOOT', 'PLACE_WUMPUS', 'PLACE_PIT', 'PLACE_GOLD',
    'CLEAR_ROOM', 'NORTH', 'SOUTH', 'EAST', 'WEST', 'BOOLEAN', 'VOID', 'OPERATOR',
    'COMPARISON', 'LOGIC', 'SPACE', 'COMMENT', 'CONSTANT', 'IF',
    'ELSE', 'LEFTBRACKET', 'RIGHTBRACKET', 'ASSIGNMENT', 'DATATYPE', 'GRAB',
    'GRID_SIZE', 'SENSE_STENCH', 'SENSE_BREEZE', 'SENSE_GLITTER', 'PRINT_POSITION', 'WHILE', 'VOID',
)

# Characters to ignore while lexing
t_ignore = r'\t|\n| '

# Regular expressions for tokens
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = r','
t_INTEGER = r'[0-9]+'
t_OPERATOR = r'\+|-'
t_COMPARISON = r'==|!=|<=|<|>=|>'
t_LOGIC = r'and|or'
t_COMMENT = r'\$.+\$'
t_LEFTBRACKET = r'\['
t_RIGHTBRACKET = r'\]'
t_ASSIGNMENT = r'='

# Error handling rule
def t_error(t):
    # Print an error message
    print(Fore.RED + Style.BRIGHT + f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}" + Style.RESET_ALL)
    t.lexer.skip(1)

def t_ID(t):
    r'[a-zA-Z][_a-zA-Z0-9]{0,15}'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Function to test lexer with a given input string
def run_lexer(input_string, lexer):
    lexer.input(input_string)
    table = PrettyTable(["Token Type", "Value", "Line", "Position"])
    stream = []
    while True:
        tok = lexer.token()
        
        if not tok:
            break
        token_type = tok.type
        token_value = tok.value
        values = [token_type, token_value, tok.lineno, tok.lexpos]
        
        if token_type == 'COMMENT':
            token_type = Fore.YELLOW + token_type + Style.RESET_ALL
            token_value = Fore.YELLOW + token_value + Style.RESET_ALL
        elif token_type in ('OPERATOR', 'COMPARISON', 'LOGIC', 'ASSIGNMENT'):
            token_type = Fore.BLUE + token_type + Style.RESET_ALL
            token_value = Fore.BLUE + token_value + Style.RESET_ALL
        elif token_type not in reserved.values():
            token_type = Fore.MAGENTA + token_type + Style.RESET_ALL
            token_value = Fore.MAGENTA + token_value + Style.RESET_ALL
        else:
            token_type = Fore.GREEN + token_type + Style.RESET_ALL
            token_value = Fore.GREEN + token_value + Style.RESET_ALL
            
        table.add_row([token_type, token_value, tok.lineno, tok.lexpos])

        stream.append(values)

    print(table)
    return stream

# Function to test lexer with files in a specified folder
def run_lexer_with_file(source_code, lexer, output_file):
    # Print the name of the file being run with colorama
    print(Fore.CYAN + Style.BRIGHT + f"Testing file: {source_code}" + Style.RESET_ALL)
    # Open the file and read the contents
    with open(source_code, 'r') as file:
        test_input = file.read()
        stream = run_lexer(test_input, lexer)
        for token in stream:
            output_file.write(f"{token[0]} {token[1]} {token[2]} {token[3]}\n")

        print(Fore.GREEN + Style.BRIGHT + "Lexing successful" + Style.RESET_ALL)

def main():

    parse = argparse.ArgumentParser()
    parse.add_argument('-f', '--file', help='Add file path to the source code', type=str)
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
        print_fancy("python3 lexer.py -f <file_path>", fill_char='.')

        print("Parameters:")
        print_fancy(Fore.CYAN + Style.BRIGHT + "-f, --file" + Style.RESET_ALL, fill_char='=')
        print("\tInclude the source code file path")
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
        args.output = "output.txt"

    output_file = open(args.output, "w", encoding="utf8")
    # Create the lexer
    lexer = lex.lex(debug=args.debug)
    run_lexer_with_file(source_code, lexer, output_file)

if __name__ == "__main__":
    main()