import unittest

from conversion import text_node_to_html_node
from text_node import TextNode, TextType


class TextTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node1, node2)

    def test_noteq1(self):
        node1 = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.IMAGE)
        self.assertNotEqual(node1, node2)

    def test_noteq2(self):
        node1 = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode(
            "This is a text node",
            TextType.BOLD_TEXT,
            "https://peterlantz3d.wordpress.com/",
        )
        self.assertNotEqual(node1, node2)

    def test_boldText(self):
        text_node = TextNode("This is bold text", TextType.BOLD_TEXT)
        node = text_node_to_html_node(text_node)
        text = "<b>This is bold text</b>"
        self.assertEqual(node.tag, "b")
        self.assertEqual(node.to_html(), text)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


if __name__ == "__main__":
    unittest.main()
