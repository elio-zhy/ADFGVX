import re
import string


class PolybiusSquare:
    def __init__(self, square, size, chars=None):
        """
        Polybius Square Cipher.

        :param square: The keysquare grid in form of string, must be `size*size` in length.
        :param size: The size of the keysquare.
        :param chars: The set of characters to use, must be `size` in length
        """
        assert len(square) == len("".join(set(square))), "invalid square: square must contain unique characters."
        assert len(square) == size * size, f"invalid square: square must contain {size * size} characters, has {len(square)}."

        if chars:
            assert len(chars) == len("".join(set(chars))), "invalid chars: chars must contain unique characters."
            assert len(chars) == size, "invalid chars: must have length "
            self.chars = chars.upper()
        else:
            self.chars = string.ascii_uppercase[:size]

        self.square = square.upper()
        self.size = size

    def encrypt_char(self, ch):
        row = self.square.index(ch) // self.size
        col = self.square.index(ch) % self.size

        return self.chars[row] + self.chars[col]

    def encrypt(self, plaintext):
        """
        :param plaintext: The string to encrypt
        :return: The encrypted string
        """
        norm_plaintext = self.normalize_string(plaintext.upper(), filter=f"[^{self.square}]")

        ret = ""
        for ch in norm_plaintext:
            ret += self.encrypt_char(ch)

        return ret


    def decrypt_pair(self, pair):
        row = self.chars.index(pair[0])
        col = self.chars.index(pair[1])

        return self.square[row * self.size + col]

    def decrypt(self, ciphertext):
        norm_ciphertext = self.normalize_string(ciphertext.upper(), filter=f"[^{self.chars}]")
        assert len(norm_ciphertext) % 2 == 0, "invalid ciphertext: must be a multiple of 2."

        ret = ""
        for i in range(0, len(norm_ciphertext), 2):
            ret += self.decrypt_pair(norm_ciphertext[i:i+2])

        return ret

    @staticmethod
    def normalize_string(string, filter):
        return re.sub(filter, "", string)
