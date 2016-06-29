import os
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings

from .models import Trace
from .utils import TraceViewer
from . import utils

def index(req):
    ctx = {'var': 42}
    return render(req, 'websharkapp/index.html', ctx)

def show_trace(req, trace_id_str):
    ctx = {'id': int(trace_id_str)}
    return render(req, 'websharkapp/trace.html', ctx)

def data_info(req, trace_id_str):
    tid = int(trace_id_str)
    t = TraceViewer(tid)
    return JsonResponse(t.data_info())

def data_packet_list(req, trace_id_str, start_id_str, end_id_str):
    tid = int(trace_id_str)
    t = TraceViewer(tid)
    return JsonResponse(t.data_packet_list(int(start_id_str, end_id_str)))

def new_trace(req):
    if req.method == 'POST':
        errors = []
        tmppath = None
        finalpath = None

        desc = req.POST.get('desc', '').strip()
        name = req.POST.get('name', '').strip()
        if not name:
            errors.append('empty name')

        upload = req.FILES.get('file', None)
        if not upload:
            errors.append('no trace found')
        else:
            try:
                r = utils.store_to_tmp(upload)
                if not r:
                    errors.append('problem while storing the trace file')
                else:
                    tmppath, chksum = r
                    if utils.trace_exists(chksum):
                        errors.append('trace file already exists in the system')
                    else:
                        if not utils.is_trace_valid(tmppath):
                            errors.append('invalid trace file')
                        else:
                            if not utils.store_to_public(tmppath, chksum):
                                errors.append('problem while copying file in the system')
                            else:
                                finalpath = chksum
            except:
                #DEBUG:raise
                errors.append('system error related to trace file')

        if tmppath and os.path.exists(tmppath):
            os.remove(tmppath)

        if errors:
            ctx = {'name': name, 'desc': desc, 'errors': errors}
            return render(req, 'websharkapp/upload.html', ctx)

        t = Trace()
        t.path = finalpath
        t.name = name
        t.desc = desc
        t.conf = ''
        t.save()

        return redirect('show_trace', t.id)
    else:
        return render(req, 'websharkapp/upload.html', {})

def latest_trace(req):
    last = Trace.objects.all().order_by('-id')[:10]
    ctx = { 'traces': last }
    return render(req, 'websharkapp/latest.html', ctx)
