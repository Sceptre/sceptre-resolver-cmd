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
        expression = None
        region = self.stack.region
        profile = self.stack.profile
        if isinstance(args, dict):
            if 'command' in args:
                command = args['command']
            else:
                raise ValueError("Missing the command to execute")
            if 'profile' in args:
                profile = args['profile']
                expression = f"{command} --profile {profile}"
            if 'region' in args:
                region = args['region']
                expression = f"{expression} --region {region}"
        else:
            expression = self.argument

        output = subprocess.check_output([shell, '-c', expression])
        if isinstance(output, bytes):
            output = output.decode(os.environ.get('SHELL_ENCODING', 'utf-8'))
        return output
