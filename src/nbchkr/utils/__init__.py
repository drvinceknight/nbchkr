import json
import re
import copy

TAGS_REGEX_PATTERNS_TO_IGNORE = ["hide", r"score:\d"]
SOLUTION_REGEX = re.compile(r"### BEGIN SOLUTION[\s\S](.*?)[\s\S]### END SOLUTION", re.DOTALL)


def read(nb_path):
    contents = nb_path.read_text()
    nb = json.loads(contents)
    return nb


def remove_cells(nb_json, tags_regex_patterns_to_ignore=None, solution_regex=None):
    if tags_regex_patterns_to_ignore is None:
        tags_regex_patterns_to_ignore = TAGS_REGEX_PATTERNS_TO_IGNORE
    if solution_regex is None:
        solution_regex = SOLUTION_REGEX
    cells = []
    for cell in nb_json["cells"]:
        if "tags" not in cell["metadata"] or all(
            not bool(re.match(pattern=pattern, string=tag))
            for tag in cell["metadata"]["tags"] 
            for pattern in tags_regex_patterns_to_ignore
        ):
            try:
                source = "".join(cell["source"])
                new_source = re.sub(pattern=solution_regex, repl="", string=source)
                cell["source"] = new_source.split("\n")


                if bool(re.match(pattern=solution_regex, string=source)) is True:
                    try:
                        cell["outputs"] = []
                    except KeyError:
                        pass
            except KeyError:
                pass
            cells.append(copy.deepcopy(cell))
    nb_out = copy.deepcopy(nb_json)
    nb_out["cells"] = cells
    return nb_out
