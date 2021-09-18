# -*- coding: utf-8 -*-

import os
import pytest

from resolver.rcmd import build_expression
from unittest import TestCase, mock


class TestBuildExpression(TestCase):

    def test_string_input_default_profile(self):
        expression = build_expression("my-command", "sceptre-profile")
        self.assertEqual("AWS_PROFILE=sceptre-profile my-command", expression)

    def test_string_input_no_args(self):
        with pytest.raises(ValueError):
            build_expression(None, "sceptre-profile")

    def test_string_input_empty_args(self):
        with pytest.raises(ValueError):
            build_expression("", "sceptre-profile")

    def test_dict_input_no_command(self):
        with pytest.raises(ValueError):
            build_expression({}, "sceptre-profile")

    def test_dict_input_missing_command(self):
        with pytest.raises(KeyError):
            arguments = {
                "profile": "my-profile"
            }
            build_expression(arguments, "sceptre-profile")

    def test_dict_input_empty_command(self):
        with pytest.raises(ValueError):
            arguments = {
                "command": ""
            }
            build_expression(arguments, "sceptre-profile")

    def test_dict_input_no_overrides(self):
        arguments = {
            "command": "my-command"
        }
        expression = build_expression(arguments, "sceptre-profile")
        self.assertEqual("AWS_PROFILE=sceptre-profile my-command",
                         expression)

    def test_dict_input_override_profile(self):
        arguments = {
            "command": "my-command",
            "profile": "my-profile"
        }
        expression = build_expression(arguments, "sceptre-profile")
        self.assertEqual("AWS_PROFILE=my-profile my-command",
                         expression)

    @mock.patch.dict(os.environ, {"AWS_PROFILE": "my-profile"})
    def test_profile_from_env_var(self):
        expression = build_expression("my-command", None)
        self.assertEqual("AWS_PROFILE=my-profile my-command",
                         expression)
