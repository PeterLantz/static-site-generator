from text_node import TextNode, TextType


def main():
    print("hello world")
    node = TextNode(
        "Here is my weebsite", TextType.LINK, "https://peterlantz3d.wordpress.com/"
    )
    print(node)


if __name__ == "__main__":
    main()
