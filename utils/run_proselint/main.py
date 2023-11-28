import itertools
import pathlib
import sys

import proselint


def get_root_path():
    """
    Obtain the path of the root of the directory
    """
    return pathlib.Path(__file__).absolute().parent.parent.parent


known_exceptions = {}
suggestions_to_ignore = {}

root = get_root_path()
rst_file_paths = root.glob("**/*.rst")
md_file_paths = root.glob("**/*.md")
documentation_file_paths = itertools.chain(rst_file_paths, md_file_paths)
exit_code = 0

for markdown_file_path in filter(
    lambda path: ".ipynb-feedback" not in str(path), root.glob("**/*md")
):
    markdown = markdown_file_path.read_text()
    exceptions = known_exceptions.get(markdown_file_path.parent.name, set(()))

    for exception in exceptions:
        markdown = markdown.replace(markdown, exception)

    suggestions = proselint.tools.lint(markdown)
    ignored_suggestions = suggestions_to_ignore.get(
        markdown_file_path.parent.name, set(())
    )
    for suggestion in filter(
        lambda suggestion: suggestion[0] not in ignored_suggestions, suggestions
    ):
        print(f"Proselint suggests the following in {markdown_file_path}")
        print(suggestion)
        exit_code = 1

sys.exit(exit_code)
