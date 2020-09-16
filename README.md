[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3999365.svg)](https://doi.org/10.5281/zenodo.3999365)

# nbchkr: Notebook checker

A lightweight solution to mark/grade/check notebook assignments.

# How


## Installation


```bash
$ pip install nbchkr
```

## Preparation

Write a jupyter notebook `main.ipynb`, using tags to denote specific cells:

- `answer:<label>` A cell where students are expected to write their answers.
- `score:<total>` A cell with assert statements to check an answer. Worth
  `<total>` marks.
- `hide` A cell that should not be shown.

See documentation for further examples and features.

## Release

Create a student version of the notebook:

```bash
$ nbchkr release --source main.ipynb --output student.ipynb
```


## Check

Given a student notebook notebook: `submitted.ipynb`

```bash
$ nbchkr check --source main.ipynb --submitted submitted.ipynb --feedback-suffix -feedback.md --output data.csv
```

This writes to screen the score (total and for each question) and creates
`feedback.md` as well as reporting the results to `data.csv`.

Given a pattern of student submissions it is possible to batch
check all of them:

```bash
$ nbchkr check --source main.ipynb --submitted submissions/*.ipynb --feedback-suffix -feedback.md --output data.csv
```

# Why?

An alternative to this tool is
[nbgrader](https://nbgrader.readthedocs.io/en/stable/) which offers a
comprehensive course management solution and includes features such as:

- An email server to be able to communicate with students;
- The ability to release assignments, feedback and marks directly;
- Addons to the jupyter notebook interface.

`nbchkr` is meant to be a lightweight alternative.


# Documentation

Full documentation is available at:
[nbchkr.readthedocs.io](nbchkr.readthedocs.io)
