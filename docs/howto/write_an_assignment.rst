write a source assignment
=========================

Writing an assignment is done by writing a Jupyter notebook and using tags:

Write a question
----------------

Use :code:`markdown` cells in Jupyter to write your question.

Write an answer
---------------

In a :code:`code` cell write the code snippet that is the answer to the
question::

    ### BEGIN SOLUTION
    <code>
    ### END SOLUTION

The :code:`### BEGIN SOLUTION` and :code:`### END SOLUTION` delimiters are
necessary. It is possible to pass your own set of delimiters to :code:`nbchkr`
(see further documentation for that).

Add the :code:`answer:<uique_label>` tag to the cell.

Write a check
-------------

In a :code:`code` cell write :code:`assert` statements to check specific
elements of the answer::

    assert <condition>, <error message>

If the :code:`<condition>` is not meet the :code:`<error message>` will be
written to the feedback on a submission.

Note that it is possible to refer to the output of a previous cell using
:code:`_`.

Add the :code:`score:<integer>` tag to the cell. The :code:`<integer>` is the
value associated with this specific check. If the :code:`<condition>` is met
then the :code:`<integer>` value will be added to the total score of a student.

Optionally, you can also add the :code:`description:<string>` tag to the cell.
This will add the :code:`<string>` to the feedback for that specific check. Note
that spaces should be replaced with :code:`-` which will automatically be
replaced in the feedback. For example: :code:`description:correct-answer` will
appear as :code:`### Correct answer` in the feedback.

Note that it is possible to write multiple checks for a given answer. This can
be done so as to programmatically offer varying levels of feedback for specific
parts of the task.
