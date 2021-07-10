# -*- coding: utf-8 -*-

import unittest
import pytest

from resolver.rcmd import build_expression


class TestBuildExpression(unittest.TestCase):

    def test_string_input_default_profile(self):
        expression = build_expression("my-command", "default-profile")
        self.assertEqual("my-command", expression)

    def test_string_input_no_args(self):
        with pytest.raises(ValueError):
            build_expression(None, "default-profile")

    def test_string_input_empty_args(self):
        with pytest.raises(ValueError):
            build_expression("", "default-profile")

    def test_dict_input_no_command(self):
        with pytest.raises(KeyError):
            build_expression({}, "default-profile")

    def test_dict_input_empty_command(self):
        with pytest.raises(ValueError):
            arguments = {
                "command": ""
            }
            build_expression(arguments, "default-profile")

    def test_dict_input_no_overrides(self):
        arguments = {
            "command": "my-command"
        }
        expression = build_expression(arguments, "default-profile")
        self.assertEqual("AWS_PROFILE=default-profile my-command",
                         expression)

    def test_dict_input_override_profile(self):
        arguments = {
            "command": "my-command",
            "profile": "my-profile"
        }
        expression = build_expression(arguments, "default-profile")
        self.assertEqual("AWS_PROFILE=my-profile my-command",
                         expression)
