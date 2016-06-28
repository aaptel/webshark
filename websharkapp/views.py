from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    ctx = {'var': 42}
    return render(request, 'websharkapp/index.html', ctx)

def show_trace(request, trace_id_str):
    ctx = {'var': 42}
    return render(request, 'websharkapp/trace.html', ctx)

def new_trace(request):
    return HttpResponse("new trace page")
