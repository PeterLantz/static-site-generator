import re

from block_type import BlockType
from leaf_node import LeafNode
from text_node import TextNode, TextType


def markdown_to_html(markdown: str) -> str:
    raise NotImplementedError()


def markdown_to_text_nodes(markdown: str) -> list[TextNode]:
    text_nodes = [TextNode(text=markdown, text_type=TextType.TEXT)]
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC_TEXT)
    text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD_TEXT)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE_TEXT)
    return text_nodes


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for i in old_nodes:
        # if it is anything but regular 'ol text, go ahead and add it. No more opetations needed
        if i.text_type != TextType.TEXT:
            new_nodes.append(i)
            continue

        active_delimiter = True

        chunks = i.text.split(delimiter)
        for chunk in chunks:
            active_delimiter = not active_delimiter
            if chunk != "":
                type = text_type if active_delimiter else TextType.TEXT
                new_nodes.append(TextNode(text=chunk, text_type=type))

        if active_delimiter:
            raise Exception(f'text did not having a closing "{delimiter}" delimiter')
    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        extraction = extract_markdown_images(node.text)
        work_text = node.text
        for image in extraction:
            chunks = work_text.split(f"![{image[0]}]({image[1]})", 1)
            if chunks[0] != "":
                new_nodes.append(TextNode(chunks[0]))
            new_nodes.append(
                TextNode(text=image[0], url=image[1], text_type=TextType.IMAGE)
            )
            work_text = chunks[1]
        if work_text != "":
            new_nodes.append(TextNode(work_text))

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        extraction = extract_markdown_links(node.text)
        work_text = node.text
        for link in extraction:
            chunks = work_text.split(f"[{link[0]}]({link[1]})", 1)
            if chunks[0] != "":
                new_nodes.append(TextNode(chunks[0]))
            new_nodes.append(
                TextNode(text=link[0], url=link[1], text_type=TextType.LINK)
            )
            work_text = chunks[1]
        if work_text != "":
            new_nodes.append(TextNode(work_text))

    return new_nodes


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(value=text_node.text)
        case TextType.BOLD_TEXT:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC_TEXT:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE_TEXT:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            if text_node.url is None:
                raise Exception("no URL found")
            return LeafNode(
                tag="a", value=text_node.text, props={"href": text_node.url}
            )
        case TextType.IMAGE:
            if text_node.url is None:
                raise Exception("no URL found")
            return LeafNode(
                tag="img", value="", props={"src": text_node.url, "alt": text_node.text}
            )
        case _:
            raise Exception("no valid type found in text node")


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[(.*?)]\((.*?)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"\[(.*?)]\((.*?)\)", text)


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks_working = markdown.split("\n\n")
    blocks_final = []
    for i in blocks_working:
        i = i.strip()
        i = i.strip("\n")
        if i != "":
            blocks_final.append(i)

    return blocks_final


def block_to_block_type(block: str) -> BlockType:

    if re.search(r"^#{1,6} ", block):
        return BlockType.HEADING

    if re.search(r"^```\n.*?\n```$", block):
        return BlockType.CODE

    lines = block.split("\n")

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    if all(line.startswith(f"{index}. ") for index, line in enumerate(lines, start=1)):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
