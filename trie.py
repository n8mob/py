from unittest import TestCase


class Node:
    def __init__(self, letter=None, is_word=False):
        self.letter = letter
        self.is_word = is_word
        self.children = {}
        self.pass_count = 0

    def __str__(self):
        self_value = self.letter or 'root'
        if self.is_word:
            return f'{self_value} (end of word)'

        if not self.children:
            return f'{self_value} (no children)'

        for child in self.children.values():
            self_value += '->' + str(child)

        return self_value

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return len(self.children)

    def __contains__(self, key):
        return key in self.children

    def __getitem__(self, key):
        if not self.children:
            return None
        return self.children[key]

    def __setitem__(self, key, value):
        self.children[key] = value


class Trie:
    def __init__(self):
        self.root = Node(letter=None, is_word=False)

    def __str__(self):
        return str(self.root)

    def __repr__(self):
        return self.__str__()

    def __contains__(self, word):
        node = self.root
        for letter in word:
            if letter not in node:
                return False
            node = node[letter]
        return node.is_word

    def has_prefix(self, prefix):
        node = self.root
        for letter in prefix:
            if letter not in node:
                return False
            node = node[letter]
        return True

    def insert(self, word):
        if not word:
            return

        node = self.root

        for letter in word:
            if letter not in node:
                node[letter] = Node(letter)
            node = node[letter]
            node.pass_count += 1
        node.is_word = True

    def insert_suffix(self, text: str, start: int):
        node = self.root
        node.pass_count += 1
        for letter in text[start:]:
            if letter not in node:
                node[letter] = Node(letter)
            node = node[letter]
            node.pass_count += 1
        node.is_word = True

    def build_suffix_trie(self, text: str):
        for i in range(len(text)):
            self.insert_suffix(text, i)

    def longest_repeated_substring(self):
        best_length = 0
        best_path: list[str] = []

        # we'll build our own stack so we don't blow out the python call stack
        # this one will hold tuples of (node, iterator over (char, child), path_list)
        stack = []
        for letter, child in self.root.children.items():
            stack.append((child, iter(child.children.items()), [letter]))

        while stack:
            node, child_iter, path = stack[-1]

            if node.pass_count >= 2 and len(path) > best_length:
                best_length = len(path)
                best_path = path[:]

            try:
                letter, child = next(child_iter)
                stack.append((child, iter(child.children.items()), path + [letter]))
            except StopIteration:
                stack.pop()

        return ''.join(best_path)


    def _walk(self, node: Node, path: list[str], out: list[str]):
        if node.is_word:
            out.append(''.join(path))
        for letter, child in node.children.items():
            path.append(letter)
            self._walk(child, path, out)
            path.pop()

    def completions(self, prefix: str) -> list[str]:
        node = self.root
        for letter in prefix:
            if letter not in node:
                return []
            node = node[letter]
        out = []
        self._walk(node, list(prefix), out)
        return out


def printdump(node: Node, prefix=''):
    if node.letter:
        details = f' (count={node.pass_count}'
        if node.is_word:
            details += ', word=True'
        details += ')'

        print(f'{prefix}{node.letter}{details}')

    for child in node.children.values():
        printdump(child, prefix + (node.letter or ''))


class TestNode(TestCase):
    def test_empty_constructor(self):
        node = Node(letter=None)
        self.assertIsNone(node.letter)
        self.assertFalse(node.is_word)
        self.assertFalse(node.children)

    def test_constructor_with_letter(self):
        node = Node(letter='a')
        self.assertEqual('a', node.letter)
        self.assertFalse(node.is_word)
        self.assertFalse(node.children)

    def test_constructor_with_letter_and_is_word(self):
        node = Node(letter='a', is_word=True)
        self.assertEqual('a', node.letter)
        self.assertTrue(node.is_word)
        self.assertFalse(node.children)

    def test_get_item(self):
        node = Node(letter='a')
        node['b'] = Node('b')
        self.assertEqual('b', node['b'].letter)
        self.assertFalse(node['b'].is_word)
        self.assertFalse(node['b'].children)
        self.assertTrue('b' in node)


class TestTrie(TestCase):
    def setUp(self) -> None:
        self.trie = Trie()

    def test_insert(self):
        self.trie.insert('hello')
        self.assertTrue(self.trie.root['h']['e']['l']['l']['o'].is_word)

    def test_another_word(self):
        self.trie.insert('world')
        self.assertTrue(self.trie.root['w']['o']['r']['l']['d'].is_word)

    def test_insert_multiple_words(self):
        self.trie.insert('hello')
        self.trie.insert('world')
        self.assertTrue(2, len(self.trie.root))
        self.assertTrue(self.trie.root['h']['e']['l']['l']['o'].is_word)
        self.assertTrue(self.trie.root['w']['o']['r']['l']['d'].is_word)

    def test_contains(self):
        self.trie.insert("car")
        self.assertTrue("car" in self.trie)
        self.assertFalse("cat" in self.trie)
        self.assertFalse("carr" in self.trie)
        self.assertFalse("ca" in self.trie)

    def test_has_prefix(self):
        self.trie.insert("car")
        self.assertTrue(self.trie.has_prefix("car"))
        self.assertTrue(self.trie.has_prefix("ca"))

    def test_completions(self):
        self.trie.insert("car")
        self.trie.insert("cat")
        self.trie.insert("bugs")

        self.assertEqual(['car', 'cat'], self.trie.completions('c'))
        self.assertEqual(['bugs'], self.trie.completions('bu'))

    def test_pass_count(self):
        self.trie.insert("car")
        self.trie.insert("cat")
        self.trie.insert("cap")

        self.assertEqual(3, self.trie.root['c'].pass_count)
        self.assertEqual(3, self.trie.root['c']['a'].pass_count)
        self.assertEqual(1, self.trie.root['c']['a']['p'].pass_count)
        self.assertEqual(1, self.trie.root['c']['a']['t'].pass_count)
        self.assertEqual(1, self.trie.root['c']['a']['r'].pass_count)


NOT_VERY_LONG = """this is a test of the trie. to test it, I'm going to insert some words. and some phrases that might repeat. and some more phrases. and then I'll insert some words. again."""
if __name__ == '__main__':
    trie = Trie()

    with open('defcon21/net-re/200_decoded.txt') as f:
        trie.build_suffix_trie(f.read())

    print(trie.longest_repeated_substring())
