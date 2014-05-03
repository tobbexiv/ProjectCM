from django.shortcuts import render, render_to_response, RequestContext

# Create your views here.

def home(request):
	
	return render_to_response("adressbook.html", locals(), context_instance=RequestContext(request))
