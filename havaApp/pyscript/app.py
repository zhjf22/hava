from ..pyscript import comment_service as cs
from havaApp.utils import ssh_connect
import os


class App1():
    def run(self):
        L = []
        l1 = cs.Comment1().run()
        l2 = cs.Comment2().run()
        L = l1 + l2
        print(L)
        return L


class App2():
    def run(self):
        L = []
        l1 = cs.Comment1().run()
        l2 = cs.Comment2().run()
        L = l1 + l2
        print(L)
        return L
