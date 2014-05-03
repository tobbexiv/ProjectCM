from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required

from adressbook.models import Adress

class AdressForm(ModelForm):
	class Meta:
		model = Adress
		exclude = ['contact_owner']
		

@login_required
def adress_list(request, template_name='adress_list.html'):
	adresses = Adress.objects.filter(contact_owner=request.user)
	data = {}
	data['object_list'] = adresses

	return render(request, template_name, data)

@login_required
def adress_create(request, template_name='adress_form.html'):
	form = AdressForm(request.POST or None)
	if form.is_valid():
		adress = form.save(commit=False)
		adress.contact_owner = request.user
		adress.save()

		return redirect('adress_list')

	return render(request, template_name, {'form':form})

@login_required
def adress_update(request, pk, template_name='adress_form.html'):
	adress = get_object_or_404(Adress, pk=pk)
	form = AdressForm(request.POST or None, instance=adress)
	if form.is_valid():
		form.save()
		return redirect('adress_list')

	return render(request, template_name, {'form':form})

@login_required
def adress_delete(request, pk, template_name='adress_delete.html'):
	adress = get_object_or_404(Adress, pk=pk)    
	if request.method=='POST':
		adress.delete()
		return redirect('adress_list')

	return render(request, template_name, {'object':adress})

