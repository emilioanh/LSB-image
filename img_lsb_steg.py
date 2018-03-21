import binascii

def hex2rgb(hexparam):
    return tuple(bytearray.fromhex(hexparam[1:]))
def rgb2hex(red, green, blue):
    return f'#{int(red):02x}{int(green):02x}{int(blue):02x}'
def str2bin(mess):
    binary = bin(int(binascii.hexlify(mess.encode()), 16))
    return binary[2:]
def bin2str(binary):
    mess = binascii.unhexlify('%x'%(int('0b'+binary, 2)))
    return mess.decode()

# red = input('Please input red: ')
# green = input('Please input green: ')
# blue = input('Please input blue: ')

# result = rgb2hex(red, green, blue)
# print(result)
# vax = hex2rgb(result)
# print(vax)
string = input('fuck you:')
val1 = str2bin(string)
print(val1)
print(bin2str(val1))