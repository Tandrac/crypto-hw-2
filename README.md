# crypto-hw-2
hw2 for crypto


For Needham-Schroeder:

Alice sends a message to Bob identifying herself.
Then, Bob sends her id, and a unique nonce encrypted with bobs shared key with the server.
Alice then sends her id, bobs id, a new nonce, and bobs encrypted message to the server.
The server then decrpts all of that, and adds the session key (Kab) alices message, and bobs message within that, then re-encrypts that and sends it back to alice.
Alice decrypts her part of the message, then sends bob the part that was encrypted with his key.
Bob then decrypts his section, generates a new nonce and sends it to Alice, using the newly shared and decrypted session key. 
Alice then decrpyts the nonce, subtracts 1 from it, re-encrypts it using the session key, and sends it to Bob
Bob then decrypts alices message, and checks that it was his nonce-1.
