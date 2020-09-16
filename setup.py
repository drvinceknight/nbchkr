from setuptools import find_packages, setup

# Read in the version number
# exec(open("src/nashpy/version.py", "r").read())

# Read in the requirements.txt file
with open("requirements.txt") as f:
    requirements = []
    for library in f.read().splitlines():
        requirements.append(library)

# Read in the version number
exec(open("src/nbchkr/version.py", "r").read())

setup(
    name="nbchkr",
    version=__version__,  # NOQA
    author="Vince Knight",
    author_email=("knightva@cardiff.ac.uk"),
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=requirements,
    url="",
    license="The MIT License (MIT)",
    description="A lightweight tool to grade notebook assignements",
    entry_points={"console_scripts": "nbchkr=nbchkr.__main__:app"},
)
