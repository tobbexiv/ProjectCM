#from django.shortcuts import render, render_to_response, RequestContext

# Create your views here.

#def home(request):
	
#	return render_to_response("adressbook.html", locals(), context_instance=RequestContext(request))

from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm

from adressbook.models import Adress

class AdressForm(ModelForm):
	class Meta:
		model = Adress

def adress_list(request, template_name='adress_list.html'):
	adresses = Adress.objects.all()
	data = {}
	data['object_list'] = adresses

	return render(request, template_name, data)


def adress_create(request, template_name='adress_form.html'):
    form = AdressForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('adress_list')

    return render(request, template_name, {'form':form})


def adress_update(request, pk, template_name='adress_form.html'):
    adress = get_object_or_404(Adress, pk=pk)
    form = AdressForm(request.POST or None, instance=adress)
    if form.is_valid():
        form.save()
        return redirect('adress_list')

    return render(request, template_name, {'form':form})


def adress_delete(request, pk, template_name='adress_delete.html'):
    adress = get_object_or_404(Adress, pk=pk)    
    if request.method=='POST':
        adress.delete()
        return redirect('adress_list')

    return render(request, template_name, {'object':adress})

