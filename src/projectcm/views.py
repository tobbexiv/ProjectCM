from django.shortcuts import render, render_to_response, RequestContext
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def home(request):
	
	return render_to_response("index.html", locals(), context_instance=RequestContext(request))
