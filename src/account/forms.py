from registration.backends.default.views import RegistrationView
from registration.forms import RegistrationForm

class RegistrationView(RegistrationView):
	form_class = RegistrationForm