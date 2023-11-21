import json
from django.http import HttpResponse, HttpRequest
from util import conf
from workman.client import Client

def index(request : HttpRequest):
    post = json.loads(request.body)
    action = post.get('action', 'submit')
    service = post.get('service', 'echo')
    jobid = post.get('job', 'job1')
    message = post.get('message', 'hello')
    identity = post.get('identity', 'django')

    print(post)

    with Client(conf.WorkMan.mgr_url, service, identity) as client:
        if action == 'submit':
            client.request(jobid, message)
            msg = client.reply(10)
        elif action == 'status':
            client.status(jobid)
            msg = client.reply(10)
        elif action == 'cancel':
            client.abort(jobid)
        else:
            return HttpResponse("action must be one of submit, status, cancel")

    if msg:
        response = msg.message
    else:
        response = "Failed to fetch response."
    return HttpResponse(response)
