"""
Base protocol data structure

Used to convert a header data into an arbitrary output formats
"""


class PacketData:
    def __init__(self):
        self.header_list = []

    def __repr__(self):
        return self, self.header_list

    def __str__(self):
        pass

    def to_pcap(self):
        pass
