import os


def ReadBinaryFile(fname) -> bytearray:
    r = bytearray()
    if os.path.isfile(fname):
        with open(fname, "rb") as binaryfile:
            r = bytearray(binaryfile.read())
    return r