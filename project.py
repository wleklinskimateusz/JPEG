from struct import unpack


marker_mapping = {
    0xffd8: "Start of Image",
    0xffe0: "Application Default Header",
    0xffdb: "Quantization Table",
    0xffc0: "Start of Frame",
    0xffc4: "Define Huffman Table",
    0xffda: "Start of Scan",
    0xffd9: "End of Image"
}

class HuffmanTable:
    def __init__(self):
        self.root=[]
        self.elements = []
    
    def BitsFromLengths(self, root, element, pos):
        if isinstance(root,list):
            if pos==0:
                if len(root)<2:
                    root.append(element)
                    return True                
                return False
            for i in [0,1]:
                if len(root) == i:
                    root.append([])
                if self.BitsFromLengths(root[i], element, pos-1) == True:
                    return True
        return False
    
    def GetHuffmanBits(self,  lengths, elements):
        '''
        Takes in the lengths and elements, iterates over all
        the elements and puts them in a root list. This list 
        contains nested lists and represents a binary tree.
        '''                  
        self.elements = elements
        ii = 0
        for i in range(len(lengths)):
            for j in range(lengths[i]):
                self.BitsFromLengths(self.root, elements[ii], i)
                ii+=1

    def Find(self,st):
        r = self.root
        while isinstance(r, list):
            r=r[st.GetBit()]
        return  r 

    def GetCode(self, st):
        '''
        method that traverses the tree for us and
        gives us back the decoded bits using the
        Huffman table. This method expects a 
        bitstream as an input.
        '''
        while(True):
            res = self.Find(st)
            if res == 0:
                return 0
            elif ( res != -1):
                return res

class JPEG:
    def __init__(self, image_file):
        with open(image_file, 'rb') as f:               # opens image as binary file to read
            self.img_data = f.read()
    
    def decodeHuffman(self, data):
        '''
        Data format:
        [0] - information of the HT, header
        [1:17] - information of the sum(n) bytes withe same amount of len(code number)
        [17:n+17] - symbols in order of increasing code length

        '''
        offset = 0
        header, = unpack("B",data[offset:offset+1])
        offset += 1

        
        lengths = unpack("BBBBBBBBBBBBBBBB", data[offset:offset+16])     # Extract the 16 bytes containing length data
        offset += 16

        elements = []                                                    # Extract the elements after the initial 16 bytes
        for i in lengths:
            elements += (unpack("B"*i, data[offset:offset+i]))
            offset += i 

        print("Header: ",header)
        print("lengths: ", lengths)
        print("Elements: ", len(elements))

        hf = HuffmanTable()                                             # generate custom HT
        hf.GetHuffmanBits(lengths, elements)
        data = data[offset:]                                            # pass leftover data

    def decode(self):
        data = self.img_data
        while(True):
            marker, = unpack(">H", data[0:2])                           # >H set set unpack function to big-endian data type (najbardziej znaczący bit z przodu) of unsigned short data type
            print(marker_mapping.get(marker))                           
            if marker == 0xffd8:                                        # start marker, process
                data = data[2:]                         
            elif marker == 0xffd9:                                      # end marker, process and if there is no more data break from the loop
                return                                  
            elif marker == 0xffda:                                      # scan marker, process with image data
                data = data[-2:]
            else:
                len_chunk, = unpack(">H", data[2:4])
                len_chunk += 2
                chunk = data[4:len_chunk]

                if marker == 0xffc4:
                    self.decodeHuffman(chunk)
                data = data[len_chunk:]            
            if len(data)==0:
                break       

class Stream:
    '''
    class that will allow us to convert a 
    string into bits and read the bits one by one.
    '''
    def __init__(self, data):
        self.data= data
        self.pos = 0

    def GetBit(self):
        b = self.data[self.pos >> 3]
        s = 7-(self.pos & 0x7)
        self.pos+=1
        return (b >> s) & 1

    def GetBitN(self, l):
        val = 0
        for i in range(l):
            val = val*2 + self.GetBit()
        return val
  

if __name__ == "__main__":
    img = JPEG('photos/profile.jpg')
    img.decode()  

