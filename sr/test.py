# coding:utf-8

class A(object):
    def __init__(self):
        self.__private()
        self.public()
    def __private(self):
        print('A.__private()')
    def public(self):
        print('A.public()')
class B(A):
    def __init__(self):
        self.__private()
    def __private(self):
        print('B.__private()')
    def public(self):
        print('B.public()')
class C(B):
    def __private(self):
        print('C.__private()')
    def public(self):
        print('C.public()')
c = C()
a = "中"
b = bytes(a, encoding="utf-8")
print(b)