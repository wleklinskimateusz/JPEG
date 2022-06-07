## Teory:

#### According to the JPEG spec (ISO/IEC 10918-6:2013 (E), section 6.1):

- Images encoded with only one component are assumed to be grayscale data in which 0 is black and 255 is white.
- Images encoded with three components are assumed to be RGB data encoded as YCbCr unless the image contains an
APP14 marker segment 
- Images encoded with four components are assumed to be CMYK, with (0,0,0,0) indicating white unless the image 
contains an APP14 marker segment 

Most JPEG algorithm implementations use luminance and chrominance (YUV encoding) instead of RGB because human eye is pretty bad at seeing high-frequency brightness changes over a small area.

Y - brightness of the color \
U - determine the color, amount of blue \
V - determine the color, amount of red 

#### JPEG encoding:
- converts an image into chunks of 8x8 blocks of pixels called MCU
- changes the range of values of the pixels so that they center on 0
- applies Discrete Cosine Transformation to each block
- uses quantization to compress the resulting block (and lose high frequency  data)
- zig-zag process, to encode low frequency info first and put zeros to the end
- Run-length, Delta and Huffman encoding

#### DCT:
take an 8x8 image block and tell us how to reproduce it using an 8x8 matrix of cosine functions. That tells us how much each cosine function (out of 64 total functions) contributes to the 8x8 input matrix.

#### Quantization process:
Divide the DCT coefficient matrix element-wise with the quantization matrix, round the result to an integer, and get the quantized matrix. It is important to note that because we apply quantization while decoding, we will have to make sure the colors fall in the [0,255] range. If they fall outside this range, we will have to manually clamp them to this range.

#### Delta encoding:
Delta encoding is a technique used to represent a byte relative to the byte before it.
 [10 11 12 13 10 9] -> [10 1  2  3  0 -1]

#### Run-length encoding
Run-length encoding is a technique used to represent a number of bytes followed by repetitive value. DC (first value) in JPEG is encoded this way.

#### Huffman encoding
 It takes some input data, maps the most frequent characters to the smaller bit patterns and least frequent characters to larger bit patterns, and finally organizes the mapping into a binary tree

#### Data storage:
A JPEG contains up to 4 Huffman tables and these are stored in the “Define Huffman Table” section (starting with 0xffc4). The DCT coefficients are stored in 2 different Huffman tables. One contains only the DC values from the zig-zag tables and the other contains the AC values from the zig-zag tables. The DCT information for the luminance and chrominance channel is stored separately so we have 2 sets of DC and 2 sets of AC information giving us a total of 4 Huffman tables.

In a greyscale image, we would have only 2 Huffman tables (1 for DC and 1 for AC) because we don’t care about the color.

#### JPEG decoding
- Extract the Huffman tables and decode the bits
- Extract DCT coefficients by undoing the run-length and delta encodings
- Use DCT coefficients to combine cosine waves and regenerate pixel values for each 8x8 block
- Convert YCbCr to RGB for each pixel
- Display the resulting RGB image

#### we support only Baseline compression
According to the standard, baseline will contain the series of 8x8 blocks right next to each other.


## Decoding procedure

#### DHT section contents:
- Marker Identifier \
-- 0xff, 0xc4 to identify DHT marker \
-- 2 bytes 
- Length \
-- This specifies the length of Huffman table \
-- 2 bytes
- HT information \
-- bit 0..3: number of HT (0..3, otherwise error) \
-- bit 4: type of HT, 0 = DC table, 1 = AC table \
-- bit 5..7: not used, must be 0 \
-- 1 byte
- Number of Symbols \
-- Number of symbols with codes of length 1..16 \
-- the sum(n) of these bytes is the total number of codes, which must be <= 256 \
-- 16 bytes
- Symbols \
-- Table containing the symbols in order of increasing code length \
-- n = total number of codes \
-- n bytes 



