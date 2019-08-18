from ..pyscript import pyscript


class Comment1():
    def run(self):
        L = []
        bs = pyscript.Base_script()

        L.append(bs.script1())
        L.append(bs.script3())

        return L


class Comment2():
    def run(self):
        L = []
        bs = pyscript.Base_script()

        L.append(bs.script2())
        L.append(bs.script3())

        return L
