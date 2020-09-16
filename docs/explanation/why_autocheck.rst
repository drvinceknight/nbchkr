why use automated checking?
===========================

In the discussion of [Schinke2014]_ (a review of assessment) the following
sentence stands out:

    "However, underlying the less encouraging news about grades are numerous
    opportunities for faculty members to make assessment and evaluation more
    productive, better aligned with student learning, and less burdensome for
    faculty and students."

It is with idea in mind that automated checking of assessment should be
implemented.

Indeed in [Wilcox2015]_ (a reflection on an implementation of automated
checking) there are two initial questions:

1. Does the automated check detract from student learning?
2. Do the benefits of implementing automated checking outway the cost?

It is hoped that software similar to and like :code:`nbchkr` answer the second
question.

The first question however is positively answered in a number of pieces of work
such as [Wilcox2015]_ itself where students reported a positive experience of
using automated checking but also benefited academically which indicates a
better overall learning process. This student satisfaction with the process is
also reported in [Saikkonen2001]_

Some of the downsides of human checking are listen in [Cheang2003]_:

1. Difficulty of judging efficiency and correctness;
2. The fact that there can be multiple approaches to a problem that would be
   missed by a human checker.
3. Emphasis on aesthetics. Note that given the modern emphasis on the importance
   of code readability I am not convinced by this particular downside.
4. Inconsistency of human checkers
5. Time: the workload of checking works is huge.

This last point is often mentioned in the literature and specifically
[Schinke2014]_ highlight the importance of creating time and space for
meaningful feedback through self and peer evaluation.

Self evaluation as a general pedagogic strategy relates well to automated
checking as described by [Losada2010]_ where they prescribe giving a number of
tests to students as part of the assessment. As part of the [Losada2010]_ a
discussion as part of Bloom's Taxonomy is given however this will not be
discussed here given numerous downsides to the taxonomy (see for example:
[Case2013]_). [Losada2010]_ lists numerous advantages to automated checking:

1. Fast feedback: in their case and similar to [Cheang2003]_, [Saikkonen2001]_
   and others the particular framework being described was an "online" one that
   students could use to gain immediate feedback.
2. Fairer grading;
3. Permanent access;
4. Efficiency;
5. Fostering a positive attitude towards test driven development (TDD).

This last point relates to the testing practice in software engineering of
writing a test before writing the software.

Specific strategies for writing checks are described in [Saikkonen2001]_ and
[Wilcox2016]_ which give insight and guidance on writing using tests that allow
for feedback that helps students identify errors. Contrary to [Cheang2003]_'s
suggestion that aesthetics  having a major role in human checking being a
negative, [Wilcox2016]_ points out that static tools can be used to check the
code quality itself (all within the testing framework). One such example of this
is in the :ref:`tutorial` where a test is included to make sure that the code
written is documented.

There are some negative aspects to automated testing another good
quote from [Schinke2014]_ is:

    "In fact, we have presented evidence that accuracy-based grading may, in
    fact demotivate students and impede learning."

It was noted also in [Wilcox2015]_ that some students do feel that it the
automated checks "unnecessarily strict".
Finally, [Wilcox2016]_ discusses some aspects of security and that automated
testing can be done inside of a virtual machine to avoid running of malicious
code.

These are all aspects to be considered when writing the specific checks for the
assignments and not losing sight of the end goal which is to create a positive
environment for student learning. Automated checking should not be thought of as
a solution to a problem of assessment but hopefully a tool that enables better
learning through:

1. Timely and actionable feedback;
2. The creation of space for productive learning activities.
