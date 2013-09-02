from django.shortcuts import render
from django.http import HttpResponse
from cms.models import Widget
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    return render(request, 'cms/index.html')

@csrf_exempt
@require_POST
def sync(request):
    return HttpResponse(
        json.dumps(Widget.sync_with_client(json.loads(request.body))),
        content_type='application/json',
    )