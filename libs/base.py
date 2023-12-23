from struct import Struct, pack
from io import BytesIO
from collections import namedtuple
import os


def AlignUp(offset, align):
    align -= 1
    return (offset + align) & ~align


def WritePadding(io, align, value=b'\x00'):
    align -= 1
    offset = io.tell()
    size = ((offset + align) & ~align) - offset
    io.write(value * size)


class Base:
    def __init__(self, io=None):
        if io:
            self.load(io)

    def load(self, io):
        raise NotImplementedError

    def save(self, io):
        raise NotImplementedError

    def getvalue(self):
        io = BytesIO()
        self.save(io)
        return io.getvalue()


class NamedStruct(Base):
    FORMATS = ()

    def __init__(self, io=None):
        fmts = '<' + ''.join([f[0] for f in self.FORMATS])
        self.struct = Struct(fmts)
        names = [f[1] for f in self.FORMATS]
        self.__dict__.update(namedtuple(self.__class__.__name__, names).__dict__)
        super().__init__(io)

    def load(self, io):
        for i, value in enumerate(self.struct.unpack(io.read(self.struct.size))):
            self.__setattr__(self._fields[i], value)

    def save(self, io):
        values = [self.__getattribute__(field) for field in self._fields]
        io.write(self.struct.pack(*values))

    def getsize(self):
        return self.struct.size


class NamedStructWithMagic(NamedStruct):
    MAGIC = None

    def __init__(self, io=None):
        if self.MAGIC is None:
            self.MAGIC = self.__class__.__name__.encode('ascii')
        NamedStruct.__init__(self, io)

    def load(self, io):
        if io.read(len(self.MAGIC)) != self.MAGIC:
            raise TypeError
        super().load(io)

    def save(self, io):
        io.write(self.MAGIC)
        super().save(io)
