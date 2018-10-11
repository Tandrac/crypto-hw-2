# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 17:15:00 2018

@author: Tommy
"""

import numpy
import random
import sympy
import hw1
    
x = sympy.Symbol('x')

#from python oauth2
def generate_nonce(length=8):
    """Generate pseudorandom number."""
    return ''.join([str(random.randint(0, 9)) for i in range(length)])

def field(result):
    c = result.all_coeffs()
    for i in range(0,len(c)):
        c[i] = abs(c[i]%2)
    return sympy.Poly.from_list(c, gens = x)
    
def diff_hell():
    modu = sympy.Poly.from_list([1,0,0,0,0,0,0,0,1,1], gens = x)

    privateA = random.randint(1,55)
    privateB = random.randint(1,55)
    
    
    expoA = sympy.Poly.from_list([1]+[0]*privateA, gens = x)
    expoB = sympy.Poly.from_list([1]+[0]*privateB, gens = x)
    
    
    resultA = sympy.div(expoA, modu, domain = 'QQ')[1]
    resultB = sympy.div(expoB, modu, domain = 'QQ')[1]


    resultA = field(resultA)
    resultB = field(resultB)
    
    
   #this is where a and b should send eachother their keys
   
    
    #this part sucked to figure out
    AA = field(sympy.div(field(resultB**privateA), modu, domain = 'QQ')[1])
    BB = field(sympy.div(field(resultA**privateB), modu, domain = 'QQ')[1])
    #print(AA)
#    print(BB)
#    print(privateA)
#    print(privateB)
    key = AA.all_coeffs()
    key = [0]*(10-len(key)) + key
    return key
   
def main():
    
    #generate shared session key, Kab
    Kab = []
    for i in range(0, 10):
        Kab.append(random.randint(0,1))
    
    #print(Kab)    
    #get Kas and Kbs
    sharedAS = diff_hell()
    sharedBS = diff_hell()
    
    #generate ids for connections
    alice = "Alice"
    bob = "Bob"
    
    
    #pretend alice send bob her id
    
    
    #bob sends alice her id, and new nonce
    bobNonce = generate_nonce(8)
    fixes = [alice, bobNonce]
    fixesEncr = hw1.tobits(fixes.__str__())
    #
    fixesEncr = hw1.crypto(fixesEncr, sharedBS)
    
    nOne = generate_nonce(8)
    #send alice id, bob id, nonce1, and bobs encrypted fix to server
    
    
    #server decrypts bobs list and adds the session key Kab
    temp = hw1.decrypto(fixesEncr, sharedBS)
    temp.append(Kab)
    #reencrypt bob
    temp = hw1.tobits(temp.__str__())
    #sned message from server to alice
    toAlice = [nOne, bob, Kab, temp]
    toAliceEncr = hw1.crypto(hw1.tobits(toAlice.__str__()),sharedAS)
    
    #decrypt alice
    aliceMessage = hw1.decrypto(toAliceEncr, sharedAS)
    #may need to use from bit to string method
    
    #alice sends bob the shared key Kab and alice id
    toBob = aliceMessage[3]

    #bob decrpyts and verifies
    bobMessage = hw1.decrypto(toBob, sharedBS)
    #should be alice id, nonce, then Kab

    #bob makes a new nonce, encrypts it, and sends it to alice
    nTwo = generate_nonce(8)
    backAlice = hw1.crypto(hw1.tobits(nTwo.__str__()), bobMessage[2])
    
    #alice decrpyts, then subtracts 1, then re-encrypts and sends it to bob
    aliceFin = hw1.decrypto(backAlice, Kab)
    aliceFin = aliceFin-1
    bobFin = hw1.crypto(hw1.tobits(aliceFin.__str__()),Kab)
    #bob then decrpts and verifies
    bobVerify = hw1.decrypto(bobFin, Kab)
    
    if bobVerify == (nTwo-1):
        return 1
    
    
    
#    temp = [Kab, alice]
#
#    temp1 = hw1.tobits(temp.__str__())
#    #print(temp.__str__())
#    b1 = hw1.crypto(temp1, sharedBS)
        
if __name__ == "__main__":
    main()
    
