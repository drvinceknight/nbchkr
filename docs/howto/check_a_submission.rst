check a submission
==================

You can check a submission in 2 ways:

1. Using the command line tool.
2. Using :code:`nbchkr` as a library.

Using the command line tool
---------------------------

Given a source assignment :code:`main.ipynb` and a submission
:code:`submitted.ipynb` you can check the submission using::

    $ nbchkr check --source main.ipynb --submitted submitted.ipynb --feedback-suffix -feedback.md --output data.csv

This creates :code:`submitted.ipynb-feedback.md` with feedback and outputs
summary scores to :code:`data.csv`.

Note that given a pattern matching a number of notebooks, for example all
notebooks in :code:`submissions/` you can check them all at once using::

    $ nbchkr check --source main.ipynb --submitted "submissions/*.ipynb" --feedback-suffix -feedback.md --output data.csv

Using :code:`nbchkr` as a library
---------------------------------

All of :code:`nbchkr`'s functionality is exposed to the user as a library.

Importing the relevant libraries::

    >>> import pathlib
    >>> import nbchkr.utils

Reading in the source notebook :code:`main.ipynb` and removing relevant cells::

    >>> source_nb_path = pathlib.Path("main.ipynb")
    >>> source_nb_node = nbchkr.utils.read(nb_path=source_nb_path)

Reading in the submitted notebook :code:`submitted.ipynb` and check that the tags
match (if they do not match the checker will still work but the results should
be confirmed manually)::

    >>> submitted_nb_path = pathlib.Path("submitted.ipynb")
    >>> nb_node = nbchkr.utils.read(submitted_nb_path)
    >>> tags_match = nbchkr.utils.check_tags_match(source_nb_node=source_nb_node, nb_node=nb_node)
    >>> tags_match
    True

Now we will add the checks to the submission from :code:`main.ipynb` and run
them::

    >>> nb_node = nbchkr.utils.add_checks(nb_node=nb_node, source_nb_node=source_nb_node)
    >>> score, maximum_score, feedback_md, passed_checks = nbchkr.utils.check(nb_node=nb_node)
    >>> score
    10
    >>> maximum_score
    11
    >>> feedback_md
    '\n---\n\n## answer:q1\n\n### Integer answer\n\n1 / 1\n\n### Correct answer\n...'
    >>> passed_checks
    {'Integer answer': True, 'Correct answer': True, 'Presence of docstring': False}

Note that the :code:`nbrchkr.utils.check_tags_match`,
:code:`nbchkr.utils.add_checks` and :code:`nbchkr.utils.check` functions can
take further arguments that allow for customisation of behaviour.
