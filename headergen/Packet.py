"""
Base protocol data structure

Used to convert a header data into an arbitrary output formats
"""


class PacketData:
    def __init__(self):
        self.data = []

    def __repr__(self):
        return self, self.data

    def __str__(self):
        return self.to_str_hex()

    def to_str_hex(self) -> str:
        """
        Returns the string of the data in the base 16 format
        :return:
        """
        ret_str = ''
        for item in self.data:
            pass
        return ret_str.strip()

    def to_str_dec(self) -> str:
        """
        Returns the string of the data in the base 10 format
        :return:
        """
        ret_str = ''
        for item in self.data:
            pass
        return ret_str.strip()

    def to_str_oct(self) -> str:
        """
        Returns the string of the data in the base 8 format
        :return:
        """
        ret_str = ''
        for item in self.data:
            pass
        return ret_str.strip()

    def to_pcap(self) -> str:
        pass
