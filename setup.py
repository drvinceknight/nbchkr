from setuptools import find_packages, setup

# Read in the version number
# exec(open("src/nashpy/version.py", "r").read())

setup(
    name="nbchkr",
    author="Vince Knight",
    author_email=("knightva@cardiff.ac.uk"),
    packages=find_packages("src"),
    package_dir={"": "src"},
    url="",
    license="The MIT License (MIT)",
    description="A lightweight tool to grade notebook assignements",
)
