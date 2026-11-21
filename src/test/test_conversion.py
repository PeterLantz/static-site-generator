import unittest

from conversion import *


class TestConversion(unittest.TestCase):
    def test_conversion(self):
        text_nodes = markdown_to_text_nodes("barnicles")
        self.assertEqual(len(text_nodes), 1)
        self.assertEqual(text_nodes[0].text_type, TextType.TEXT)

        text_nodes = markdown_to_text_nodes("one_two_three")
        self.assertEqual(len(text_nodes), 3)
        self.assertEqual(text_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(text_nodes[1].text_type, TextType.ITALIC_TEXT)
        self.assertEqual(text_nodes[2].text_type, TextType.TEXT)

        text_nodes = markdown_to_text_nodes("one**two**_three_four`five`")
        self.assertEqual(len(text_nodes), 5)
        self.assertEqual(text_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(text_nodes[1].text_type, TextType.BOLD_TEXT)
        self.assertEqual(text_nodes[2].text_type, TextType.ITALIC_TEXT)
        self.assertEqual(text_nodes[3].text_type, TextType.TEXT)
        self.assertEqual(text_nodes[4].text_type, TextType.CODE_TEXT)
        self.assertEqual(text_nodes[1].text, "two")

        text_nodes = markdown_to_text_nodes(
            "one**two**![barbara](https://iscomingforyou)_three_four`five`"
        )
        self.assertEqual(text_nodes[2].text_type, TextType.IMAGE)
        self.assertEqual(text_nodes[2].text, "barbara")
        self.assertEqual(text_nodes[2].url, "https://iscomingforyou")
        self.assertEqual(text_nodes[3].text_type, TextType.ITALIC_TEXT)

    def test_extractions(self):
        findings = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertTrue(findings[0])
        self.assertEqual(findings[0][0], "to boot dev")
        self.assertEqual(findings[0][1], "https://www.boot.dev")
        self.assertEqual(findings[1][0], "to youtube")
        self.assertEqual(findings[1][1], "https://www.youtube.com/@bootdotdev")

        findings = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertTrue(findings[0])
        self.assertEqual(findings[0][0], "rick roll")
        self.assertEqual(findings[0][1], "https://i.imgur.com/aKaOqIh.gif")
        self.assertEqual(findings[1][0], "obi wan")
        self.assertEqual(findings[1][1], "https://i.imgur.com/fJRm4Vk.jpeg")

    def test_blocks(self):
        blocks = markdown_to_blocks("\nbollocks\n\n\ndumbdumb\n")
        self.assertEqual(len(blocks), 2)
        self.assertEqual(blocks[0], "bollocks")
        self.assertEqual(blocks[1], "dumbdumb")


if __name__ == "__main__":
    unittest.main()
