def zxscr_lineaddr(linen):

    n = linen >> 6
    linen &= 0x3F
    d = linen % 8
    addr = (n * 2048) + ((linen >> 3) * 32) + (d * 8 * 32)

    return addr