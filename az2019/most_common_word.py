import string
from typing import List


class Solution:

    @staticmethod
    def mostCommonWord(paragraph: str, banned: List[str]) -> str:

        words = paragraph.translate(None, string.punctuation).split()

        return words[0]

