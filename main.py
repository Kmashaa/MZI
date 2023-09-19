import binascii

def join_64bits(text):
    crypted_text = 0
    for i in reversed(range(len(text))):
        print(text[i])

        crypted_text |= text[i]
        if i != 0:
            crypted_text = crypted_text << 64
    return crypted_text

def intToHex(int):
    return hex(int)[2:]

def hexToUtf8(text):
    text = binascii.unhexlify(text).decode('utf8')
    text = text.replace('\x00', '')
    return text

def utf8ToHex(text):
    text = binascii.hexlify(text.encode('utf8')).decode('utf8')
    return text


sbox = [
    [4, 10, 9, 2, 13, 8, 0, 14, 6, 11, 1, 12, 7, 15, 5, 3],
    [14, 11, 4, 12, 6, 13, 15, 10, 2, 3, 8, 1, 0, 7, 5, 9],
    [5, 8, 1, 13, 10, 3, 4, 2, 14, 15, 12, 7, 6, 0, 9, 11],
    [7, 13, 10, 1, 0, 8, 9, 15, 14, 4, 6, 12, 11, 2, 5, 3],
    [6, 12, 7, 1, 5, 15, 13, 8, 4, 10, 9, 14, 0, 3, 11, 2],
    [4, 11, 10, 0, 7, 2, 1, 13, 3, 6, 8, 5, 9, 12, 15, 14],
    [13, 11, 4, 1, 3, 15, 5, 9, 0, 10, 14, 7, 6, 8, 2, 12],
    [1, 15, 13, 0, 5, 7, 10, 4, 9, 2, 3, 14, 6, 11, 8, 12],
]

def func(A,X):
    temp = A^X
    # print(temp,"tttt")
    seq=list()
    for i in range(8):
        seq.append((temp>>(4*(7-i)))&0xF)
    print(seq)

    for i in range(8):
        seq[i]=sbox[i].index(seq[i])
        print(bin(seq[i]))
    print(seq)
    result=0
    for i in range(8):
        result |= seq[i]<<(7*4-i*4)
    print(bin(result))
    mask = (1 << 32) - 1

    result = (((result >> 11) | (result << (32 - 11)))) & mask
    print("before", result)

    return result

def gen_key(key,type):

    if type=="enc":
        keys = list()
        for i in range(8):
            keys.append((key >> (32 * i)) & 0xFFFFFFFF)
        finkeys=list()
        for i in range(24):
            finkeys.append(keys[i%8])
        for i in range(7,-1,-1):
            finkeys.append(keys[i%8])
        print("finkeys",finkeys)
        return finkeys
    elif type=="dec":
        keys = list()
        for i in range(8):
            keys.append((key >> (32 * i)) & 0xFFFFFFFF)
        print("keys",keys)
        finkeys = list()
        for i in range(8):
            finkeys.append(keys[i % 8])
        for i in range(31, 7, -1):
            finkeys.append(keys[i % 8])
        print("fink",finkeys)
        return finkeys

def GOST_28147_89_enc(text, key, mode, op_mode="ECB", ):
    temp = 0
    if len(hex(text)[2:]) % 16 > 0:
        temp = 1
    templist=list()
    for i in range(len(hex(text)) // 16 + temp):
        templist.append((text >> (64 * i)) & 0xFFFFFFFFFFFFFFFF)
    text=templist

    print(text)
    if temp == 1:
        text[len(text) - 1] = text[len(text) - 1] << (64 - len(hex(text[len(text) - 1]) * 4))
    print(text,"text")
    finkeys = gen_key(key,mode)
    final_text=list()
    for block in text:

        A = block >> 32
        B = block & 0xFFFFFFFF
        X=finkeys
        for i in range(32):
            res=func(A,X[i])
            A_temp=B^res
            B_temp=A
            A=A_temp
            B=B_temp
        block=(A<<32)|B
        final_text.append(block)
    crypted_text = join_64bits(final_text)
    return crypted_text



if __name__ == '__main__':
    fileName = "Text.txt"
    key = 0x287fc759c1ad6b59ac8597159602217e9a03381dcd943c4719dcca000fb2b577


    with open(fileName, "r") as read_file:
        lines = read_file.readlines()
    print(lines)
    for line in lines:
        #print(line)
        line=int(utf8ToHex(line), 16)

        crypted_line = str(GOST_28147_89_enc(line, key, "enc"))
        print("crrrrr",crypted_line)
        with open("encr.txt", 'w') as write_file:
            write_file.write(crypted_line + '\n')

    with open("encr.txt", "r") as read_file:
        lines = read_file.readlines()

        with open("decr.txt", 'w') as write_file:
            for line in lines:
                line_to_decrypt = int(line.removesuffix('\n'))
                print("line_to_decrypt", line_to_decrypt)
                decrypted_line = GOST_28147_89_enc(line_to_decrypt, key, "dec", "GUM")
                print("Decrypted_line: ", decrypted_line)
                decrypted_line = intToHex(decrypted_line)

                write_file.write(hexToUtf8(decrypted_line))

                # print("ltd",line_to_decrypt)
                # print(key)
                # decrypted_line=GOST_28147_89_enc(line_to_decrypt, key, "dec")
                # print("decr_l",decrypted_line)
                # concatenated_string = ''.join(map(str, decrypted_line))
                # line_to_decrypt = int(concatenated_string.removesuffix('\n'))
                # resulting_integer = hex(int(concatenated_string))
                #
                # print(hexToUtf8(intToHex(resulting_integer)))
                #
                #
                # decr_hex_line=list()




