import re
import os
import subprocess
import tempfile
from time import time
from string import Template
from giacgtk.settings import scale


def render_latex(content, fg=[0.981, 0.981, 0.981], template='math'):
    """
        Render latex as svg, return path to svg.
    """
    with tempfile.TemporaryDirectory() as tmpdirname:
        texfile = open(tmpdirname + '/main.tex', 'w+t')
        content = Template(read_template(name=template)).substitute(red=fg[0],
                                                                    green=fg[1],
                                                                    blue=fg[2],
                                                                    body=content)
        texfile.write(content)
        texfile.flush()
        texfile.close()

        subprocess.run('latex -interaction=nonstopmode main.tex',
                       shell=True, cwd=tmpdirname)
        subprocess.run('dvisvgm -n -c {} -b 10 main.dvi'.format(scale), shell=True, cwd=tmpdirname)

        # Move svg to a safer directory
        timestamp = millis()
        filepath = '/tmp/giac-gtk/output-{}.svg'.format(timestamp)
        if not os.path.exists('/tmp/giac-gtk/'):
            os.makedirs('/tmp/giac-gtk/')
        os.rename(tmpdirname + '/main.svg', filepath)
        return filepath


def read_file(path):
    """
        Reads the content of a file
    """
    content = ''
    with open(path) as f:
        content = f.read()
    return content


def millis():
    return int(round(time() * 1000))


def read_template(name='math'):
    """
        Read the template named <name> from the templates directory
    """
    return read_file(os.path.dirname(__file__) + '/templates/' + name + '.tex')


def latex_left_right(latex):
    """
        Return the input with every matching pair of [], \{\}, ()
        as a \left-right pair.

        >>> latex_left_right('(x^2-1)')
        '\\left(x^2-1\\right)'
        >>> latex_left_right('\left(x^2-1\\right)')
        '\\left(x^2-1\\right)'
    """
    return latex


if __name__ == "__main__":
    import doctest
    doctest.testmod()
