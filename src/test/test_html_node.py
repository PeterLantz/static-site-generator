import unittest

from html_node import HTMLNode


class TestHTLMNode(unittest.TestCase):
    def test_1(self):
        node = HTMLNode(props={"item": "itemequals"})
        self.assertEqual(' item="itemequals"', node.props_to_html())


if __name__ == "__main__":
    unittest.main()
