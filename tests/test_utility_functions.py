"""
Tests for a small utility functions.
"""
import nbchkr


def test_get_tags():
    cell = {"metadata": {"tags": ["tag_1", "tag_2", ""]}}
    assert nbchkr.utils.get_tags(cell=cell) == "tag_1|tag_2"
    assert nbchkr.utils.get_tags(cell=cell, tag_seperator="@") == "tag_1@tag_2"


def test_get_tags_with_given_regex():
    cell = {"metadata": {"tags": ["tag_1", "tag_2", "answer:q1", "answer:q2"]}}
    obtained_tags = nbchkr.utils.get_tags(
        cell=cell, tag_seperator="@", tag_regex=nbchkr.utils.ANSWER_TAG_REGEX
    )
    assert obtained_tags == "answer:q1@answer:q2"
    obtained_tags = nbchkr.utils.get_tags(cell=cell, tag_regex=nbchkr.utils.ANSWER_TAG_REGEX)
    assert obtained_tags == "answer:q1|answer:q2"


def test_get_None_when_there_are_no_tags():
    cell = {"metadata": {"not_tags": ["tag_1", "tag_2"]}}
    assert nbchkr.utils.get_tags(cell=cell) is None
    assert nbchkr.utils.get_tags(cell=cell, tag_seperator="@") is None


def test_get_score():
    cell = {"metadata": {"tags": ["score:40", "mark_23"]}}
    assert nbchkr.utils.get_score(cell=cell) == 40
    assert nbchkr.utils.get_score(cell=cell, score_regex_pattern=r"mark\_(\d)") == 2
    assert nbchkr.utils.get_score(cell=cell, score_regex_pattern=r"mark\_(\d+)") == 23
