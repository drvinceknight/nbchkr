""""
Tests to check quality assurance of notebooks.
"""

import nbchkr.utils
from test_release import NB_PATH


def test_check_tags_when_they_match():
    nb_node = nbchkr.utils.read(nb_path=NB_PATH / "submission.ipynb")
    source_nb_node = nbchkr.utils.read(nb_path=NB_PATH / "test.ipynb")
    nb_node = nbchkr.utils.add_checks(nb_node=nb_node, source_nb_node=source_nb_node)
    assert (
        nbchkr.utils.check_tags_match(source_nb_node=source_nb_node, nb_node=nb_node)
        is True
    )


def test_check_tags_when_only_the_answer_tags_match():
    nb_node = nbchkr.utils.read(nb_path=NB_PATH / "submission.ipynb")
    source_nb_node = nbchkr.utils.read(nb_path=NB_PATH / "test.ipynb")
    assert (
        nbchkr.utils.check_tags_match(source_nb_node=source_nb_node, nb_node=nb_node)
        is True
    )


def test_check_tags_when_they_do_not_match_for_specific_case():
    nb_node = nbchkr.utils.read(nb_path=NB_PATH / "submission_with_missing_tags.ipynb")
    source_nb_node = nbchkr.utils.read(nb_path=NB_PATH / "test.ipynb")
    assert (
        nbchkr.utils.check_tags_match(source_nb_node=source_nb_node, nb_node=nb_node)
        is False
    )
