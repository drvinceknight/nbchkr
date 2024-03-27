"""
Test that the version number exists and is valid.
"""

import nbchkr
import packaging


def test_version_is_str():
    assert type(nbchkr.__version__) is str


def test_version_is_valid():
    assert (
        type(packaging.version.parse(nbchkr.__version__)) is packaging.version.Version
    )
