from sceptre.resolvers import Resolver
import json
import os
import subprocess


class SceptreResolverCmd(Resolver):

    def __init__(self, *args, **kwargs):
        super(SceptreResolverCmd, self).__init__(*args, **kwargs)

    def resolve(self):
        """
        Attempts to get the 1password secret named by ``param``
        :param param: The shell expression or command to execute.
        :type param: str
        :returns: Shell output.
        :rtype: str
        :raises: Exception
        """

        expression = self.argument
        shell = os.environ.get('SHELL', '/bin/bash')
        output = subprocess.check_output([shell, '-c', expression])
        if isinstance(output, bytes):
            output = output.decode(os.environ.get('SHELL_ENCODING', 'utf-8'))
        return output
