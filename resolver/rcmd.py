from sceptre.resolvers import Resolver
import os
import subprocess


class SceptreResolverCmd(Resolver):

    def __init__(self, *args, **kwargs):
        super(SceptreResolverCmd, self).__init__(*args, **kwargs)

    def resolve(self):
        '''
        Executes a command in an environment shell
        :return: the resulting output from the executed command
        '''

        expression = self.argument
        shell = os.environ.get('SHELL', '/bin/bash')
        output = subprocess.check_output([shell, '-c', expression])
        if isinstance(output, bytes):
            output = output.decode(os.environ.get('SHELL_ENCODING', 'utf-8'))
        return output
