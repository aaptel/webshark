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
        #
        # XXX: would be nice to somehow keep that object in memory as
        # we will probably load it often
        #
        self._cap = pyshark.FileCapture(self._data.path())


    def data_info(self):
        r = {
            'pub_date': str(self._data.pub_date),
            'name': self._data.name,
            'desc': self._data.desc,
            'conf': self._data.conf,
            'length': len(self._cap),
        }
        return r

    def data_list(self, start, end):
        r = {
            'packets': [
                ['10', '0.54566544', '192.168.0.1', '192.168.0.2', 'TCP', '42', 'Foobar baz zab zob zib'],
                ['10', '0.54566544', '192.168.0.1', '192.168.0.2', 'TCP', '42', 'Foobar baz zab zob zib'],
                ['10', '0.54566544', '192.168.0.1', '192.168.0.2', 'TCP', '42', 'Foobar baz zab zob zib'],
                ['10', '0.54566544', '192.168.0.1', '192.168.0.2', 'TCP', '42', 'Foobar baz zab zob zib'],
                ['10', '0.54566544', '192.168.0.1', '192.168.0.2', 'TCP', '42', 'Foobar baz zab zob zib'],
            ]
        }
        return r


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
