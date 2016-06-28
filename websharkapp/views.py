from django.http import HttpResponse


def index(request):
    return HttpResponse("hello from webshark")

def show_trace(request, trace_id_str):
    return HttpResponse("view trace %d page" % int(trace_id_str))

def new_trace(request):
    return HttpResponse("new trace page")
