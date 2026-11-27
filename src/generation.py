import os
import shutil

from conversion import markdown_to_html


def copy_contents_over(source: str, target: str) -> None:
    items = os.listdir(source)
    for i in items:
        item_path = os.path.join(source, i)
        item_target_path = os.path.join(target, i)

        # copy file over
        if os.path.isfile(item_path):
            if item_path.endswith(".md"):
                item_target_path = item_target_path.rsplit(".", 1)[0] + ".html"
                generate_page(item_path, "template.html", item_target_path)
            else:
                shutil.copy(item_path, item_target_path)

        # create folder in new directory, then copy contents over to it
        else:
            if not os.path.exists(item_target_path):
                os.mkdir(item_target_path)
            copy_contents_over(item_path, item_target_path)


def extract_title(markdown: str) -> str:
    if not markdown.startswith("#"):
        raise Exception("No header found in file.")
    header = markdown.split("\n", 1)[0]
    header = header.strip("#").strip()
    return header


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # collect information
    from_content = ""
    template_content = ""
    with open(from_path) as file:
        from_content = file.read()
    with open(template_path) as file:
        template_content = file.read()

    # convert it to html
    page_html = markdown_to_html(from_content)
    page_title = extract_title(from_content)
    page_html = template_content.replace("{{ Content }}", page_html).replace(
        "{{ Title }}", page_title
    )

    # write to files
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as file:
        file.write(page_html)
