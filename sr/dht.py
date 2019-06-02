# encoding: utf-8
from . import meta
from threading import Thread, Timer
from collections import deque
import socket
from bencode import bencode, bdecode
import traceback
from time import sleep
from socket import inet_ntoa
from struct import pack, unpack

RE_JOIN_DHT_INTERVAL = 3
TID_LENGTH = 2
BOOTSTRAP_NODES = (
    ("router.bittorrent.com", 6881),
    ("dht.transmissionbt.com", 6881),
    ("router.utorrent.com", 6881)
)
class Node:
    def __init__(self, nid, ip, port):
        self.nid = nid
        self.ip = ip
        self.port = port
class DHT(Thread):
    def __init__(self, task_scheduler, bind_ip, bind_port, max_queue_qsize):
        Thread.__init__(self)
        self.setDaemon(True)
        self.task_scheduler = task_scheduler
        self.bind_ip = bind_ip
        self.bind_port = bind_port
        self.nodes = deque(maxlen=max_queue_qsize)
        self.udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.udp_server.bind((bind_ip, bind_port))

        self.process_request_actions = {
            "get_peers": self.on_get_peers_request,
            "announce_peer": self.on_announce_peer_request,
        }
        timer(RE_JOIN_DHT_INTERVAL, self.re_join_DHT)

    def send_krpc(self, msg, address):
        try:
            self.udp_server.sendto(bencode(msg), address)
        except:
            traceback.print_exc()
    def send_find_node(self, address, nid=None):
        nid = self.get_neighbor(nid, self.nid) if nid else self.nid
        tid = meta.entropy(TID_LENGTH)
        self.send_krpc(make_query(tid, "find_node", {
            "id": nid,
            "target": meta.random_id()
        }), address)

    def get_neighbor(self, target, local, end=10):
        return target[:end] + local[end:]
    def join_dht(self):
        for address in BOOTSTRAP_NODES:
            self.send_find_node(address)
    def re_join_dht(self):
        if len(self.nodes):
            self.join_dht()
        timer(RE_JOIN_DHT_INTERVAL, self.re_join_dht)
    def auto_send_find_node(self):
        wait = 1.0 / self.max_node_qsize
        while True:
            try:
                node = self.nodes.popleft()
                self.send_find_node((node.ip, node.port), node.nid)
            except:
                traceback.print_exc()
        sleep(wait)
    def process_find_node_response(self, msg):
        nodes = decode_node(msg["r"]["nodes"])
        for node in nodes:
            (nid, ip, port) = node
            if len(nid) != 20: continue
            if ip == self.bind_ip: continue
            self.nodes.append(Node(nid, ip, port))


def timer(t, f):
    Timer(t, f).start()
def make_query(tid, q, a):
    return {
        "t": tid,
        "y": "q",
        "q": q,
        "a": a,
    }
def make_reply(tid, r):
    return {
        "t": tid,
        "y": 'r',
        "r": r
    }
def decode_node(nodes):
    n = []
    length = len(nodes)
    if length % 26 != 0:
        return n
    for i in range(0, length, 26):
        nid = nodes[i:i+20]
        ip = inet_ntoa(nodes[i+20:i+24])
        port = unpack("!H", nodes[i + 24:i + 26])[0]
        n.append((nid, ip, port))
    return n