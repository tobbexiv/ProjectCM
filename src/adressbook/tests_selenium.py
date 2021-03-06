from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from django.test import LiveServerTestCase
# Create your tests here.

class TestCaseLogin(LiveServerTestCase):

	@classmethod	
	def setUpClass(cls):
		cls._password_peter = '123'		
		cls._driver = webdriver.PhantomJS()
		cls._driver.set_window_size(1124, 850)


	def test_1_login(self):
		self._driver.get("http://localhost:8000/")
		self._driver.find_element_by_id('id_username').send_keys("peter")
		self._driver.find_element_by_id('id_password').send_keys(self._password_peter)
		self._driver.find_element_by_id('login').click();
		body = self._driver.find_element_by_class_name('page_title')
		self.assertIn('Project CM', body.text)

	def test_3_logout(self):
		self._driver.get("http://localhost:8000/")
		self._driver.find_element_by_id('logout').click()
		body = self._driver.find_element_by_class_name('page_title')
		self.assertIn('ProjectCM', body.text)

	@classmethod
	def tearDownClass(cls):
		cls._driver.quit()
