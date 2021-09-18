# -*- coding: utf-8 -*-

from sceptre.resolvers import Resolver
import os
import subprocess


def build_expression(args, profile):
    '''
    Build the command that will get executed. The expression always contains
    an AWS profile. By default, the profile that the command is executed with
    is the one that is used to run sceptre. The user can override that profile
    by setting an alternate profile in the `profile` parameter.
    :param args: input arguments
    :param profile: the AWS profile to execute with
    :return: the expression to execute
    '''
    if not args:
        raise ValueError("Missing the command to execute")

    if not profile:
        profile = os.environ.get("AWS_PROFILE")

    expression = args
    if isinstance(expression, dict):
        try:
            expression = args['command']
            if not expression:
                raise ValueError("Missing the command to execute")
        except KeyError:
            raise KeyError("Missing the command to execute")

        if 'profile' in args:
            # override default profile
            profile = args['profile']

    expression = f"AWS_PROFILE={profile} {expression}"

    return expression


class SceptreResolverCmd(Resolver):

    def __init__(self, *args, **kwargs):
        super(SceptreResolverCmd, self).__init__(*args, **kwargs)

    def resolve(self):
        '''
        Executes a command in an environment shell.
        :return: the resulting output from the executed command
        '''
        expression = build_expression(self.argument, self.stack.profile)
        shell = os.environ.get('SHELL', '/bin/bash')
        output = subprocess.check_output([shell, '-c', expression])
        if isinstance(output, bytes):
            output = output.decode(os.environ.get('SHELL_ENCODING', 'utf-8'))
        return output
