
from posixpath import split
import numpy as np

def hex_to_rgb(hex):
    rgb = []
    for i in (0, 2, 4):
        decimal = int(hex[i:i+2], 16)
        rgb.append(decimal)
  
    return tuple(rgb)

def decodeMatrix(n,m):
    data = []
    f = open("matrix_code.txt", "r")
    for x in f:
        data.append(x.split(','))
    f.close()

    data = np.array(data)
    matrix = np.zeros([3,n,m])

    n = int(n/2)
    m = int(m/2)

    hex = data.T[4]
    matrix_hex = np.reshape(hex,(n,m))


    for i in range(0,n-1):
        for j in range(0,m-1):
            k = i*2
            l = j*2
            matrix[0,k,l] = hex_to_rgb(matrix_hex[i,j].lstrip('#'))[0]
            matrix[0,k+1,l] = hex_to_rgb(matrix_hex[i+1,j].lstrip('#'))[0]
            matrix[0,k,l+1] = hex_to_rgb(matrix_hex[i,j+1].lstrip('#'))[0]
            matrix[0,k+1,l+1] = hex_to_rgb(matrix_hex[i+1,j+1].lstrip('#'))[0]
            
            matrix[1,k,l] = hex_to_rgb(matrix_hex[i,j].lstrip('#'))[1]
            matrix[1,k+1,l] = hex_to_rgb(matrix_hex[i+1,j].lstrip('#'))[1]
            matrix[1,k,l+1] = hex_to_rgb(matrix_hex[i,j+1].lstrip('#'))[1]
            matrix[1,k+1,l+1] = hex_to_rgb(matrix_hex[i+1,j+1].lstrip('#'))[1]

            matrix[2,k,l] = hex_to_rgb(matrix_hex[i,j].lstrip('#'))[2]
            matrix[2,k+1,l] = hex_to_rgb(matrix_hex[i+1,j].lstrip('#'))[2]
            matrix[2,k,l+1] = hex_to_rgb(matrix_hex[i,j+1].lstrip('#'))[2]
            matrix[2,k+1,l+1] = hex_to_rgb(matrix_hex[i+1,j+1].lstrip('#'))[2]

    matrix = matrix[:,:-2,:-2]

    return matrix
