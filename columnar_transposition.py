import random
import string


class ColumnarTransposition:
    def __init__(self, keyword):
        assert len(keyword) > 0, "invalid keyword: keyword length must be >= 1."
        self.keyword = keyword.upper()

    def sort_keyword(self):
        ch_map = [(self.keyword[i], i) for i in range(len(self.keyword))]
        return dict([k, v[1]] for k, v in enumerate(sorted(ch_map)))

    def encrypt(self, plaintext):
        length = len(self.keyword)

        ordered_map = self.sort_keyword()

        ret = ""
        for i in range(length):
            ret += plaintext[ordered_map[i]::length]

        return ret

    def decrypt(self, ciphertext):
        length = len(self.keyword)
        ret = ["*"] * len(ciphertext)

        ordered_map = self.sort_keyword()
        min_col_len = len(ciphertext) // length
        # column whose index < cond have an extra character.
        cond = len(ciphertext) % length

        index = 0
        for i in range(length):
            col_len = min_col_len + 1 if ordered_map[i] < cond else min_col_len
            ret[ordered_map[i]::length] = ciphertext[index:index + col_len]
            index += col_len

        return "".join(ret)
