import json
from django.http import HttpResponse, HttpRequest
from workman.client import Client

def index(request : HttpRequest):
    with Client('tcp://127.0.0.1:5555') as client:
        client.request('test', '12', [request.GET.get('m')])
        msg = client.reply(10)

    if msg:
        response = json.dumps(msg.items())
    else:
        response = "Failed to fetch response."
    return HttpResponse(response)
