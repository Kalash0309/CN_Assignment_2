def caesar_encrypt(text,shift):
    encrypted = ""

    for char in text:
        change = True
        if char.islower():
            ref = ord('a')
            tot = 26
        elif char.isupper():
            ref = ord('A')
            tot = 26
        elif char.isdigit():
            ref = ord('0')
            tot = 10
        else:
            change = False
        
        if(change):
            char_shift = (ord(char) - ref + shift) % tot + ref
            char_new = chr(char_shift)
        else:
            char_new = char

        encrypted += char_new
    
    return encrypted


def caesar_decrypt(cipher_text,shift):
    decrypted = ""

    for char in cipher_text:
        change = True
        if char.islower():
            ref = ord('a')
            tot = 26
        elif char.isupper():
            ref = ord('A')
            tot = 26
        elif char.isdigit():
            ref = ord('0')
            tot = 10
        else:
            change = False
        
        if(change):
            char_shift = (ord(char) - ref - shift) % tot + ref
            char_new = chr(char_shift)
        else:
            char_new = char

        decrypted += char_new
    
    return decrypted

def reverse(text, start, end):
    str = text[start:end]
    return str[::-1]


def transpose_encrypt(text):
    encrypted = ""
    start = 0
    for i in range(len(text)):
        if text[i] == ' ':
            end = i
            encrypted += reverse(text,start,end)
            encrypted += ' '
            start = i+1
        elif i == (len(text)-1):
            end = i+1
            encrypted += reverse(text,start,end)
            start = i

    return encrypted
