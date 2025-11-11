#!/usr/bin/env python3
import argparse
from sys import stdin


def exit_usage():
    print('usage: <search_term> <file to search> [-i in_file] [-t file_type]')


def parse_stdin(search_term, file_type):
    """open stdin and pass to parse_file"""
    with open(stdin) as f:
        return parse_file(f, file_type)


def parse_file(search_term, field, in_file, file_type):
    pass


def main(search_term, field='fingerprint', in_file=None, file_type=None):
    if not in_file or in_file == '-':
        # read from stdin
        if not file_type:
            exit_usage()
        else:
            print(parse_stdin(search_term, file_type))
        print(parse_file(search_term, field, in_file, file_type))
    elif not file_type:
        if '.' in in_file:
            file_type = in_file.split('.')[-1]
        else:
            exit_usage()
    print(parse_file(search_term, field, in_file, file_type))


if __name__ == '__main__':
    """Command-line arguments:
    - search term (positional or keyword)
    - search field (default to 'fingerprint')
    - input file (default to stdin)
    - file type (default based on file extension)
    """
    parser = argparse.ArgumentParser()
    # search term / search value - positional, required first argument
    parser.add_argument('search_term', nargs='1', help='term to search for')
    # input file
    parser.add_argument('in_file', nargs='?', default='-', help='input file to search (default: stdin)')
    parser.add_argument('-t', '--file_type', required=False, default='-', help='override the file extension (or provide the type if no extension is provided in the file name)')
    # search field
    parser.add_argument('-f', '--field', required=False, default='fingerprint', help='field to search (default: fingerprint)')
    args = parser.parse_args()

    if not args.search_term:
        exit_usage()

    main(args.search_term, args.field, args.in_file, args.file_type)
