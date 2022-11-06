from columnar_transposition import ColumnarTransposition
from polybius import PolybiusSquare

class ADFGVX:
    def __init__(self, square, keyword):
        """
        :param square: The keysquare grid in form of string, must be 36 in length.
        :param keyword: Keyword for permutation.
        """
        assert len(square) == len("".join(set(square))), "invalide square: characters in square must be unique."
        assert len(square) == 36, f"invalide square: must have 36 characters, has {len(square)}"
        assert len(keyword) > 0, "invalide keyword: keyword length must >= 1"
        
        self.square = square
        self.keyword = keyword

    def encrypt(self, plaintext):
        s1 = PolybiusSquare(self.square, size=6, chars="ADFGVX").encrypt(plaintext)
        s2 = ColumnarTransposition(self.keyword).encrypt(s1)

        return s2

    def decrypt(self, ciphertext):
        s1 = ColumnarTransposition(self.keyword).decrypt(ciphertext)
        s2 = PolybiusSquare(self.square, size=6, chars="ADFGVX").decrypt(s1)

        return s2
