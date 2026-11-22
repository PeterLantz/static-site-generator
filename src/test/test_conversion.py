import unittest

from conversion import *


class TestConversion(unittest.TestCase):
    def test_full_operation(self):

        html = markdown_to_html("""
```
this is some code
whoops
```
""")
        test_against = "<div><code>this is some code\nwhoops</code></div>"
        self.assertEqual(html, test_against)

        html = markdown_to_html("""
## text**bold**text

# _italic_text

> famous quote
>by famous man


- one
- two

1. one
2. two

```
some code _whoops_
darn no formatting
```
""")
        test_against = "<div>"
        test_against += "<h2>text<b>bold</b>text</h2><h1><i>italic</i>text</h1>"
        test_against += "<blockquote>famous quote\nby famous man</blockquote>"
        test_against += "<ul><li>one</li><li>two</li></ul>"
        test_against += "<ol><li>one</li><li>two</li></ol>"
        test_against += "<code>some code _whoops_\ndarn no formatting</code>"
        test_against += "</div>"
        self.assertEqual(html, test_against)

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
        blocks = split_markdown_into_blocks("\nbollocks\n\n\ndumbdumb\n")
        self.assertEqual(len(blocks), 2)
        self.assertEqual(blocks[0], "bollocks")
        self.assertEqual(blocks[1], "dumbdumb")

        blocks = split_markdown_into_blocks("""
- item one
- item one one
- item one one one

1. moo
2. two

```
here is some code, tis three
```

> tis a qoute, tis the 4th

a random paragraph here, to celebrate the number 5

# heading one, or should I say 6?

###### heading two, maybe 7

- whoops
this is an invalid ordered list
and is really a paragraph
and is item 8
            """)

        self.assertEqual(len(blocks), 8)
        self.assertEqual(
            block_markdown_to_block_type(blocks[0]), BlockType.UNORDERED_LIST
        )
        self.assertEqual(
            block_markdown_to_block_type(blocks[1]), BlockType.ORDERED_LIST
        )
        self.assertEqual(block_markdown_to_block_type(blocks[2]), BlockType.CODE)
        self.assertEqual(block_markdown_to_block_type(blocks[3]), BlockType.QUOTE)
        self.assertEqual(block_markdown_to_block_type(blocks[4]), BlockType.PARAGRAPH)
        self.assertEqual(block_markdown_to_block_type(blocks[5]), BlockType.HEADING)
        self.assertEqual(block_markdown_to_block_type(blocks[6]), BlockType.HEADING)
        self.assertEqual(block_markdown_to_block_type(blocks[7]), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
