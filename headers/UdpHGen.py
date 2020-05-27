"""
UDP header representation structure and generator
"""

__version__ = '0.0.1'

__all__ = [
    'UdpHeader',
    'UdpHGen'
]


class UdpHeader:
    def __init__(self):
        pass

    def __repr__(self):
        pass

    def __str__(self):
        pass


class UdpHGen:
    def __init__(self, struct: list):
        for item in struct:
            if ('name' not in item) or ('length' not in item):
                exit(3)
        self.fields = list

    def __repr__(self):
        pass

    def __str__(self):
        pass

    def generate_header(self, packet: list[str]):
        pass
