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
# c = C()


# h = b"get_peers"
# print(h)
# print(type(h))
# print(type(h.decode()))
#
# import queue
#
# q = queue.Queue()
# print(q.qsize())
#
# l = (1111, 333)
# print(l)

# from hashlib import sha1
# from random import randint
# def random_id():
#     h = sha1()
#     h.update(entropy(20).encode(encoding="utf-8"))
#     return h.digest()
# def entropy(length):
#     return "".join(chr(randint(0, 255)) for _ in range(length))
# h = entropy(20)
# print(h)
# print(type(h))
# h = sha1()
# h.update(entropy(20).encode(encoding="utf-8"))
# print(h.digest())
# print(type(h.digest()))
#
# bt_header = chr(len("fff")) + "fff"
# ext_bytes = "\x00\x00\x00\x00\x00\x10\x00\x00"
# som = bt_header + ext_bytes
# print(som)
# print(len(som.encode(encoding="utf-8")))

#
from bencode import bencode, bdecode
#
# print(type(bencode("u")))
# l = (chr(21) + chr(34))+bencode("u").decode("utf-8")
# print(l)
# print(l)
# print(type(l))
# print(type(chr(21)))

a = "d1:ad2:id20:\na\x08\x11\x9dH\xe0\xb4\xd73;\xee\xe2m\xb38\xb2'#\x8a9:info_hash20:\x0e\xc8\x14\xd7\x9e\xb6A\x9a\xdc\x96FQ\x03i\xd5\xa5$Z\x0b\xf56:noseedi1ee1:q9:get_peers1:t2:\xe0\xd21:v4:LT\x01\x001:y1:qe"
b= b"d1:ad2:id20:\na\x08\x11\x9dH\xe0\xb4\xd73;\xee\xe2m\xb38\xb2'#\x8a9:info_hash20:\x0e\xc8\x14\xd7\x9e\xb6A\x9a\xdc\x96FQ\x03i\xd5\xa5$Z\x0b\xf56:noseedi1ee1:q9:get_peers1:t2:\xe0\xd21:v4:LT\x01\x001:y1:qe"
# a = bytes(a, encoding="ISO-8859-1")
# print(b)
# b = str(b, encoding="ISO-8859-1")
# b = bytes(b, encoding="ISO-8859-1")
# print(b)
# msg = bdecode(a)
# print(msg)

y = bencode({"m": {"ut_metadata": 1}}).decode("utf-8")
l = bin(27).replace("0b", "")
print(bytes(l, encoding="utf-8"))
print(l.encode("utf-8"))
print(l)