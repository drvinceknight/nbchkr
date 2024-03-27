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

In a :code:`code` cell write statements to check any given property
of a variable.
To do this define a :code:`property_check` function that takes a variable
:code:`variable`. Pass this :code:`property_check` function as well as a
:code:`feedback_string` and the name of a variable to check the property of
:code:`variable_string` to :code:`nbchkr.checks.check_variable_has_expected_property`

Note that it is possible to refer to the output of a previous cell using
:code:`_`.

Here is a check for the previous output being even::

    output = _

    import nbchkr.checks
    variable_string = "output"
    feedback_string = "Your output is not even"

    def check_even(variable):
        return variable % 2 == 0

    nbchkr.checks.check_variable_has_expected_property(
        variable_string=variable_string,
        feedback_string=feedback_string,
        property_check=check_even,
    )

Add the :code:`score:<integer>` tag to the cell. The :code:`<integer>` is the
value associated with this specific check. If the :code:`<condition>` is met
then the :code:`<integer>` value will be added to the total score of a student.

Add the :code:`description:<string>` tag to the cell.
This will add the :code:`<string>` to the feedback for that specific check. Note
that spaces should be replaced with :code:`-` which will automatically be
replaced in the feedback. For example: :code:`description:correct-answer` will
appear as :code:`### Correct answer` in the feedback.

Note that it is possible to write multiple checks for a given answer. This can
be done so as to programmatically offer varying levels of feedback for specific
parts of the task.


Property checks with arguments
''''''''''''''''''''''''''''''

Note that it is also possible to write property check functions that take
keyword arguments and pass these to
:code:`nbchkr.checks.check_variable_has_expected_property`. For example::

    output = _

    import nbchkr.checks
    variable_string = "output"
    feedback_string = "Your output is not even"

    def check_divisibiliy_by_m(variable, m):
        return variable % m == 0

    nbchkr.checks.check_variable_has_expected_property(
        variable_string=variable_string,
        feedback_string=feedback_string,
        property_check=check_divisibiliy_by_m,
        m=2,
    )
