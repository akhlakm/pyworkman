import json
from django.http import HttpResponse, HttpRequest
from util import conf
from workman.client import Client

def index(request : HttpRequest):
    with Client(conf.WorkMan.mgr_url, 'echo', 'django') as client:
        client.request(request.GET.get('j', 'job3'), request.GET.get('m'))
        msg = client.reply(10)

    if msg:
        response = msg.message
    else:
        response = "Failed to fetch response."
    return HttpResponse(response)
