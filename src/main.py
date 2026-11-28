import os
import shutil
import sys

from generation import copy_contents_over


def main():
    # figure out paths
    base_path = "/"
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    source_path = "static"
    public_path = "docs"

    # clear out the public folder
    shutil.rmtree(public_path, ignore_errors=True)
    os.mkdir(public_path)

    # make sure source folder exists
    if not os.path.exists(source_path):
        os.mkdir(source_path)

    # copy and convert contents over
    copy_contents_over(source_path, public_path, base_path=base_path)


if __name__ == "__main__":
    main()
