# nbchkr: Notebook checker

A lightweight solution to mark/grade/check notebook assignments.

# How

## Installation:

$ pip install nbchkr

## Preparation:

Write a jupyter notebook `main.ipynb`, using tags to denote specific cells:

- `score:<total>` A cell with assert statements to check an answer. Worth
  `<total>` marks.
- `hide` A cell that should not be shown.

See documentation for further examples and features.

## Release:

Create a student version of the notebook:

$ nbchkr release --source main.ipynb --output student.ipynb

## Check

Given a student notebook notebook: `submitted.ipynb`

$ nbchkr check --source main.ipynb --submitted submitted.ipynb --feedback feedback.md

This writes to screen the score (total and for each question) and creates
`feedback.md`.

# Why?

An alternative to this tool is
[nbgrader](https://nbgrader.readthedocs.io/en/stable/) which offers a
comprehensive course management solution and includes features such as:

- An email server to be able to communicate with students;
- The ability to release assignments, feedback and marks directly;
- Add ons to the jupyter notebook interface.

`nbchkr` is meant to be a lightweight alternative.
