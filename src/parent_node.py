from html_node import HTMLNode


class ParentNode(HTMLNode):
    def __init__(
        self, tag: str, children: list["HTMLNode"], props: dict[str, str] | None = None
    ) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.children is None:
            raise ValueError()
        children_html = ""
        for i in self.children:
            children_html += i.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
