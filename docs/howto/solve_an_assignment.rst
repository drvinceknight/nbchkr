solve an assignment
===================

You can solve an assignment in 1 or 2 ways:

1. Using the command line tool.
2. Using :code:`nbchkr` as a library.

Using the command line tool
---------------------------

Given a source assignment :code:`main.ipynb`::

    $ nbchkr solve --source main.ipynb --output solution.ipynb

This creates :code:`solution.ipynb` with relevant cells removed which can
then be distributed to students.

Using :code:`nbchkr` as a library
---------------------------------

All of :code:`nbchkr`'s functionality is exposed to the user as a library.

Importing the relevant libraries::

    >>> import pathlib
    >>> import re
    >>> import nbchkr.utils

Reading in the source notebook :code:`main.ipynb` and removing relevant cells.
We here use a regex that matches nothing for the solutions (as we want them to
stay in place)::

    >>> nb_path = pathlib.Path("main.ipynb")
    >>> solution_regex = re.compile('$^')
    >>> nb_node = nbchkr.utils.read(nb_path=nb_path)
    >>> student_nb = nbchkr.utils.remove_cells(nb_node=nb_node, solution_regex=solution_regex)

Writing the assignment notebooks :code:`assignment.ipynb`::

    >>> output_path = pathlib.Path("solution.ipynb")
    >>> nbchkr.utils.write(output_path=output_path, nb_node=nb_node)
