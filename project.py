from struct import unpack

'''
Teory:

According to the JPEG spec (ISO/IEC 10918-6:2013 (E), section 6.1):

Images encoded with only one component are assumed to be grayscale data in which 0 is black and 255 is white.

Images encoded with three components are assumed to be RGB data encoded as YCbCr unless the image contains an
APP14 marker segment as specified in 6.5.3, in which case the color encoding is considered either RGB or YCbCr
according to the application data of the APP14 marker segment. The relationship between RGB and YCbCr is 
defined as specified in Rec. ITU-T T.871 | ISO/IEC 10918-5.

Images encoded with four components are assumed to be CMYK, with (0,0,0,0) indicating white unless the image 
contains an APP14 marker segment as specified in 6.5.3, in which case the color encoding is considered either 
CMYK or YCCK according to the application data of the APP14 marker segment. The relationship between CMYK and 
YCCK is defined as specified in clause 7.

Most JPEG algorithm implementations use luminance and chrominance (YUV encoding) instead of RGB 
because human eye is pretty bad at seeing high-frequency brightness changes over a small area

Y - brightness of the color
U - determine the color, amount of blue
V - determine the color, amount of red






'''



marker_mapping = {
    0xffd8: "Start of Image",
    0xffe0: "Application Default Header",
    0xffdb: "Quantization Table",
    0xffc0: "Start of Frame",
    0xffc4: "Define Huffman Table",
    0xffda: "Start of Scan",
    0xffd9: "End of Image"
}


class JPEG:
    def __init__(self, image_file):
        with open(image_file, 'rb') as f:               # opens image as binary file to read
            self.img_data = f.read()
    
    def decode(self):
        data = self.img_data
        while(True):
            marker, = unpack(">H", data[0:2])           # >H set set unpack function to big-endian data type (najbardziej znaczący bit z przodu) of unsigned short data type
            print(marker_mapping.get(marker))           # 
            if marker == 0xffd8:                        # start marker, process
                data = data[2:]                         #
            elif marker == 0xffd9:                      # end marker, process and if there is no more data break from the loop
                return                                  #
            elif marker == 0xffda:                      # scan marker, process with image data
                data = data[-2:]
            else:
                lenchunk, = unpack(">H", data[2:4])
                data = data[2+lenchunk:]            
            if len(data)==0:
                break        

if __name__ == "__main__":
    img = JPEG('profile.jpg')
    img.decode()  

