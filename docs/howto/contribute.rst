contribute
----------

Installing a development version
++++++++++++++++++++++++++++++++

To install a development version of the library::

    $ python setup.py develop

Run tests
+++++++++

To run the basic unit tests::

    $ python -m pytest

To run the full set of tests with syntax highlighting, doctests and coverage::

    $ python -m pytest -v --cov=nbchkr --cov-fail-under=100 --flake8 --doctest-glob='*.rst

To run static type checking::

    $ python -m mypy src/

To run the doctest coverage checker::

    $ python -m interrogate -e setup.py -e tets/ -M -i -v -f 100

Style formatting
++++++++++++++++

To the automatic style formatter :code:`black`::

    $ python -m black .

To run the import sorting formatter :code:`isort`::

    $ python -m isort src/nbchkr/.

Build the documentation
+++++++++++++++++++++++

To build the documentation::

    $ cd docs
    $ make html

Git branching
+++++++++++++

The most up to date branch that all new features should be branched from is
:code:`dev`.

New releases are tagged.
