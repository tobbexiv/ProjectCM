from django.test import TestCase
from adressbook.models import Adress
from django.contrib.auth.models import User
# Create your tests here.

class AdressTestCase(TestCase):
	def setUp(self):
		#set up test user
		self.test_user_peter = User.objects.create_user('peter', 'peter@test.com', 'testpassword')
		self.test_user_prefect = User.objects.create_user('prefect', 'prefect@test.com', 'testpassword2')

		#create test adressbook entry
		Adress.objects.create(name="Andreas", email="andreas@test.com", contact_owner=self.test_user_peter)
		Adress.objects.create(name="Tobias", email="tobias@test.com", contact_owner=self.test_user_prefect)

	def test_adressbook_entries(self):
		#test peters adressbook
		ab_peter = Adress.objects.get(contact_owner=self.test_user_peter)
		self.assertEqual(ab_peter.name, 'Andreas')
		self.assertEqual(ab_peter.email, 'andreas@test.com')
		self.assertEqual(ab_peter.contact_owner, self.test_user_peter)

		#test prefects adressbook
		ab_prefect = Adress.objects.get(contact_owner=self.test_user_prefect)
		self.assertEqual(ab_prefect.name, 'Tobias')
		self.assertEqual(ab_prefect.email, 'tobias@test.com')
		self.assertEqual(ab_prefect.contact_owner, self.test_user_prefect)