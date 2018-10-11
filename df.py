# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 17:15:00 2018

@author: Tommy
"""

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
   #BB = field(sympy.div(field(resultA**privateB), modu, domain = 'QQ')[1])
  
    key = AA.all_coeffs()
    key = [0]*(10-len(key)) + key
    return key
   
def main():
    
    #generate shared session key, Kab
    Kab = []
    for i in range(0, 10):
        Kab.append(random.randint(0,1))
    
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

    bobFix = hw1.encrypt(fixes.__str__(), sharedBS)
    #print(bobFix)    
    
    #alice generates nonce for the server
    nOne = generate_nonce(8)

    # alice sends alice id, bob id, nonce1, and bobs encrypted fix to server
    alToSer = [alice, bob, nOne, bobFix]    
    
    #server decrypts bobs list and adds the session key Kab
    tDec = hw1.decrypt(bobFix, sharedBS)
    
    tDec.append(Kab)

    #reencrypt bobs part
    newBob = hw1.encrypt(tDec.__str__(), sharedBS)
    
    #then re-encrypt alices part and send it to her
    servToAlice = hw1.encrypt([nOne, bob, Kab, newBob].__str__(), sharedAS)
    
    
    #decrypt alice
    aFromS = hw1.decrypt(servToAlice, sharedAS)
    
    #may need to use from bit to string method
    #alice sends bob the shared key Kab and alice id
    toBob = aFromS[3]


    #bob decrpyts and verifies
    bobMessage = hw1.decrypt(toBob, sharedBS)
    #should be alice id, nonce, then Kab

    #bob makes a new nonce, encrypts it, and sends it to alice
    nTwo = generate_nonce(8)
    backAlice = hw1.encrypt(nTwo.__str__(), bobMessage[2])
    
    #alice decrpyts, then subtracts 1, then re-encrypts and sends it to bob
    aliceFin = hw1.decrypt(backAlice, Kab)
    aliceFin = aliceFin-1
    
    bobFin = hw1.encrypt(aliceFin.__str__(),Kab)
    #bob then decrpts and verifies
    bobVerify = hw1.decrypt(bobFin, Kab)
    
    if bobVerify == (int(nTwo)-1):
        print("Job Done!")
        return 1
    
if __name__ == "__main__":
    main()
    
