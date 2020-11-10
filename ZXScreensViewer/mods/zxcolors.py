h, f = 0xD7, 0xFF


class ZXColors:

    def __init__(self):

        r = [bytearray([0, 0, 0, 0]), bytearray([h, 0, 0, 0]), bytearray([0, 0, h, 0]), bytearray([h, 0, h, 0]),
             bytearray([0, h, 0, 0]), bytearray([h, h, 0, 0]), bytearray([0, h, h, 0]), bytearray([h, h, h, 0]),
             bytearray([0, 0, 0, 0]), bytearray([f, 0, 0, 0]), bytearray([0, 0, f, 0]), bytearray([f, 0, f, 0]),
             bytearray([0, f, 0, 0]), bytearray([f, f, 0, 0]), bytearray([0, f, f, 0]), bytearray([f, f, f, 0])]

        self.colors = r

    def getcolor(self, idx):
        return self.colors[idx]


def byte_to_pixels(bval, attr, zxcolors: ZXColors) -> bytearray:

    mask = 0x80

    hattr = 8 if (attr >> 6) & 1 else 0
    idx1 = hattr + (attr & 7)
    idx2 = hattr + ((attr >> 3) & 7)

    c1 = zxcolors.getcolor(idx1)
    c2 = zxcolors.getcolor(idx2)

    r = bytearray()
    for i in range(8):
        r.extend(c1 if bval & mask else c2)
        mask >>= 1

    return r
