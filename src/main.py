import os
import shutil

from generation import copy_contents_over, generate_page


def main():
    shutil.rmtree("public", ignore_errors=True)
    os.mkdir("public")
    if not os.path.exists("static"):
        os.makedirs("static")
    copy_contents_over("static", "public")


if __name__ == "__main__":
    main()
