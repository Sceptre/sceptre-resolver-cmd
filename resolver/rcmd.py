# -*- coding: utf-8 -*-
import subprocess
from typing import Optional, Union

from sceptre.exceptions import SceptreException
from sceptre.resolvers import Resolver
from sceptre.stack import Stack


class SceptreResolverCmd(Resolver):
    def __init__(
        self,
        argument: Union[str, dict] = None,
        stack: Stack = None,
        *,
        subprocess_run=subprocess.run
    ):
        super(SceptreResolverCmd, self).__init__(argument, stack)
        self._subprocess_run = subprocess_run

    def resolve(self) -> str:
        """
        Executes a command in an environment shell.
        :return: the resulting output from the executed command
        """
        command, environment_variables = self._get_subprocess_envs()
        shell = environment_variables.get('SHELL', '/bin/bash')
        result = self._subprocess_run(
            [shell, '-c', command],
            env=environment_variables,
            check=True,
            capture_output=True
        )
        output = result.stdout

        if isinstance(output, bytes):
            output = output.decode(environment_variables.get('SHELL_ENCODING', 'utf-8'))

        return output

    def _get_subprocess_envs(self):
        profile = region = role = self.stack.connection_manager.STACK_DEFAULT
        if isinstance(self.argument, dict):
            profile = self.argument.get('profile', profile)
            region = self.argument.get('region', region)
            role = self.argument.get('sceptre_role', role)
            command: Optional[str] = self.argument.get('command', '')
        else:
            command: str = self.argument

        if command in ('', None):
            raise SceptreException("A command is required for the !rcmd resolver")

        environment_variables = self.stack.connection_manager.create_session_environment_variables(
            profile, region, role
        )
        return command, environment_variables
