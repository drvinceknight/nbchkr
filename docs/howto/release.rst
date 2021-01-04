release
-------

The release process:

1. Adjust the version number in :code:`version.py`.
2. Tag a new release::

    git tag <release number>

3. Push the new tag to github::

    git push --tags

4. Create a new release on github. 
5. Create a distribution::

    python setup.py sdist bdist_wheel

6. Use :code:`twine` to upload to pypi::

    python -m twine upload dist/*
