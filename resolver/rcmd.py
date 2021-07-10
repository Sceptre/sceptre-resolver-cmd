# -*- coding: utf-8 -*-

from sceptre.resolvers import Resolver
import os
import subprocess


def build_expression(args, profile):
    '''
    Build the command that will get executed.  The input argument is only used
    when args is passed in as a dictionary containing command and profile.
    If the args is passed in as a string the profile is ignored.
    :param args: input arguments
    :param profile: the AWS profile to execute with
    :return: the expression to execute
    '''
    expression = None
    if isinstance(args, dict):

        try:
            expression = args['command']
            if not expression:
                raise ValueError("Missing the command to execute")
        except KeyError:
            raise KeyError("Missing the command to execute")

        if 'profile' in args:
            # override default profile
            expression = f"AWS_PROFILE={args['profile']} {expression}"
        else:
            expression = f"AWS_PROFILE={profile} {expression}"

    else:
        if not args:
            raise ValueError("Missing the command to execute")

        expression = args

    return expression


class SceptreResolverCmd(Resolver):

    def __init__(self, *args, **kwargs):
        super(SceptreResolverCmd, self).__init__(*args, **kwargs)

    def resolve(self):
        '''
        Executes a command in an environment shell
        :return: the resulting output from the executed command
        '''
        expression = build_expression(self.argument, self.stack.profile)
        shell = os.environ.get('SHELL', '/bin/bash')
        output = subprocess.check_output([shell, '-c', expression])
        if isinstance(output, bytes):
            output = output.decode(os.environ.get('SHELL_ENCODING', 'utf-8'))
        return output
