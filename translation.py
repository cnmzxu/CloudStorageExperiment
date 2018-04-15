import myerror

def bytelist2int(bytelist):
    return int(''.join([hex(x)[2:].zfill(2) for x in bytelist]), 16)

def int2bytelist(integer, length):
    if integer < 0:
        raise myerror.myerror("Unexcepted_Negative_Integer")
    a = bytes().fromhex(hex(integer)[2:].zfill(2 * length))
    if (len(a) > length):
        raise myerror.myerror("Too_Large_Integer_To_Convert")
        return None
    else:
        return a

def bytelist2bin(bytelist):
    return ''.join([bin(x)[2:].zfill(8) for x in bytelist])

def bin2bytelist(binlist):
    if len(binlist) % 8 != 0:
        raise myerror.myerror("Unmatchable_Length_Binlist")
    return int2bytelist(int(binlist, 2), len(binlist) // 8)
    