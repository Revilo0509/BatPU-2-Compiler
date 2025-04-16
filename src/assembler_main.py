from assembler import assemble
from schematic import make_schematic
import argparse
import os
import sys

def parse_arguments():
    parser = argparse.ArgumentParser(description='Assemble and create a schematic for a program.')
    parser.add_argument('program', type=str, help='The name of the program to assemble and create a schematic for.')
    return parser.parse_args()

def main():
    args = parse_arguments()
    program = args.program

    # Define file paths
    base_name = os.path.splitext(program)[0]
    as_filename = os.path.join('programs', f'{program}.as')
    mc_filename = os.path.join('programs/binaries', f'{base_name}.mc')
    schem_filename = os.path.join('schem', f'{base_name}.schem')
    
    # Check if the input file exists
    if not os.path.isfile(as_filename):
        print(f"Error: The file '{as_filename}' does not exist.", file=sys.stderr)
        sys.exit(1)

    # Perform assembly and schematic creation
    try:
        assemble(as_filename, mc_filename)
        make_schematic(mc_filename, schem_filename)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()