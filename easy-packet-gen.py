#!/usr/bin/env python3

# stdlib imports
from sys import exit, stdout, stderr
from argparse import ArgumentParser
from pathlib import Path
from json import load
from random import randrange

# custom imports
from headers import *


# TODO: Add docstrings
def main():
    parser = ArgumentParser(prog='Easy Packet Generator', description='Generate a packet file')
    parser.add_argument('template', action='store', type=str,
                        help='Relative or full path to the file containing the template for generating packets')
    parser.add_argument('--count', action='store', type=int, default=1, help='Number of packets to generate')
    parser.add_argument('--struct-dir', action='store', type=str, default='./default',
                        help='Relative or full path to the directory containing packet structure definitions')
    parser.add_argument('--out-format', action='store', type=int, default=1,
                        help='Format of the output file: 1 - text (hex), 2 - text (dec), 3 - binary. Default: 1')
    parser.add_argument('--diff-output', action='store', type=str, default=None,
                        help='File name for the reference file (for use with text diff programs).')
    parser.add_argument('--diff-format', action='store', type=int, default=1,
                        help='Format of the reference file: 1 - text (hex), 2 - text (dec), 3 - binary. Default: 1')
    parser.add_argument('-f', '--fast', action='store_true',
                        help='Omits checksum/length/etc. calculations, producing invalid packets, but running faster.')
    parser.add_argument('--full-rand', action='store_true',
                        help='Completely randomizes the payload. Warning: Causes the generator to run slower!')
    parser.add_argument('-s', '--silent', action='store-true',
                        help='Suppresses all output messages (stdout and stderr). Overrides --verbose')
    parser.add_argument('-v', '--verbose', action='count', default=0, help='Outputs messages to stdout')
    parser.add_argument('--version', action='version', version='%(prog)s 0.1')

    arguments = parser.parse_args()

    if arguments.count < 1:
        print('Argument error: packet count must not be less than 1.'
              'Run easy-packet-parser -h|--help for more info.', file=stderr)
        exit(2)

    # TODO: Implement and remove
    if arguments.diff_output is not None:
        print('Diff output is not yet implemented. Please run without the --diff-output option', file=stderr)
        exit(10)

    config = {}

    # read config
    try:
        with open('config/config.json') as file:
            data = load(file)
            del data
    except IOError as exp:
        if not arguments.silent and arguments.verbose > 0:
            print('Config file not found: {0}'.format(exp), file=stdout)
    except KeyError as exp:
        if not arguments.silent:
            print('Config file syntax error: {0}'.format(exp), file=stderr)
        exit(3)

    # read headers
    try:
        with open(arguments.template, 'r') as file:
            known_headers = load(file)
            if not isinstance(known_headers, list):
                raise TypeError
    except IOError as exp:
        print('Headers file I/O error: {0}'.format(exp), file=stderr)
        exit(1)
    except TypeError as exp:
        print('Headers file syntax error: {0}'.format(exp), file=stderr)
        exit(1)

    # read packet template
    try:
        with open(arguments.template, 'r') as file:
            data = load(file)
            headers_template = data['headers']
            payload_template = data['payload']
            del data
    except IOError as exp:
        print('Template file I/O error: {0}'.format(exp), file=stderr)
        exit(1)
    except KeyError as exp:
        print('Template file syntax error: {0}'.format(exp), file=stderr)
        exit(3)

    # Parse template and prepare header generators
    generators = {}

    for header in headers_template:
        if header in known_headers:
            if header in generators:
                continue
            else:
                try:
                    with open('default/' + header + '.struct.json', 'r') as file:
                        data = load(file)
                        generators[header] = HeaderGen(data)
                        del data
                except IOError as exp:
                    print('File I/O error: {0}'.format(exp), file=stderr)
                    exit(1)
        else:
            print('Unrecognized header in the template', file=stderr)
            exit(3)

    # Prepare and truncate the output file
    try:
        with open('./output.pak', 'w'):
            pass
    except IOError as exp:
        print('File I/O error: {0}'.format(exp), file=stderr)
        exit(1)

    # Generate packets
    for i in range(arguments.count):
        # Generate the packet's payload
        payload = []
        payload_length = payload_template['length']

        if not arguments.full_rand:
            payload_byte = str(hex(randrange(256)))
            for j in range(payload_length):
                payload.append(payload_byte)
            del payload_byte
        else:
            for j in range(payload_length):
                payload.append(str(hex(randrange(256))))

        packet = payload

        for header in reversed(headers_template):
            new_header = generators[header].generate_header(packet, arguments.use_fast)
            packet = new_header.extend(packet)

        with open('./output.pak', 'a') as file:
            file.write(str(len(packet)))
            file.writelines(packet)


if __name__ == '__main__':
    main()
