from . import models
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
import pyshark
import tempfile
import hashlib
import os
from shutil import copyfile

class TraceViewer:
    def __init__(self, tid):
        self._data = models.Trace.objects.get(pk=tid)
        self.tid = tid
        self.pub_date = self._data.pub_date

        print("traceviewer loading...")

        # XXX: would be nice to somehow keep that object in memory as
        # we will probably load it often
        self._packets = list(pyshark.FileCapture(trace_path(self._data.path)))
        # XXX: tshark has 2 xml output format which pyshark uses
        # - pmdl: trace with complete packet info
        # - psdl: simpler trace with just the one-line summary display
        #         in Wireshark packet list
        #
        # We need both and the packet summary is not in the pmdl format :(
        self._summaries = list(pyshark.FileCapture(trace_path(self._data.path), only_summaries=True))
        #self._cap_summaries = pyshark.FileCapture(trace_path(self._data.path), only_summaries=True)

        # XXX: pyshark lazily loads the trace, we have to iterate over
        # it to get the size
        self.size = len(self._packets)

        # This is extremely ineficient, we need something
        # - that gives us both summary and packet info (eventually separately)
        # - doesn't have to load the whole trace to get to a packet
        # - keep them in memory so we dont load again at every requests
        print("traceviewer created")


    def data_info(self):
        r = {
            'pub_date': str(self._data.pub_date),
            'name': self._data.name,
            'desc': self._data.desc,
            'conf': self._data.conf,
            'length': self.size,
        }
        return r

    def data_packet_list(self, start, count):
        r = []
        stop = min(start+count, self.size)
        for i in range(start, stop):
            r.append([
                self._summaries[i].no,
                self._summaries[i].time,
                self._summaries[i].source,
                self._summaries[i].destination,
                self._summaries[i].protocol,
                self._summaries[i].length,
                self._summaries[i].info,
            ])
        return {'packets': r}

def store_to_tmp(upload):
    md5 = hashlib.md5()
    path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False) as f:
            path = f.name
            for c in upload.chunks():
                f.write(c)
                md5.update(c)
    except:
        if path and os.path.exists(path):
            os.remove(path)
        return None

    return path, md5.hexdigest()

def store_to_public(path, chksum):
    final = trace_path(chksum)
    try:
        copyfile(path, final)
    except:
        #DEBUG: raise
        return False
    return True

def trace_path(chksum):
    return os.path.join(settings.TRACE_FILE_DIR, chksum)

def is_trace_valid(path):
    try:
        cap = pyshark.FileCapture(path)

        # XXX: pyshark lazily load the packet so this always returns 0

        # if len(cap) <= 0:
        #     return False

        # try looping over the packets and do something kind of useful
        # that wont be optimized out
        i = 0
        for p in cap:
            if p[0].src != 'xyz':
                i = i+1
    except:
        #DEBUG: raise
        return False
    return True

def trace_exists(chksum):
    return os.path.exists(trace_path(chksum))
