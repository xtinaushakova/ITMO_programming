'''
    Реализация шифра Цезаря с произвольным сдвигом
'''

import string
LETTERS = string.ascii_letters

def encrypt_caesar(plaintext : str, step : int) -> str:
    """
    >>> encrypt_caesar("PYTHON", 3)
    'SBWKRQ'
    >>> encrypt_caesar("python", 3)
    'sbwkrq'
    >>> encrypt_caesar("Python3.6", 3)
    'Sbwkrq3.6'
    >>> encrypt_caesar("", 6)
    ''
    """

    ciphertext = [LETTERS[((LETTERS.find(x) + step) % 26) + 26 * x.isupper()] if x.isalpha() else x for x in plaintext]

    return ''.join(ciphertext)


def decrypt_caesar(ciphertext : str, step : int) -> str:
    """
    >>> decrypt_caesar("SBWKRQ", 3)
    'PYTHON'
    >>> decrypt_caesar("sbwkrq", 3)
    'python'
    >>> decrypt_caesar("Sbwkrq3.6", 3)
    'Python3.6'
    >>> decrypt_caesar("", 3)
    ''
    """

    plaintext = [LETTERS[((LETTERS.find(x) - step) % 26) + 26 * x.isupper()] if x.isalpha() else x for x in ciphertext]

    return ''.join(plaintext)
