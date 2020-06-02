"""
Universal header generator
"""

from sys import exit, stderr
from random import randrange, choice

from .HeaderData import HeaderData


# TODO: Add docstrings
class HeaderGen:
    def __init__(self, data: dict):
        self.header_name = 'HEADER NAME ERROR'
        try:
            self.header_name = data['hdr_name']
            self.header_length = data['hdr_length']
            self.header_structure = data['hdr_structure']
            for item in self.header_structure:
                if 'name' not in item or 'length' not in item:
                    raise KeyError
        except KeyError as exp:
            print('{0} header generator: {1}'.format(self.header_name, exp), file=stderr)
            exit(3)

    def __repr__(self):
        return self, self.header_structure

    def __str__(self):
        print('Header generator object'
              'Fields definition:')
        for item in self.header_structure:
            print('\t' + item['name'] + ': ' + str(item['length']))

    def generate_header(self, payload: list, use_fast: bool) -> HeaderData:
        new_header_data = []
        bit_string = ''

        for item in self.header_structure:
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
                            bit_string += format_string.format(len(payload))
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
            except KeyError as exp:
                print('{0} header generator: Invalid value format of the item' + item['name'], file=stderr)
                exit(3)

            while len(bit_string) > 8:
                new_header_data.append(int(bit_string[0:8], 2))
                bit_string = bit_string[8:]

        return HeaderData(new_header_data)
