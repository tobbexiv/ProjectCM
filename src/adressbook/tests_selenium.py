from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from django.test import LiveServerTestCase
# Create your tests here.

class TestCaseLogin(LiveServerTestCase):

	@classmethod	
	def setUpClass(cls):
		cls._password_peter = '123'		
		cls._driver = webdriver.PhantomJS()


	def test_1_login(self):
		self._driver.get("http://localhost:8000/")
		self._driver.find_element_by_id('id_login').send_keys("peter")
		self._driver.find_element_by_id('id_password').send_keys(self._password_peter)
		self._driver.find_element_by_class_name("primaryAction").click();
		body = self._driver.find_element_by_tag_name('h1')
		self.assertIn('ProjectCM', body.text)


	def test_2_new(self):
		self._driver.get("http://localhost:8000/adressbook/")
		self._driver.find_element_by_id('new').click()
		self._driver.find_element_by_id('id_name').send_keys("test")
		self._driver.find_element_by_id('id_email').send_keys(str('test@email.com'))
		self._driver.find_element_by_id('save').click()
		body = self._driver.find_element_by_tag_name('body')
		self.assertIn('test', body.text)
		self.assertIn('test@email.com', body.text)


	def test_3_logout(self):
		self._driver.get("http://localhost:8000/")
		self._driver.find_element_by_id('logout').click()
		body = self._driver.find_element_by_tag_name('h1')
		self.assertIn('Sign In', body.text)

	@classmethod
	def tearDownClass(cls):
		cls._driver.quit()
