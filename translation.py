def bytelist2int(bytelist):
    return int(''.join([hex(x)[2:].zfill(2) for x in bytelist]), 16)

def int2bytelist(integer, length):
    if integer < 0:
        print("Not a right integer.")
        return None
    a = bytes().fromhex(hex(integer)[2:].zfill(2 * length))
    if (len(a) > length):
        print("Too small integer.")
        return None
    else:
        return a

