import string
letters = string.ascii_letters

def encrypt_caesar(plaintext):
    """
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """

    ciphertext = ''.join([letters[((letters.find(x) + 3) % 26) + 26 * x.isupper()] if x.isalpha() else x for x in plaintext])
    return ciphertext


def decrypt_caesar(ciphertext):
    """
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """

    plaintext = ''.join([letters[((letters.find(x) - 3) % 26) + 26 * x.isupper()] if x.isalpha() else x for x in ciphertext])
    return plaintext