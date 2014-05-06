from django.test import TestCase
from adressbook.models import Adress
from django.contrib.auth.models import User
# Create your tests here.

class AdressTestCase(TestCase):
	def setUp(self):
		#set up test users
		self.test_user_peter = User.objects.create_user('peter', 'peter@test.com', 'testpassword')
		self.test_user_prefect = User.objects.create_user('prefect', 'prefect@test.com', 'testpassword2')

		#create test adressbook entries
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


class AdressbookViewsTestCaseWithoutLogin(TestCase):

	def setUp(self):
		#set up test users
		self.test_user_peter = User.objects.create_user('peter', 'peter@test.com', 'testpassword')
		self.test_user_prefect = User.objects.create_user('prefect', 'prefect@test.com', 'testpassword2')

		#create test adressbook entries
		Adress.objects.create(name="Andreas", email="andreas@test.com", contact_owner=self.test_user_peter)
		Adress.objects.create(name="Tobias", email="tobias@test.com", contact_owner=self.test_user_prefect)


	#test pages without login, should return 302 redirect (to login page)
	def test_index_wo_login(self):
		resp = self.client.get('/adressbook/')
		self.assertRedirects(resp, '/accounts/login/?next=/adressbook/', status_code=302, target_status_code=200, msg_prefix='')	


	def test_new_wo_login(self):
		resp = self.client.get('/adressbook/new')
		self.assertRedirects(resp, '/accounts/login/?next=/adressbook/new', status_code=302, target_status_code=200, msg_prefix='')	   


	def test_edit_wo_login(self):
		resp = self.client.get('/adressbook/edit/1')
		self.assertRedirects(resp, '/accounts/login/?next=/adressbook/edit/1', status_code=302, target_status_code=200, msg_prefix='')


	def test_delete_wo_login(self):
		resp = self.client.get('/adressbook/delete/1')
		self.assertRedirects(resp, '/accounts/login/?next=/adressbook/delete/1', status_code=302, target_status_code=200, msg_prefix='')



class AdressbookViewsTestCaseWithLogin(TestCase):

	def setUp(self):

		password_peter = 'testpassword'
		#set up test users
		self.test_user_peter = User.objects.create_user('peter', 'peter@test.com', password=password_peter)		

		#create test adressbook entries
		Adress.objects.create(name="Andreas", email="andreas@test.com", contact_owner=self.test_user_peter)		

		self.client.login(username="peter", password=password_peter)

	#test pages with login, should return 200
	def test_index_wth_login(self):
		resp = self.client.get('/adressbook/')
		self.assertEqual(resp.status_code, 200)


	def test_new_wth_login(self):
		resp = self.client.get('/adressbook/new')
		self.assertEqual(resp.status_code, 200) 


	def test_edit_wth_login(self):
		resp = self.client.get('/adressbook/edit/1')
		self.assertEqual(resp.status_code, 200)


	def test_delete_wth_login(self):
		resp = self.client.get('/adressbook/delete/1')
		self.assertEqual(resp.status_code, 200)

	def tearDown(self):
		self.client.logout()