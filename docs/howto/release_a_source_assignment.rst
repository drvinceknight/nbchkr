release an assignment
=====================

You can release an assignment in 1 or 2 ways:

1. Using the command line tool.
2. Using :code:`nbchkr` as a library.

Using the command line tool
---------------------------

Given a source assignment :code:`main.ipynb`::

    $ nbchkr release --source main.ipynb --output assignment.ipynb

This creates :code:`assignment.ipynb` with relevant cells removed  which can
then be distributed to students.

Using :code:`nbchkr` as a library
---------------------------------

All of :code:`nbchkr`'s functionality is exposed to the user as a library.

Importing the relevant libraries::

    >>> import pathlib
    >>> import nbchkr.utils

Reading in the source notebook :code:`main.ipynb` and removing relevant cells::

    >>> nb_path = pathlib.Path("main.ipynb")
    >>> nb_node = nbchkr.utils.read(nb_path=nb_path)
    >>> student_nb = nbchkr.utils.remove_cells(nb_node=nb_node)

Writing the assignment notebooks :code:`assignment.ipynb`::

    >>> output_path = pathlib.Path("assignment.ipynb")
    >>> nbchkr.utils.write(output_path=output_path, nb_node=nb_node)

Note that the :code:`nbchkr.utils.remove_cells` function can take as arguments
different regex patterns and replacement strings which allows flexibility for
how to write your notebooks.

Writing a slightly different regex for solution delimiters::

    >>> import re
    >>> solution_regex = re.compile(r"### SOLUTION START[\s\S](.*?)[\s\S]### SOLUTION END", re.DOTALL)

Writing a different replacement text, this is what the student will see instead
of the solution::

    >>> solution_repl = "# Write your solution here"

Removing the cells::

    >>> student_nb = nbchkr.utils.remove_cells(nb_node=nb_node, solution_regex=solution_regex, solution_repl=solution_repl)
