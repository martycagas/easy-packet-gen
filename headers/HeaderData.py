"""
Base protocol data structure

Used to convert a header data into an arbitrary output formats
"""


# TODO: Add docstrings
class HeaderData:
    def __init__(self, header_data: list):
        self.header_data = header_data

    def __repr__(self):
        return self, self.header_data

    def __str__(self):
        """
        Outputs the object in the default format - string representation of the hexadecimal values with space as the
        delimiter.
        """
        ret_string = ''
        for item in self.header_data:
            ret_string = ret_string + ' {:02x}'.format(item)
        return ret_string.strip()

    def to_dec_str(self) -> str:
        ret_string = ''
        for item in self.header_data:
            ret_string = ret_string + ' {:03d}'.format(item)
        return ret_string.strip()
