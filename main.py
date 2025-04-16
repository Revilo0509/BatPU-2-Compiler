import argparse
import os
import re
import sys

# Global dictionary to store variable names and their memory addresses
Variables = {}
NextMemoryAddress = 0  # Tracks the next available memory address (0-239)

def tokenize(file_path):
    """Tokenizes the content of a file into a list of (token, line_number) tuples."""
    if not os.path.exists(file_path):
        sys.exit(f"Error: File '{file_path}' does not exist.")
    with open(file_path, 'r') as file:
        content = file.readlines()
    
    tokens = []
    for line_number, line in enumerate(content, start=1):
        # Match strings in quotes, words, parentheses, or equals
        line_tokens = re.findall(r'"[^"]*"|\b\w+\b|\(|\)|=', line)
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
        token = Tokens.pop(0)[0]
        arguments.append(token)
        if len(arguments) == expected_count:
            break

    # Ensure there is a closing parenthesis
    if not Tokens or Tokens[0][0] != ")":
        sys.exit(f"Error on line {line_number}: {function_name} Missing closing parenthesis ')'.")

    Tokens.pop(0)  # Remove ')'
    return arguments

def handle_print(argument, line_number):
    """Generates assembly code for the 'print' function."""
    compiled = []

    if argument.startswith('"') and argument.endswith('"'):  # Check if the argument is a string
        # Remove the surrounding quotes
        string_content = argument[1:-1]
        # Handle printing characters to the character buffer
        compiled.extend([
            "LDI r15 clear_chars_buffer",
            "STR r15 r0",
            "LDI r15 write_char"
        ])

        for char in string_content:
            compiled.append(f"LDI r14 \"{char}\"")
            compiled.append("STR r15 r14")
        
        compiled.extend([
            "LDI r15 buffer_chars",
            "STR r15 r0"
        ])
    elif argument.isdigit():  # Check if the argument is a number
        # Handle printing numbers to the Number Display
        compiled.extend([
            f"LDI r14 {argument}",  # Load the number into r14
            "LDI r15 250",         # Load the memory address for 'Show Number'
            "STR r15 r14"          # Store the number to the display
        ])
    elif argument in Variables:  # Check if the argument is a declared variable
        # Debugging: Print variable usage
        print(f"Printing variable '{argument}' with address {Variables[argument]}")
        
        # Handle printing the value of a variable
        memory_address = Variables[argument]
        compiled.extend([
            f"LDI r15 {memory_address}",  # Load the memory address of the variable into r15
            "LOD r15 r14",               # Load the variable's value into r14
            "LDI r15 250",               # Load the memory address for 'Show Number'
            "STR r15 r14"                # Store the value to the display
        ])
    else:
        sys.exit(f"Error on line {line_number}: Invalid argument for print statement.")
    
    return compiled

def handle_variable_declaration(variable, value, line_number):
    """Generates assembly code for variable declarations."""
    global NextMemoryAddress

    if variable in Variables:
        sys.exit(f"Error on line {line_number}: Variable '{variable}' is already declared.")

    if NextMemoryAddress > 239:
        sys.exit("Error: Memory limit exceeded. No more variables can be declared.")

    if not value.isdigit():
        sys.exit(f"Error on line {line_number}: Only numeric values are supported for variables.")

    # Assign the next available memory address to the variable
    Variables[variable] = NextMemoryAddress
    memory_address = NextMemoryAddress
    NextMemoryAddress += 1

    # Generate assembly code to store the value in the variable's memory location
    compiled = [
        f"LDI r14 {value}",  # Load the value into r14
        f"LDI r15 {memory_address}",  # Load the memory address into r15
        "STR r15 r14"  # Store the value in the variable's memory location
    ]
    
    return compiled

def run():
    """Processes tokens and generates compiled assembly code."""
    compiled = []

    while Tokens:
        token, line_number = Tokens[0]

        if token == "print":
            arguments = get_arguments(1)
            if arguments:
                argument = arguments[0]
                compiled.extend(handle_print(argument, line_number))  # Always call handle_print
        elif len(Tokens) > 2 and Tokens[1][0] == "=":  # Check for variable declaration
            variable = Tokens.pop(0)[0]  # Get the variable name
            Tokens.pop(0)  # Remove the '=' token
            value = Tokens.pop(0)[0]  # Get the value
            compiled.extend(handle_variable_declaration(variable, value, line_number))
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