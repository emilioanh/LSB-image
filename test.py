from PIL import Image
import binascii
import optparse

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

def encode(hexcode, digit):
    if hexcode[-1] in ('0', '1', '2', '3', '4', '5'):
        hexcode = hexcode[:-1] + digit
        return hexcode
    else:
        return None

def decode(hexcode):
    if hexcode[-1] in ('0', '1'):
        return hexcode[-1]
    else:
        return None

def hide(filename, message):
    img = Image.open(filename)
    binary = str2bin(message) + '1111111111111110'
    if img.mode in ('RGBA'):
        img = img.convert('RGBA') #chuyển dữ liệu về dạng (R,G,B,A) với giá trị là int
        datas = img.getdata()
        newData = []
        digit = 0
        temp =''
        for item in datas: #lấy từng dòng giá trị RGBA
            if (digit < len(binary)): #chưa hết bin của mess
                newpix = encode(rgb2hex(item[0], item[1], item[2]),binary[digit])
                if newpix == None:
                    newData.append(item)
                else:
                    r, g, b = hex2rgb(newpix)
                    newData.append((r,g,b,255))
                    digit += 1
            else:
                newData.append(item)
        img.putdata(newData)
        img.save(filename, "PNG")
        return "Completed!"
    return "Incorrect Image Mode, can't hide this shit!"