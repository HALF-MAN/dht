# encoding: utf-8
import json
import queue
from threading import Thread
from concurrent.futures import ThreadPoolExecutor

import gc

from . import TCPUtils, blacklist
import time
from random import randint
from hashlib import sha1
from bencode import bencode, bdecode
import math
import traceback
#下载info_metadata信息的工作线程
#从任务队列里获取任务，再交给工作线程处理
SECOND = 1
MINUTE = 60 * SECOND

BT_PROTOCOL = "BitTorrent protocol"
BT_MSG_ID = 20
EXT_HANDSHAKE_ID = 0
class TaskScheduler(Thread):
    def __init__(self, limit, numThread=4):
        Thread.__init__(self)
        self.queue = queue()
        self.setDaemon(True)
        self.limit = limit
        self.executor = ThreadPoolExecutor(numThread)
        self.blackList = blacklist.BlackList(5*MINUTE, 50000)
    def put_task(self, taskInfo):
        #如果任务队列超出队列限制大小，默认丢弃该任务
        if queue.qsize() >= self.limit:
            return
        self.queue.put(taskInfo)
    def run(self):
        while True:
            if self.queue.qsize() == 0:
                continue
            self.executor.submit(self.__download_metadata, (self.queue.get()))
    def __download_metadata(self, taskInfo, timeout=15):
        try:
            if self.blackList.has(taskInfo.address):
                return
            conn = TCPUtils.get_connection(taskInfo.address)
            self.__handshake(conn, taskInfo)
            resp = conn.recv()
            if not self.__onHandshake(resp, taskInfo.infoHash):
                try:
                    conn.close()
                except:
                    return
            self.__ext_handshake(conn, taskInfo)
            resp = conn.recv()
            ut_metadata, metadata_size = get_ut_metadata(resp), get_metadata_size(resp)
            # request each piece of metadata
            metadata = []
            for piece in range(int(math.ceil(metadata_size / (16.0 * 1024)))):
                self.__request_metadata(conn, ut_metadata, piece)
                packet = self.__recv_all(conn, timeout)  # the_socket.recv(1024*17) #
                metadata.append(packet[packet.index("ee") + 2:])
            metadata = "".join(metadata)
            info = parse_metadata(metadata)
            print(info, "\r\n\r\n")
        except:
            traceback.print_exc()
        finally:
            conn.close()

    def __handshake(self, conn, taskInfo):
        infohash = taskInfo.infoHash
        peer_id = random_id()
        msg = preheader() + infohash + peer_id
        conn.send_msg(msg)

    def __on_handshake(self, packet, targetInfoHash):
        bt_header, packet = packet[:20], packet[20:]
        if bt_header != preheader():
            return False
        if packet[24] != 0x10:
            return False
        packet = packet[8:]
        infohash = packet[:20]
        if infohash != targetInfoHash:
            return False
        return True

    def __ext_handshake(self, conn):
        msg = chr(BT_MSG_ID) + chr(EXT_HANDSHAKE_ID) + bencode({"m": {"ut_metadata": 1}})
        conn.send_msg(msg)

    def __request_metadata(conn, ut_metadata, piece):
        msg = chr(BT_MSG_ID) + ut_metadata + bencode({"msg_type": 0, "piece": piece})
        conn.send_msg(msg)
    def __recv_all(self, conn, timeout=15):
        conn.setblocking(0)
        total_data = []
        begin = time.time()
        while True:
            time.sleep(0.05)
            if total_data and time.time() - begin > timeout:
                break
            elif time.time() - begin > 2 * timeout:
                break
            try:
                data = conn.recv(1024)
                if data:
                    total_data.append(data)
                    begin = time.time()
            except:
                pass
        return "".join(total_data)


class TaskInfo:
    def __init__(self, address, infoHash, timeout=15):
        self.address = address
        self.infoHash = infoHash
        self.timeOut = timeout
def random_id():
    h = sha1()
    h.update(entropy(20))
    return h.digest()
def entropy(length):
    return "".join(chr(randint(0, 255)) for _ in range(length))
def preheader():
    bt_header = chr(len(BT_PROTOCOL)) + BT_PROTOCOL
    ext_bytes = "\x00\x00\x00\x00\x00\x10\x00\x00"
    return bt_header + ext_bytes
def get_ut_metadata(packet):
    pass
def get_metadata_size(packet):
    pass
def parse_metadata(metadata, taskInfo):
    info = {}
    info['hash_id'] = taskInfo.infoHash.encode("hex").upper()
    meta_data = bdecode(metadata)
    del metadata
    if meta_data['name']:
        info['name'] = meta_data['name'].strip()
    else:
        info['name'] = ''
    if meta_data['length']:
        info['length'] = meta_data['length']
    else:
        info['length'] = 0
    if meta_data['files']:
        info['files'] = meta_data['files']
        for file in info['files']:
            if file['length']:
                info['length'] += file['length']
        info['files'] = json.dumps(info['files'], ensure_ascii=False)
        info['files'] = info['files'].replace("\"path\"", "\"p\"").replace("\"length\"", "\"l\"")
    else:
        info['files'] = ''
    info['a_ip'] = taskInfo.address[0]
    info['hash_size'] = str(info['hash_size'])
    gc.collect()
    return info