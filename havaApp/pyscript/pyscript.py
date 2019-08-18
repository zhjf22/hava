import os

import inspect
import subprocess
from havaApp import script
from havaApp.utils import ssh_connect


class Base_script(object):

    def __init__(self):
        self.file_path = '../script/'

    def get__function_name(self):
        '''获取正在运行函数(或方法)名称'''
        return inspect.stack()[1][3]

    def get_shell_name(self, func_name):
        real_path = os.path.dirname(__file__)
        print(real_path)
        return os.path.join(real_path, self.file_path, func_name + '.sh')

    def script1(self):
        func_name = self.get__function_name()
        return self.get_shell_name(func_name)

    def script2(self):
        func_name = self.get__function_name()
        return self.get_shell_name(func_name)

    def script3(self):
        func_name = self.get__function_name()
        return self.get_shell_name(func_name)
