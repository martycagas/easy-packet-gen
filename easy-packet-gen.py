#!/usr/bin/env python3

# stdlib imports
import sys
from argparse import ArgumentParser
from json import load
from random import randrange

# custom imports
from headers.EthHGen import *
from headers.Ipv4HGen import *
from headers.UdpHGen import *


def main():
    parser = ArgumentParser(prog='Easy Packet Generator', description='Generate a packet file')
    # TODO: Add the option for choosing a packet structure directory (aside from the current default directory)
    parser.add_argument('template', action='store', type=str,
                        help='File containing the template for generating packets')
    parser.add_argument('--count', action='store', type=int, default=1, help='Number of packets to generate')
    parser.add_argument('--out-format', action='store', type=int, default=1,
                        help='Format of the output file: 1 - text (hex), 2 - text (dec), 3 - binary. Default: 1')
    parser.add_argument('--diff-output', action='store', type=str, default=None,
                        help='File name for the reference file (for use with text diff programs).')
    parser.add_argument('--diff-format', action='store', type=int, default=1,
                        help='Format of the reference file: 1 - text (hex), 2 - text (dec), 3 - binary. Default: 1')
    parser.add_argument('-f', '--full-rand', action='store_true',
                        help='Completely randomizes the payload. Warning: Causes the generator to run slower!')
    parser.add_argument('--fast', action='store_true',
                        help='Omits checksum/length/etc. calculations, producing invalid packets, but running faster.')
    parser.add_argument('-v', '--verbose', action='count', default=0, help='Outputs messages to stdout')
    parser.add_argument('--version', action='version', version='%(prog)s 0.1')
    arguments = parser.parse_args()

    if (arguments.count < 1):
        print('Argument error: packet count must not be less than 1.', file=sys.stderr)
        print('Run easy-packet-parser -h|--help for more info.', file=sys.stderr)
        sys.exit(2)

    # TODO: Implement and remove
    if (arguments.fast is False):
        print('Valid packet generation is not yet implemented, please run with the --fast option.', file=sys.stderr)
        sys.exit(10)

    # TODO: Implement and remove
    if (arguments.diff_output is not None):
        print('Diff output is not yet implemented. Please run without the --diff-output option', file=sys.stderr)
        sys.exit(10)

    try:
        with open(arguments.template, 'r') as file:
            data = load(file)
            payload_template = data['payload']
            headers_template = data['headers']
            del (data)
    except (IOError):
        print('Template file found not found!', file=sys.stderr)
        sys.exit(1)

    # Parse template and prepare header generators
    generators = []

    for header in headers_template:
        if header == 'eth':
            try:
                with open('default/eth.struct.json', 'r') as file:
                    data = load(file)
                    generators.append(EthHGen(data))
                    del (data)
            except (IOError):
                print(header + ' format file found not found!', file=sys.stderr)
                sys.exit(1)
        elif header == 'ipv4':
            try:
                with open('default/ipv4.struct.json', 'r') as file:
                    data = load(file)
                    generators.append(Ipv4HGen(data))
                    del (data)
            except (IOError):
                print(header + ' format file found not found!', file=sys.stderr)
                sys.exit(1)
        elif header == 'udp':
            try:
                with open('default/udp.struct.json', 'r') as file:
                    data = load(file)
                    generators.append(UdpHGen(data))
                    del (data)
            except (IOError):
                print(header + ' format file found not found!', file=sys.stderr)
                sys.exit(1)
        else:
            print('Unrecognized header in the template', file=sys.stderr)
            sys.exit(3)

    # Prepare and truncate the output file
    try:
        with open('./output.pak', 'w'):
            pass
    except (IOError):
        print('The output file could not be written to or created!', file=sys.stderr)
        sys.exit(1)

    # Generate packets
    for i in range(arguments.count):
        # Generate the packet's payload
        payload = []

        if (arguments.full_rand is False):
            payload_byte = str(hex(randrange(256)))
            for j in range(payload_template['length']):
                payload.append(payload_byte)
            del (payload_byte)
        else:
            for j in range(payload_template['length']):
                payload.append(str(hex(randrange(256))))

        packet = payload

        for generator in reversed(generators):
            header = generator.generate_header(packet)
            packet = header.extend(packet)

        with open('./output.pak', 'a') as file:
            file.write(str(len(packet)))
            file.writelines(packet)


if __name__ == '__main__':
    main()
