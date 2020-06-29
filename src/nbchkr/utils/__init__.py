import json
import re

TAGS_REGEX_PATTERNS_TO_IGNORE = ["hide", r"score:\d"]
SOLUTION_REGEX = r"### BEGIN SOLUTION\n*\n### END SOLUTION"


def read(nb_path):
    contents = nb_path.read_text()
    nb = json.loads(contents)
    return nb


def remove_cells(nb_json, tags_regex_patterns_to_ignore=None):
    if tags_regex_patterns_to_ignore is None:
        tags_regex_patterns_to_ignore = TAGS_REGEX_PATTERNS_TO_IGNORE
    cells = []
    for cell in nb_json["cells"]:
        if "tags" not in cell["metadata"] or all(
            not bool(re.match(pattern=pattern, string=tag))
            for tag in cell["metadata"]["tags"] 
            for pattern in tags_regex_patterns_to_ignore
        ):
            try:
                print(cell["metadata"]["tags"])
            except KeyError:
                pass
            cells.append(cell)
    nb_json["cells"] = cells
    return nb_json
