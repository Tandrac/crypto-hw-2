def tobits(s):
#from https://stackoverflow.com/questions/10237926/convert-string-to-list-of-bits-and-viceversa
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result

def frombits(bits):
#from https://stackoverflow.com/questions/10237926/convert-string-to-list-of-bits-and-viceversa
    chars = []
    for b in range(len(bits) // 8):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)

def initialPerm(pt):
    #initial permutation of bit positions
    switchList = [pt[1], pt[5], pt[2], pt[0], pt[3], pt[7], pt[4], pt[6]]
    return switchList

def tenPerm(key):
    #switching around the list for the permutation
    newList = [key[2], key[4], key[1], key[6], key[3], key[9], key[0], key[8], key[7], key[5]]
    return newList

def leftShift(bit):
    #left shifting py popping the leading bit, and appending a 0
    bit.pop(0)
    bit.append(0)
    
    
def keys(initialKey):
    #perm = tenPerm(initialKey)
    #3 5 2 7 4 10 1 9 8 6
    perm = [initialKey[2], initialKey[4], initialKey[1], initialKey[6], initialKey[3], initialKey[9], initialKey[0], initialKey[8], initialKey[7], initialKey[5]]
    fiveL = [perm[0], perm[1], perm[2], perm[3], perm[4]]
    fiveR = [perm[5], perm[6], perm[7], perm[8], perm[9]]
    
    #leftshifting
    leftShift(fiveR)
    leftShift(fiveL)
    
    #getting K1
    Kone = [fiveR[0], fiveL[2], fiveR[1], fiveL[3], fiveR[2], fiveL[4], fiveR[4], fiveR[3]]

    #leftshift again
    leftShift(fiveR)
    leftShift(fiveL)
    
    #getting K2
    Ktwo = [fiveR[0], fiveL[2], fiveR[1], fiveL[3], fiveR[2], fiveL[4], fiveR[4], fiveR[3]]

    #returning K1 and K2 as a list
    keys = [Kone, Ktwo]
    return keys
    
    
def xor(bit, K):
    #an xor for two binary lists
    l = []
    for x in range(0,len(bit)):
        if(bit[x] != K[x]):
            l.append(1)
        else:
            l.append(0)
    return l
    
def btoI(x):
    #converts 2 bit binary to 0-3 respectivly
    l = x[0]
    r = x[1]
    if(l == 0):
        if(r == 0):
            return 0
        else:
            return 1
    else:
        if(r == 0):
            return 2
        else:
            return 3

    
def lSub(fourBit):
    #make the matrix
    m = [[1,0,3,2],[3,2,1,0],[0,2,1,3],[3,1,3,2]]
    #getting column index
    column = [fourBit[1], fourBit[2]]
    c = btoI(column)
    
    #getting row index
    row = [fourBit[0], fourBit[3]]
    r = btoI(row)
    
    #finding right matrix entry
    s = m[c][r]


    #this part is so bad dont look at it lol, for returning binary list
    
    a = [0, 0]
    b = [0, 1]
    c = [1, 0]
    d = [1, 1]


    if(s == 0):
        return a
    elif(s == 1):
        return b
    elif(s == 2):
        return c
    else:
        return d
    
def rSub(fourBit):
    #make the matrix
    m = [[0,1,2,3],[2,0,1,3],[3,0,1,0],[2,1,0,3]]
    #getting column index
    column = [fourBit[1], fourBit[2]]
    c = btoI(column)    
    
    #getting row index
    row = [fourBit[0], fourBit[3]]
    r = btoI(row)
    
    s = m[c][r]

    #this part is so bad dont look at it lol, for returning binary list
    
    a = [0, 0]
    b = [0, 1]
    c = [1, 0]
    d = [1, 1]


    if(s == 0):
        return a
    elif(s == 1):
        return b
    elif(s == 2):
        return c
    else:
        return d

    
    
def Ffunct(fb, K):
    #4 bit expamsion
    eightBit = [fb[3], fb[0], fb[1], fb[2], fb[1], fb[2], fb[3], fb[0]]

    #time to xor k and 8bit
    plus = xor(eightBit, K)
    #split the 8bit to left and right
    bitL = [plus[0], plus[1], plus[2], plus[3]]
    bitR = [plus[4], plus[5], plus[6], plus[7]]

    #do s substitutuion    
    L = lSub(bitL)
    R = rSub(bitR)
    
    #final permutation
    fPerm = [L[1], R[1], R[0], L[0]]
    
    return fPerm
    

def crypto(word, initialKey):
    #initial permutation
    ip = initialPerm(word)
    #split the bits into left and right halfs
    bitL = [ip[0], ip[1], ip[2], ip[3]]
    bitR = [ip[4], ip[5], ip[6], ip[7]]
    #get k0 and k1
    K = keys(initialKey)
    
    #F function for right 4 bits and k0
    fOut = Ffunct(bitR, K[0])
    
    #xor for left 4 bits and first f function, also right part of final perm
    newR = xor(bitL, fOut)
    
    #F function for xor and k1
    secondF = Ffunct(newR, K[1])
    
    #xor with second F function and right 4 bits, also left part of final perm
    finalXor = xor(bitR, secondF)
    
    #combine the 2 xors, and apply permutation
    inversePerm = [finalXor[3], finalXor[0], finalXor[2], newR[0], newR[2], finalXor[1], newR[3], newR[1]]
    return inversePerm    
    
def decrypto(word, initialKey):
    #this entire thing is the same as crypto, but with the k0 and k1 positions flipped
    
    
    
    #initial permutation
    ip = initialPerm(word)
    #split the bits into left and right halfs
    bitL = [ip[0], ip[1], ip[2], ip[3]]
    bitR = [ip[4], ip[5], ip[6], ip[7]]
    #get k0 and k1
    K = keys(initialKey)
    
    #F function for right 4 bits and k0
    fOut = Ffunct(bitR, K[1])
    
    #xor for left 4 bits and first f function, also right part of final perm
    newR = xor(bitL, fOut)
    
    #F function for xor and k1
    secondF = Ffunct(newR, K[0])
    
    #xor with second F function and right 4 bits, also left part of final perm
    finalXor = xor(bitR, secondF)
    
    #combine the 2 xors, and apply permutation
    inversePerm = [finalXor[3], finalXor[0], finalXor[2], newR[0], newR[2], finalXor[1], newR[3], newR[1]]
    return inversePerm     
    
def main():
    initialKey = [1, 1, 0, 0, 1, 0, 1, 1, 1, 0]
    words = input("Enter string to be encrypted: ")
    text = tobits(words)
        
    #encrpyted list
    c = []
    #decrpyted list
    d = []
    for i in range(0,len(text),8):
       l = crypto(text[i:i+8], initialKey)
       c.append(l)
    
    #showing encrpyted
    print("Encrypted as: ", end='')
    for x in range(len(c)):
        print(frombits(c[x]), end=' ')
    print('')
    
    #showing decrpyted
    for j in range(0,len(c)):
       t = decrypto(c[j], initialKey)
       d.append(frombits(t))
    empty = ""
    print("Decrypted as: ", empty.join(d))

    
    
if __name__== "__main__":
    main()