import json
from workman import conf
from workman.client import Client
from django.http import HttpResponse, HttpRequest

def index(request : HttpRequest):
    timeout = 10 # secs
    post = json.loads(request.body)
    action = post.get('action', 'submit')
    service = post.get('service', 'echo')
    jobid = post.get('job', 'job-1')
    message = post.get('message', 'hello')

    msg = None

    with Client(conf.WorkMan.mgr_url, service) as client:
        if action == 'submit':
            client.request(jobid, message)
            msg = client.reply(timeout)
        elif action == 'status':
            client.status(jobid)
            msg = client.reply(timeout)
        elif action == 'listall':
            client.list_items(service="")
            msg = client.reply(timeout)
        elif action == 'listsvc':
            client.list_items(service.strip())
            msg = client.reply(timeout)
        elif action == 'cancel':
            client.abort(jobid)
        else:
            response = json.dumps({"error": "Invalid action."})
            return HttpResponse(response)

    if msg:
        response = msg.message
    else:
        response = json.dumps({"error": "Failed to fetch response."})
    return HttpResponse(response)
