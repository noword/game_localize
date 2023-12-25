import sys
from struct import unpack, pack
from collections import OrderedDict

sys.path.append('../../libs')
from base import *


class T2gFile(NamedStruct):
    FORMATS = (('I', 'index'), ('52s', 'name_bytes'), ('I', 'size'), ('I', 'aligned_size'))

    def load(self, io):
        super().load(io)
        self.buf = io.read(self.aligned_size)[: self.size]

    def save(self, io):
        super().save(io)
        io.write(self.buf)
        io.write(b'\x00' * (self.aligned_size - self.size))

    def replace(self, buf):
        self.buf = buf
        self.size = len(buf)
        self.aligned_size = AlignUp(self.size, 0x40)

    @property
    def name(self):
        return self.name_bytes.strip(b'\x00').decode('ascii')

    def __str__(self):
        return f'{self.size:08x} {self.name}'


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
            f = T2gFile(io)
            self[f.name] = f

    def save(self, io):
        super().save(io)

        for f in self.values():
            f.save(io)

    def dump(self, name):
        open(name, 'wb').write(self[name].buf)

    def dump_all(self):
        for name, f in self.items():
            open(name, 'wb').write(f.buf)

    def replace(self, name, buf):
        self[name].replace(buf)

    def __str__(self):
        s = []
        for i, f in enumerate(self.values()):
            s.append(f'{i} {f}')
        return '\n'.join(s)


def test():
    from pathlib import Path
    from io import BytesIO

    for name in Path('backup').glob('*.t2g'):
        print(f'test {name}')
        t2g = T2GF(open(name, 'rb'))
        old_bytes = open(name, 'rb').read()
        new_bytes = t2g.getvalue()
        if old_bytes != new_bytes:
            open(f'{name}.new', 'wb').write(new_bytes)
            print(f'test failed on {name}')
            raise TypeError


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('name', action='store', nargs='?')
    parser.add_argument('dump_name', action='store', nargs='?')
    parser.add_argument("--dump_all", action="store_true", default=False)
    parser.add_argument("--test", action="store_true", default=False)
    args = parser.parse_args()

    if args.test:
        test()
    else:
        t2g = T2GF(open(args.name, 'rb'))
        if args.dump_all:
            t2g.dump_all()
        elif args.dump_name:
            t2g.dump(args.dump_name)
        else:
            print(t2g)
