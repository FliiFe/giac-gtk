import os
import subprocess
from tempfile import TemporaryFile
from string import printable
import re


class GiacInstance():
    def __init__(self, path='default'):
        self.path = path if path != 'default' else self.find_giac()
        self.outfile = TemporaryFile()
        self.instance = subprocess.Popen([self.path, '--texmacs'],
                                         stdin=subprocess.PIPE,
                                         stdout=self.outfile,
                                         stderr=subprocess.DEVNULL,
                                         universal_newlines=True)
        self.seek = 0

    def wait_for_prompt(self):
        """
            Wait until the REPL show the promt (so that giac is ready
            for new input)
        """
        data = b''
        while b'prompt#>' not in data:
            data = self.read_output()
        return data.decode('ascii')

    def read_output(self):
        """
            Read all output, starting from the last
            seek update index
        """
        self.outfile.seek(self.seek)
        return self.outfile.read()

    def update_seek(self):
        """
            Update the seek value, effectively discarding all previous data
        """
        self.seek = self.outfile.seek(0, 2)

    @staticmethod
    def find_giac():
        """
            Lookup for giac binary in PATH

            >>> GiacInstance.find_giac()
            '/usr/bin/giac'
        """
        for d in os.getenv('PATH', default='').split(':'):
            if os.path.exists(d + '/giac'):
                return d + '/giac'
        raise LookupError('Could not find giac binary in PATH.')

    @staticmethod
    def sanitize_command(to_sanitize):
        """
            Make sure there is a newline at end of input.
        """
        command = to_sanitize + '\n'
        return re.sub('^\s+', '', command, flags=re.MULTILINE)

    def exec_command(self, command):
        """
            Execute a command and returns the output given by giac,
            in the form
            <mode>: <content>

            For example
            >>> giac_instance = GiacInstance()
            >>> print(giac_instance.exec_command('factor(x^4-1)'))
            latex:\[ (x-1)\cdot (x+1) (x^{2}+1) \]
            >>> giac_instance.destroy()
        """
        self.wait_for_prompt()
        self.update_seek()
        self.instance.stdin.write(self.sanitize_command(command))
        self.instance.stdin.flush()
        return self.fix_output(self.wait_for_prompt())

    @staticmethod
    def fix_output(output):
        """
            Sometimes the output read in the output file is wrongly formatted.
            This method fixes the formatting and forces the format
            <mode>: <content>

            >>> GiacInstance.fix_output('prompt#> erbatim: (x)->x^2')
            'verbatim: (x)->x^2'
            >>> GiacInstance.fix_output('verbatim: (x)->x^2')
            'verbatim: (x)->x^2'
            >>> GiacInstance.fix_output('verbatim:latex: x^4-1')
            'latex: x^4-1'
            >>> GiacInstance.fix_output('prompt#> atex: x^4-1')
            'latex: x^4-1'
        """
        line = ''.join(
            char for char in output if char in printable and char != '\n')
        if line[0:8] == 'prompt#>':
            if line[9:13] == 'atex':
                prefix = 'l'
            elif line[9:13] == 'erba':
                prefix = 'v'
            else:
                prefix = 'verbatim: '
            line = prefix + line[9:]
        line = line.replace('prompt#>', '')
        line = re.sub('^verbatim:(\s*)(?!verbatim|latex)',
                      'verbatim:verbatim:\\1', line, flags=re.MULTILINE)
        line = re.sub('\s+$', '', line)
        line = re.sub('^\s*verbatim:', '', line)
        return line

    def destroy(self):
        """
            Kill giac instance. This is needed, otherwise the giac
            process keeps running after python closes
        """
        self.instance.kill()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
