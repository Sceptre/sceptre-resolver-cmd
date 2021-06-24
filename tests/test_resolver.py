import sys
import os

base_dir_path = os.path.dirname(os.path.dirname(__file__))
module_path = os.path.join(base_dir_path, 'resolver')
print(module_path)
sys.path.append(module_path)

from rcmd import SceptreResolverCmd


class TestStackActions(object):
    def setup_method(self, test_method):
        pass

    def test_simple_echo_call(self):
        rcmd_instance = SceptreResolverCmd("echo \"Hello!\"")
        assert rcmd_instance
        print('test that the test is executing')
        output = rcmd_instance.resolve()
        print(output)
        assert output == "Hello!\n"
