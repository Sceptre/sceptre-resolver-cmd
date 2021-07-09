# -*- coding: utf-8 -*-

from sceptre.resolvers import Resolver
import os
import subprocess


def build_expression(args, profile, region):
    '''
    Build the command that will get executed.  The input argument is only used
    when args is passed in as a dictionary containing command, profile, and region.
    If the args is passed in as a string the profile and region is ignored.
    the profile and region is ignored.
    :param args: input arguments
    :param profile: the default AWS profile to execute with
    :param region: the default AWS region to excute with
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

        if 'region' in args:
            # override default region
            expression = f"AWS_DEFAULT_REGION={args['region']} {expression}"
        else:
            expression = f"AWS_DEFAULT_REGION={region} {expression}"

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
        expression = build_expression(self.argument, self.profile, self.region)
        output = subprocess.check_output(['shell', '-c', expression])
        if isinstance(output, bytes):
            output = output.decode(os.environ.get('SHELL_ENCODING', 'utf-8'))
        return output
