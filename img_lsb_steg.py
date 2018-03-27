HEADER_SIZE = 54 # Gia tri header cua file bmp
DELIMITER = "$" # Phan cach giua gia tri so ki tu can giau vao hinh va message

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

class GiautinLSB(object):

    def __init__(self):
        self.bytes_processed = 0
        self.new_image_data = bytearray()
        self.original_image = ''
        self.text_to_hide = ''

    def open_image(self):
        # Mo file de xu ly
        with open(ImageFile, "rb") as f:
            self.original_image = f.read()

    # Doc va ghi lai phan header vao file moi (chi ghi vao phan data)
    def read_header(self):
        for x in range(0, HEADER_SIZE):
            self.new_image_data.append(self.original_image[x])
            self.bytes_processed += 1

    def hide_text_size(self):
        sz = len(self.text_to_hide)
        processed_text_size = str(sz)
        processed_text_size += DELIMITER # processed_text_size = so luong ky tu + $ (VD: 18$...)
        self.hide(processed_text_size)

    # Giau mess vao trong anh dung LSB
    def hide(self, mess):
        
