"""
IPV4 header representation structure and generator
"""

__version__ = '0.0.1'

__all__ = [
    'Ipv4Header',
    'Ipv4HGen'
]


class Ipv4Header:
    def __init__(self):
        pass

    def __repr__(self):
        pass

    def __str__(self):
        pass


class Ipv4HGen:
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
