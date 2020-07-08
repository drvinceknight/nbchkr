# nbchkr: Notebook checker

A lightweight solution to mark/grade/check notebook assignments.

# How

## Installation:

$ pip install nbchkr

## Preparation:

Write a jupyter notebook `main.ipynb`, using tags to denote specific cells:

- `answer:<label>` A cell where students are expected to write their answers.
- `score:<total>` A cell with assert statements to check an answer. Worth
  `<total>` marks.
- `hide` A cell that should not be shown.

See documentation for further examples and features.

## Release:

Create a student version of the notebook:

$ nbchkr release --source main.ipynb --output student.ipynb

## Check

Given a student notebook notebook: `submitted.ipynb`

$ nbchkr check --source main.ipynb --submitted submitted.ipynb --feedback feedback.md --output data.csv

This writes to screen the score (total and for each question) and creates
`feedback.md` as well as reporting the results to `data.csv`.

Given a directory of student submission `submissions/` it is possible to batch
check all of them:

$ nbchkr check --source main.ipynb --submitted submissions/ --feedback feedback/ --output data.csv

This will check all notebooks in `submissions/` and write feedback files to
`feedback/`.

# Why?

An alternative to this tool is
[nbgrader](https://nbgrader.readthedocs.io/en/stable/) which offers a
comprehensive course management solution and includes features such as:

- An email server to be able to communicate with students;
- The ability to release assignments, feedback and marks directly;
- Add ons to the jupyter notebook interface.

`nbchkr` is meant to be a lightweight alternative.
