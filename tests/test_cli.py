"""
Tests for the command line tool.
"""
import subprocess

def test_help_call():
    output = subprocess.run(["nbchkr", "--help"], capture_output=True)
    expected_stdout = b'Usage: nbchkr [OPTIONS]\n\nOptions:\n  --help  Show this message and exit.\n'
    assert output.stdout == expected_stdout
    assert output.stderr == b''

def test
