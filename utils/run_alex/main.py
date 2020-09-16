import itertools
import pathlib
import subprocess
import sys


def get_root_path():
    """
    Obtain the path of the root of the directory
    """
    return pathlib.Path(__file__).absolute().parent.parent.parent


root = get_root_path()
max_exit_code = 0


rst_file_paths = root.glob("**/*.rst")
md_file_paths = root.glob("**/*.md")
documentation_file_paths = itertools.chain(rst_file_paths, md_file_paths)

for file_path in documentation_file_paths:
    output = subprocess.run(["alex", file_path], capture_output=True, check=False)

    if (exit_code := output.returncode) > 0:
        max_exit_code = max(max_exit_code, exit_code)
        print(output.stderr.decode("utf-8"))

sys.exit(max_exit_code)
