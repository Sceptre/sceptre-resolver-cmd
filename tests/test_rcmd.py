# -*- coding: utf-8 -*-

import subprocess
from unittest import TestCase
from unittest.mock import Mock, create_autospec

from parameterized import parameterized
from sceptre.connection_manager import ConnectionManager
from sceptre.exceptions import SceptreException
from sceptre.stack import Stack

from resolver.rcmd import SceptreResolverCmd


class TestSceptreResolverCmd(TestCase):

    def setUp(self):
        self.argument = 'echo "hello!"'
        self.envs = {
            'SHELL': '/my/special/shell'
        }

        self.stack = Mock(
            Stack,
            connection_manager=Mock(ConnectionManager, **{
                'create_session_environment_variables.return_value': self.envs
            })
        )
        self.stack.name = "mock-name"
        self.subprocess_run = create_autospec(subprocess.run)

    @property
    def resolver(self):
        return SceptreResolverCmd(
            argument=self.argument,
            stack=self.stack,
            subprocess_run=self.subprocess_run
        )

    def test_resolve__dict_arg__runs_command_from_dict_arg(self):
        self.argument = {'command': self.argument}

        self.resolver.resolve()

        self.subprocess_run.assert_any_call(
            [self.envs['SHELL'], '-c', self.argument['command']],
            env=self.envs,
            check=True,
            capture_output=True,
        )

    def test_resolve__string_arg__runs_command_from_string(self):
        self.resolver.resolve()

        self.subprocess_run.assert_any_call(
            [self.envs['SHELL'], '-c', self.argument],
            env=self.envs,
            check=True,
            capture_output=True,
        )

    def test_resolve__dict_arg__no_connection_params__uses_stack_default(self):
        self.argument = {'command': self.argument}

        self.resolver.resolve()
        expected_profile = expected_region = expected_role = self.stack.connection_manager.STACK_DEFAULT
        self.stack.connection_manager.create_session_environment_variables.assert_any_call(
            expected_profile, expected_region, expected_role
        )

    def test_resolve__dict_arg__takes_connection_params_from_dict(self):
        self.argument = {
            'command': self.argument,
            'profile': 'my_profile',
            'region': 'my_region',
            'sceptre_role': 'my_role'
        }

        self.resolver.resolve()
        self.stack.connection_manager.create_session_environment_variables.assert_any_call(
            self.argument['profile'], self.argument['region'], self.argument['sceptre_role']
        )

    def test_resolve__returns_output(self):
        result = self.resolver.resolve()

        self.assertEqual(self.subprocess_run.return_value.stdout, result)

    def test_resolve__output_is_bytes__decodes_using_shell_encoding(self):
        expected = 'hello!'
        self.envs['SHELL_ENCODING'] = encoding = 'utf-32'
        self.subprocess_run.return_value.stdout = expected.encode(encoding)
        result = self.resolver.resolve()

        self.assertEqual(expected, result)

    def test_resolve__output_is_bytes_but_shell_encoding_not_set__deocodes_via_utf8(self):
        expected = 'hello!'
        self.subprocess_run.return_value.stdout = expected.encode('utf-8')
        result = self.resolver.resolve()

        self.assertEqual(expected, result)

    @parameterized.expand([
        ('no arg', None),
        ('dict arg with no command', {}),
        ('dict arg with empty command', {'command': ''}),
        ('string arg with empty command', '')
    ])
    def test_resolve__invalid_command_argument__raises_sceptre_exception(self, name, arg):
        self.argument = arg

        with self.assertRaises(SceptreException):
            self.resolver.resolve()
