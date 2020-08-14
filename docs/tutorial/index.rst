Tutorial
========

How to write an assignment
--------------------------

Initial setup
+++++++++++++

Open a Jupyter notebook, we will choose to name it :code:`main.ipynb` (but the
name is not important).

IMAGE

On the Jupyter toolbar, click on :code:`View` and then :code:`Cell Toolbar` and
then :code:`Tags`.

IMAGE

This should make the native tag menu available to you on every cell in your
Jupyter notebook.

IMAGE

We can now start writing our assignment.

Writing text for a question
+++++++++++++++++++++++++++

Let us write a markdown cell with some instructions and a question that we want
to ask our students::

    # Class assignement

    We will use this assignment to solidify our understanding of using Python to
    carry out some numerical operations and also write functions.

    Use this notebook to write your answers in the cells as instructed, do your
    best not to delete any of the cells that are already there.

    ## Question one.

    Use python to obtain the remainder when dividing 21 by 5.

    \\[21 \mod 5\\]

Be sure to indicate that that cell is a :code:`markdown` cell and not the usual
:code:`code` cell.

IMAGE

Once you run that cell it should like like the following:

IMAGE

Writing the answer to a question
++++++++++++++++++++++++++++++++

In the next cell we will write down the expected answer but also include a
delimiters for what should not be shown to students::

    ### BEGIN SOLUTION
    21 % 5
    ### END SOLUTION

We can run that cell if we want to keep an eye on the answer.

An important step at this stage is to let :code:`nbchkr` know that this is an
answer cell, we do this by adding `answer:q1` to tags.

Everything should now look like the following:

IMAGE

Writing checks for the answer
+++++++++++++++++++++++++++++

We will now write a check for the answer, that :code:`nbchkr` uses to be able to give
feedback to a student. We do this using python :code:`assert` statements::

    q1_answer = _
    feedback_text = "Your opteration did not return an integer which is expected"
    assert type(q1_answer) is int

We will also add a tag: :code:`score:1` to this cell.

As well as checking that the answer is an integer let us check the actual answer
by creating a new cell and writing::

    feedback_text = "The expected answer is 1 because 21 = 5 * 3 + 1"
    assert q1_answer == 1, feedback_text

This will be worth 3 points so let us add the tag: :code:`score:3`.

Everything should now look like the following:

IMAGE

Writing another question
++++++++++++++++++++++++

Let us write a second question that asks students to write a function::

    ## Question two.

    Write a python function `get_remainder(m, n)` that returns the remainder
    the remainder when dividing \\(m\\) by \\(n\\).

    \\[m \mod n\\]


Writing the answer
++++++++++++++++++

As before we write an answer in a cell below::

    def get_remainder(m, n):
        ### BEGIN SOLUTION
        """
        This function returns the remainder of m when dividing by n
        """
        return m % n
        ### END SOLUTION

Including checks
++++++++++++++++

We will now add some cells to check the answer.

First let us make sure there is a docstring::

    feedback_text = """You did not include a docstring. This is important to help document your code.


    It is done  using triple quotation marks. For example:

    def get_remainder(m, n):
        \"\"\"
        This function returns the remainder of m when dividing by n
        \"\"\"
        ...

    Using that it's possible to access the docstring,
    one way to do this is to type: `get_remainder?`
    (which only works in Jupyter) or help(get_remainder).

    We can also comment code using `#` but this is completely
    ignored by Python so cannot be accessed in the same way.

    """
    assert  get_remainder.__doc__ is not None, feedback_text

Whilst we've decided to write quite a lot of feedback with details about writing
docstrings we are only going to score this part of the answer 1 point so we use
the tag: `score:1`.

We will also include specific checks for the actual answer::

    assert get_remainder(5, 3) == 2, "Incorrect answer for m=5, n=3: 5 mod 2 = 1 because 5 = 3 * 1 + 2"
    assert get_remainder(34, 21) == 13, "Incorrect answer for m=34, n=21: 34 mod 21 = 13 because 34 = 21 * 1 + 13"
    assert get_remainder(1000, 10) == 0, "Incorrect answer for m=1000, n=10: 1000 mod 10 = 0 because 1000 = 10 * 100 + 0"

IF you would like to see a final version of this notebook you can find it here.

IF you would like to see a final version of this notebook
you can find it here.

TODO Add link to notebookk

How to release an assignment
----------------------------

Now we can take that source notebook and create an assignment that can be given
to students. To do this, we use the command line tool that comes with `nbchkr`::

    $ nbchkr release --source main.ipynb --output assignement.ipynb

This creates a notebook `assignment.ipynb` with the answers and checks removed.

TODO Add link to notebookk

Check student assignments and generate feedback
------------------------------------------------

Assuming we have a class of 3 students who each submitted a notebook with the
following naming convention::

    ssignement_<student_number>.ipynb

These notebooks are all put in the `submissions/` directory.
TODO Add link to download

.. toctree::
   :maxdepth: 2
   :caption: Contents:
