import sys
from struct import unpack, pack
from collections import OrderedDict

sys.path.append('../../libs')
from base import *


class T2GF(NamedStructWithMagic, OrderedDict):
    FORMATS = (
        ('I', 'zero'),
        ('I', 'one'),
        ('I', 'num'),
        ('48s', 'dummy'),
    )

    def __init__(self, io=None):
        OrderedDict.__init__(self)
        NamedStructWithMagic.__init__(self, io)

    def load(self, io):
        super().load(io)
        assert self.zero == 0
        assert self.one == 1
        assert self.dummy == b'\x00' * 48

        for i in range(self.num):
            (index,) = unpack('I', io.read(4))
            assert i == index
            name = io.read(0x34).strip(b'\x00').decode('ascii')
            size, total_size = unpack('II', io.read(8))
            buf = io.read(total_size)[:size]
            self[name] = buf

    def save(self, io):
        super().save(io)

        for i, (name, buf) in enumerate(self.items()):
            size = AlignUp(len(buf), 0x40)
            io.write(pack('I52sII', i, name.encode('ascii'), len(buf), size))
            io.write(buf)
            io.write(b'\x00' * (size - len(buf)))

    def dump_all(self):
        for name, buf in self.items():
            open(name, 'wb').write(buf)

    def replace(self, name, buf):
        self[name] = buf

    def __str__(self):
        s = []
        for i, (name, buf) in enumerate(self.items()):
            s.append(f'{i} {len(buf):08x} {name} ')
        return '\n'.join(s)


if __name__ == '__main__':
    t2g = T2GF(open(sys.argv[1], 'rb'))
    print(t2g)
    t2g.save(open('1.bin', 'wb'))
