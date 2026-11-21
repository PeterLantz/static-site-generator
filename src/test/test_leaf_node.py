import unittest

from leaf_node import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_case1(self):
        node = LeafNode(tag="p", value="bruh")
        text = "<p>bruh</p>"
        self.assertEqual(node.to_html(), text)

    def test_case2(self):
        node = LeafNode(value="bruh")
        text = "bruh"
        self.assertEqual(node.to_html(), text)

    def test_case3(self):
        node = LeafNode(tag="tag", value="bruh", props={"one": "1", "two": "2"})
        text = '<tag one="1" two="2">bruh</tag>'
        self.assertEqual(node.to_html(), text)


if __name__ == "__main__":
    unittest.main()
