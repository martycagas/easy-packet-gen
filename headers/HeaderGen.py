"""
Universal header generator
"""

from sys import exit, stderr
from random import randrange, choice

from .HeaderData import HeaderData


# TODO: Add docstrings
class HeaderGen:
    def __init__(self, structure: list):
        for i, item in enumerate(structure):
            if 'name' not in item or 'length' not in item:
                print('Ethernet header generator: Invalid packet structure format at index: ' + str(i), file=stderr)
                exit(3)
        self.packet_structure = structure

    def __repr__(self):
        return self, self.packet_structure

    def __str__(self):
        print('Ethernet header generator object'
              'Fields definition:')
        for item in self.packet_structure:
            print('\t' + item['name'] + ': ' + str(item['length']))

    def generate_header(self, packet: list, use_fast: bool) -> HeaderData:
        new_header_data = []
        bit_string = ''
        bits_read = 0

        for item in self.packet_structure:
            try:
                item_length = item['length']
                format_string = '{:0' + item_length + 'b}'
                if (use_fast is True) or ('value' not in item):
                    bit_string += format_string.format(randrange(2 ** item_length))
                else:
                    item_value = item['value']
                    item_value_type = item_value['type']
                    if item_value_type == 'const':
                        item_value_values = item_value['values']
                        bit_string += format_string.format(item_value_values[0])
                    elif item_value_type == 'random':
                        bit_string += format_string.format(randrange(2 ** item_length))
                    elif item_value_type == 'enum':
                        item_value_base = item_value['base']
                        item_value_values = item_value['values']
                        enum_choice = choice(item_value_values)
                        bit_string += format_string.format(int(enum_choice, item_value_base))
                    elif item_value_type == 'length':
                        item_value_of = item_value['of']
                        if item_value_of == 'payload':
                            bit_string += format_string.format(len(packet))
                        elif item_value_of == 'header':
                            pass
                        elif item_value_of == 'all':
                            pass
                        else:
                            raise KeyError
                    elif item_value_type == 'checksum':
                        item_value_of = item_value['of']
                        if item_value_of == 'payload':
                            pass
                        elif item_value_of == 'header':
                            pass
                        elif item_value_of == 'all':
                            pass
                        else:
                            raise KeyError
                    else:
                        raise KeyError
                bits_read += item_length
            except (KeyError):
                print('Ethernet header generator: Invalid value format of the item' + item['name'], file=stderr)
                exit(3)

            if bits_read > 32:
                new_header_data.append(int(bit_string[0:8], 2))
                new_header_data.append(int(bit_string[8:16], 2))
                new_header_data.append(int(bit_string[16:24], 2))
                new_header_data.append(int(bit_string[24:32], 2))
                bits_read = 0
                bit_string = ''

        return HeaderData(new_header_data)
