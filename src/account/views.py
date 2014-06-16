from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.

class UserForm(ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email']

@login_required
def account_show(request, template_name='account/show.html'):
	userdata = User.objects.get(username=request.user.username)
	userprofile = userdata.profile
	
	return render(request, template_name, {'userdata':userdata, 'userprofile':userprofile})		


@login_required
def account_edit(request, pk, template_name='account/edit_form.html'):
	userdata = get_object_or_404(User, pk=pk)
	form = UserForm(request.POST or None, instance=userdata)
	if form.is_valid():
		form.save()
		return redirect('account.views.account_show')

	return render(request, template_name, {'form':form})		
