'''
    Реализация шифра Вижнера
'''

import string
LETTERS = string.ascii_letters

<<<<<<< HEAD
def encrypt_vigenere(plaintext : str, keyword : str) -> str:
=======
def encrypt_vigenere(plaintext, keyword):
>>>>>>> feature/rsa
    """
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """

    keyword = (keyword * len(plaintext))[:len(plaintext)].lower()
    ciphertext = ""

    for count, plain_letter in enumerate(plaintext):
        step = LETTERS.find(keyword[count])
        ciphertext += LETTERS[((LETTERS.find(plain_letter) + step) % 26) + 26 * plain_letter.isupper()]

    return ciphertext


<<<<<<< HEAD
def decrypt_vigenere(ciphertext : str, keyword : str) -> str:
=======
def decrypt_vigenere(ciphertext, keyword):
>>>>>>> feature/rsa
    """
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    keyword = (keyword * len(ciphertext))[:len(ciphertext)].lower()
    plaintext = ""

    for count, cipher_letter in enumerate(ciphertext):
        step = LETTERS.find(keyword[count])
        plaintext += LETTERS[((LETTERS.find(cipher_letter) - step) % 26) + 26 * cipher_letter.isupper()]

    return plaintext
