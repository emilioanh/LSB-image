import binascii
import optparse

HEADER_SIZE = 54 # Gia tri header cua file bmp
DELIMITER = "$" # Phan cach giua gia tri so ki tu can giau vao hinh va message

# User Configurations

def bin2str(binary):
    mess = binascii.unhexlify('%x'%(int('0b'+binary, 2)))
    return mess.decode()

class GiautinLSB(object):

    def __init__(self):
        self.bytes_processed = 0
        self.new_image_data = bytearray()
        self.original_image = ''
        self.text_to_hide = ''

    def open_image(self, filename):
        # Mo file de xu ly
        with open(filename, "rb") as f:
            self.original_image = f.read()

    # Doc va ghi lai phan header vao file moi (chi ghi vao phan data)
    def read_header(self):
        for x in range(0, HEADER_SIZE):
            self.new_image_data.append(self.original_image[x])
            self.bytes_processed += 1

    def hide_text_size(self):
        size = len(self.text_to_hide)
        processed_text_size = str(size)
        processed_text_size += DELIMITER # processed_text_size = so luong ky tu + $ (VD: 18$...)
        self.hide(processed_text_size)

    # Giau mess vao trong anh dung LSB
    def hide(self, mess):
        # Duyet tung ky tu trong chuoi can giau
        for i in range(0, len(mess)):

            current_char = mess[i] # Lay ra ky tu thu i
            current_char_binary = '{0:08b}'.format(ord(current_char)) # Doi ky tu thanh binary {0:08b}
            '''
            so 0 dau la index cua bien i trong format(i) vi o day chi co 1 bien => what ever
            sau dau ":" so 0 dau la ky tu muon dien vao de du 8 ky tu
            8 la dinh dang chuoi ra se co 8 ky tu
            b la kieu binary (dung format)  
            '''

            # Giau tung bit cua ky tu vao tung byte cua hinh
            for bit in range(0, len(current_char_binary)):
                new_byte_binary = ''

                # Ghi de vao byte cua hinh tung bit cua ky tu

                # Lay ra gia tri binary cua byte tiep theo cua hinh
                current_image_binary = bin(self.original_image[self.bytes_processed])[2:] #vi co dang 0bxxx nen phai lay tu ky tu thu 3

                # Giu nguyen 7 ky tu dau
                new_byte_binary = current_image_binary[:7]

                # Gan bit cua ky tu can hide vao cuoi
                new_byte_binary += current_char_binary[bit]

                # Chuyen gia tri binary cua byte vua sua doi thanh char
                new_byte = chr(int(new_byte_binary, 2))

                # Chuyen gia tri cua ky tu de gan vao hinh moi
                self.new_image_data.append(ord(new_byte))
                self.bytes_processed += 1 #danh dau da xu ly them 1 byte cua hinh

    def copy_rest(self):
        # copy cac thanh phan con lai cua hinh khong bi sua doi de tao thanh hinh moi hoan chinh
        self.new_image_data += self.original_image[self.bytes_processed:]

    def close_file(self):
        # Ghi ra thanh file moi
        with open("hidden_pic.bmp", "wb") as out:
            out.write(self.new_image_data)

    def run(self, filename, stega_text):
        self.text_to_hide = stega_text
        self.open_image(filename)
        self.read_header()
        self.hide_text_size()
        self.hide(self.text_to_hide)
        self.copy_rest()
        self.close_file()

class GiaimaLSB:

    def __init__(self, filename):
        self.fd = open(filename, 'rb')
        self.number_of_chars_in_text = 0
        self.original_text = ''

    def read_header(self):
        # Doc cho qua header, chi doc k xu ly
        for i in range(0, HEADER_SIZE):
            byte = self.fd.read(1) # 1 la de doc tung byte => cho du header_size

    # Lay ra LSB cua 8 bytes tiep theo va xep lai thanh 1 byte,
    # Tra ve gia tri ASCII cua byte vua tao ra
    def get_char(self):
        new_byte = ''

        # Lay LSB cua 8 bytes
        for bit in range(0, 8):
            byte = self.fd.read(1)
            # lay gia tri int cua byte 'and' voi 00000001 (and voi 1 luon ra chinh gia tri cua no) de ra LSB
            new_byte += str(ord(byte) & 0x01)

        # Doi gia tri binary cua byte vua tao thanh ASCII
        ch = bin2str(new_byte)
        return ch

    # Lay ra chieu dai mess duoc giau,
    # Duoc giau truoc dau $
    def get_text_size(self):
        curr_ch = self.get_char()
        size_in_string = ''

        # lap den khi gap dau $
        while curr_ch != DELIMITER:
            size_in_string += curr_ch
            curr_ch = self.get_char()

        if (size_in_string != ''):
            self.number_of_chars_in_text = int(size_in_string)

    # Doc ky tu giau trong hinh theo so luong ky tu da doc
    def get_hidden_text(self):
        decoded_chars = 0 #ky tu da lay ra tu hinh
        while decoded_chars < self.number_of_chars_in_text:
            self.original_text += self.get_char()
            decoded_chars += 1

    def close_file(self):
        self.fd.close()

    def get_text(self):
        self.read_header()
        self.get_text_size()
        self.get_hidden_text()
        self.close_file()
        return self.original_text

def main():
    parser = optparse.OptionParser('usage %prog ' + '-e/-d <target file>')
    parser.add_option('-e', dest = 'hide', type='string',  help='target pic path to hide text')
    parser.add_option('-d', dest = 'retr', type='string',  help='target pic path to retrieve text')
    (options, args) = parser.parse_args()
    if (options.hide != None):
        TextToHide = input("Enter a message to Hide: ")
        stega_instance = GiautinLSB()
        stega_instance.run(options.hide, TextToHide)
        print("Successfully finished hiding text")
    elif (options.retr != None):
        destag_insta = GiaimaLSB(options.retr)
        text = destag_insta.get_text()
        a = "Successfully decoded, text is: {}".format(text)
        print(a)

if __name__ == '__main__':
	main()
