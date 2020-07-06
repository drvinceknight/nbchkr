import json
import re
import pathlib

from typing import Tuple, Optional
import nbformat

TAGS_REGEX_PATTERNS_TO_IGNORE = ["hide", r"score:\d"]
SOLUTION_REGEX = re.compile(
    r"### BEGIN SOLUTION[\s\S](.*?)[\s\S]### END SOLUTION", re.DOTALL
)
ANSWER_TAG_REGEX = r"answer:*"
SCORE_REGEX = re.compile(r"score:(\d+)")


def read(nb_path: pathlib.Path, as_version: int=4) -> dict:
    """
    Read a jupyter notebook file at `nb_path`.

    Returns the python `dict` representation.
    """
    with open(nb_path, "r") as f:
        nb = nbformat.read(f, as_version=as_version)
    return nb


def remove_cells(
    nb_json, tags_regex_patterns_to_ignore=None, solution_regex=None
):  # TODO Add typing to this function
    """
    Given a dictionary representation of a notebook, removes:

    - Cells with tags matching patterns in `tags_regex_patterns_to_ignore`
    - Text in cells matching the `solution_regex` pattern.

    Returns the python `dict` representation.
    """
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
                cell["source"] = new_source

                if bool(re.match(pattern=solution_regex, string=source)) is True:
                    try:
                        cell["outputs"] = []
                    except KeyError:  # pragma: no cover
                        pass  # TODO Add test coverage for this statement
            except KeyError:  # pragma: no cover
                pass  # TODO Add test coverage for this statement
            cells.append(cell)
    nb_json["cells"] = cells
    return nb_json


def write(output_path: pathlib.Path, nb_json):
    """
    Write the python dict representation of a notebook to `output_path`.
    """
    output_path.write_text(json.dumps(nb_json))


def add_checks(nb_json: dict, source_nb_json: dict, answer_tag_regex=None) -> dict:
    if answer_tag_regex == None:
        answer_tag_regex = ANSWER_TAG_REGEX
    answers = {tag: cell 
               for cell in nb_json["cells"] 
               for tag in cell["metadata"].get("tags", [])
               if bool(re.match(pattern=answer_tag_regex, string=tag))}
    for i, cell in enumerate(source_nb_json["cells"]):
        for tag in cell["metadata"].get("tags", []):
            if tag in answers:
                source_nb_json["cells"][i] = answers[tag]
    return source_nb_json
def get_tags(cell: dict, seperator: str="|") -> Optional[str]:
    try:
        return seperator.join(cell["metadata"]["tags"])
    except KeyError:
        return None


def get_score(cell: dict, score_regex_pattern=None) -> Optional[int]:
    if score_regex_pattern == None:
        score_regex_pattern = SCORE_REGEX
    tags = get_tags(cell)
    if tags is not None:
        search = re.search(pattern=score_regex_pattern, string=tags)
        try:
            return int(search.group(1))
        except AttributeError:
            return None
    return None

