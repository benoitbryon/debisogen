"""Various utilities."""
from contextlib import contextmanager
import fileinput
import re
import shutil
import subprocess
import sys
import tempfile


@contextmanager
def use_temp_dir():
    """Create temporary directory, return it's name, delete it at the
    end of the context execution, even if an exception is raised.

    >>> import os
    >>> try:
    ...     with use_temp_dir() as directory:
    ...         os.path.exists(directory)
    ...         os.path.isdir(directory)
    ...         raise Exception('Dummy Exception')
    ... except:
    ...     pass
    True
    True
    >>> os.path.exists(directory)
    False

    """
    directory = tempfile.mkdtemp()
    try:
        yield directory
    finally:
        shutil.rmtree(directory)


def replace_in_file(search, replacement, filename):
    """Perform a regular expression search/replace on each line of a file.

    Limitation: currently doesn't perform multiline search/replace."""
    for line in fileinput.input(filename, inplace=1):
        line = re.sub(search, replacement, line)
        sys.stdout.write(line)


def execute_command(command, data={}):
    """Execute a shell command.

    Command is a string ; data a dictionnary where values are supposed to be
    strings or integers and not variables or commands.

    Command and data are combined with string format operator.

    >>> execute_command('echo "%(msg)s"', {'msg': 'Hello world!'})

    """
    if data:
        command = command % data
    print "Executing %s" % command
    return subprocess.call(command, shell=True)


def is_url(value):
    """Return True if value is an URL, i.e. if it startswith http:// or
    something similar."""
    return value.startswith('http://') or value.startswith('https://')


def download_file(source, destination):
    """Download file from source to destination."""
    execute_command('curl --location --output %(dest)s %(src)',
                    {'dest': destination, 'src': source})
