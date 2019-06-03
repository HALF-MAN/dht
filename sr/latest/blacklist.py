# encoding: utf-8
import time
import threading


class entry:
    def __init__(self, addr, ctime):
        self.addr = addr
        self.ctime = ctime

class BlackList:
    def __init__(self, expiredAfter, limit):
        self.expiredAfter = expiredAfter
        self.limit = limit
        self.ll = []
        self.lock = threading.Lock()
        self.cache = {}

    def add (self, addr):
        self.lock.acquire()
        self.removeExpiredLocked()
        try:
            if len(self.ll) >= self.limit:
                return
            if addr not in self.cache[addr]:
                e = entry(addr, time.time())
                self.ll.append(e)
                self.cache[addr] = e
        finally:
            self.lock.release()
    def has(self, addr):
        self.lock.acquire()
        try:
            if self.cache[addr]:
                e = self.cache[addr]
                if time.time() - e.ctime < self.expiredAfter:
                    return True
                self.ll.remove(e)
                self.cache.pop(e.addr)
        finally:
            self.lock.release()
        return False
    def removeExpiredLocked(self):
      now = time.time()
      for elem in self.ll:
        if now - elem.ctime < elem.expiredAfter:
            break
        self.ll.remove(elem)
        self.cache.pop(elem.addr)

