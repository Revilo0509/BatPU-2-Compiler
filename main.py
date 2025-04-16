import argparse
import os
import re
import sys

def tokenize(file_path):
    """Tokenizes the content of a file into a list of (token, line_number) tuples."""
    if not os.path.exists(file_path):
        sys.exit(f"Error: File '{file_path}' does not exist.")
    with open(file_path, 'r') as file:
        content = file.readlines()
    
    tokens = []
    for line_number, line in enumerate(content, start=1):
        line_tokens = re.findall(r'\b\w+\b|\(|\)|"', line)
        tokens.extend((token, line_number) for token in line_tokens)
    return tokens

def get_arguments(expected_count):
    """Parses and retrieves the expected number of arguments from the token list."""
    if not Tokens:
        sys.exit("Error: No tokens available to parse arguments.")

    function_name, line_number = Tokens[0]  # Peek at the first token without popping it

    # Ensure the token list is not empty and the second token is an opening parenthesis
    if not Tokens or len(Tokens) < 2 or Tokens[1][0] != "(":
        sys.exit(f"Error on line {line_number}: {function_name} Expected opening parenthesis '('.")

    Tokens.pop(0)  # Remove the function name
    Tokens.pop(0)  # Remove '('
    arguments = []

    while Tokens and Tokens[0][0] != ")":
        arguments.append(Tokens.pop(0)[0])
        if len(arguments) == expected_count:
            break

    # Ensure there is a closing parenthesis
    if not Tokens or Tokens[0][0] != ")":
        sys.exit(f"Error on line {line_number}: {function_name} Missing closing parenthesis ')'.")

    Tokens.pop(0)  # Remove ')'
    return arguments

def handle_print(argument, line_number):
    """Generates assembly code for the 'print' function."""
    if len(argument) > 10:
        sys.exit(f"Error on line {line_number}: Token too long.")

    compiled = [
        "LDI r15 clear_chars_buffer",
        "STR r15 r0",
        "LDI r15 write_char"
    ]

    for char in argument:
        compiled.append(f"LDI r14 \"{char}\"")
        compiled.append("STR r15 r14")
    
    compiled.extend([
        "LDI r15 buffer_chars",
        "STR r15 r0"
    ])
    return compiled

def run():
    """Processes tokens and generates compiled assembly code."""
    compiled = []

    while Tokens:
        token, line_number = Tokens[0]

        if token == "print":
            arguments = get_arguments(1)
            if arguments:
                compiled.extend(handle_print(arguments[0], line_number))
        else:
            print(f"Error on line {line_number}: Unrecognized token '{token}'.")
            Tokens.pop(0)

    compiled.append("HLT")
    print("\n".join(compiled))

def main():
    """Main entry point for the compiler."""
    parser = argparse.ArgumentParser(description='Compile a Pulang program to a .schem file.')
    parser.add_argument('file', type=str, nargs='?', help='The file to compile.')  # Make the argument optional
    args = parser.parse_args()

    # Prompt for the file argument if it's missing
    if not args.file:
        args.file = input("Please enter the name of the file to compile (without extension): ").strip()

    pulang_folder_path = "pulang"
    pulang_program_path = os.path.join(pulang_folder_path, f"{args.file}.pulang")

    global Tokens
    Tokens = tokenize(pulang_program_path)

    print("Tokens:", Tokens)
    run()

if __name__ == "__main__":
    main()