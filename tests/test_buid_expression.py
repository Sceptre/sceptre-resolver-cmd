# -*- coding: utf-8 -*-

import unittest
import pytest

from resolver.rcmd import build_expression


class TestBuildExpression(unittest.TestCase):

    def test_string_input_default_profile_and_region(self):
        expression = build_expression("my-command", "default-profile", "default-region")
        self.assertEqual("my-command", expression)

    def test_string_input_no_args(self):
        with pytest.raises(ValueError):
            build_expression(None, "default-profile", "default-region")

    def test_string_input_empty_args(self):
        with pytest.raises(ValueError):
            build_expression("", "default-profile", "default-region")

    def test_dict_input_no_command(self):
        with pytest.raises(KeyError):
            build_expression({}, "default-profile", "default-region")

    def test_dict_input_empty_command(self):
        with pytest.raises(ValueError):
            arguments = {
                "command": ""
            }
            build_expression(arguments, "default-profile", "default-region")

    def test_dict_input_no_overrides(self):
        arguments = {
            "command": "my-command"
        }
        expression = build_expression(arguments, "default-profile", "default-region")
        self.assertEqual("AWS_DEFAULT_REGION=default-region AWS_PROFILE=default-profile my-command",
                         expression)

    def test_dict_input_override_profile(self):
        arguments = {
            "command": "my-command",
            "profile": "my-profile"
        }
        expression = build_expression(arguments, "default-profile", "default-region")
        self.assertEqual("AWS_DEFAULT_REGION=default-region AWS_PROFILE=my-profile my-command",
                         expression)

    def test_dict_input_override_region(self):
        arguments = {
            "command": "my-command",
            "region": "my-region"
        }
        expression = build_expression(arguments, "default-profile", "default-region")
        self.assertEqual("AWS_DEFAULT_REGION=my-region AWS_PROFILE=default-profile my-command",
                         expression)

    def test_dict_input_override_profile_and_region(self):
        arguments = {
            "command": "my-command",
            "profile": "my-profile",
            "region": "my-region"
        }
        expression = build_expression(arguments, "default-profile", "default-region")
        self.assertEqual("AWS_DEFAULT_REGION=my-region AWS_PROFILE=my-profile my-command",
                         expression)
