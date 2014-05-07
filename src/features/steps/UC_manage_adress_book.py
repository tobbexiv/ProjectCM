from behave import *
from django.conf import settings

@given('a user')
def step_impl(context):
    from django.contrib.auth.models import User
    password = 'testpassword'
    user = User(username="peter", password=password)


@when('I log in')
def step_impl(context):
    br = context.browser
    br.open(context.browser_url('/accounts/login'))
    br.select_form(nr=0)
    br.form['username'] = 'peter'
    br.form['password'] = 'testpassword'
    br.submit

@then('I see the landing page')
def step_impl(context):
    br = context.UC_manage_address_book
    response = br.response()
    soup = context.parse_soup()
    msg = str(soup.findAll('h1')[0])
    assert response.code == 200
    assert "ProjectCM Main Page" in msg

@given('I am logged in')
def step_impl(context):
	assert False

@given('I am on the contact list')
def step_impl(context):
	assert False

@given('I clicked create contact')
def step_impl(context):
	assert False

@when('I type in the correct contact data')
def step_impl(context):
	assert False

@when('I upload a profile picture for the contact')
def step_impl(context):
	assert False

@when('I click create')
def step_impl(context):
	assert False

@then('I should see a confirmation message')
def step_impl(context):
	assert False

@given('I clicked delete contact')
def step_impl(context):
	assert False

@when('I confirm the deletion')
def step_impl(context):
	assert False

@given('I clicked edit for a contact')
def step_impl(context):
	assert False

@when('I change the data correctly')
def step_impl(context):
	assert False

@given('I clicked show for a contact')
def step_impl(context):
	assert False

@when('I click back')
def step_impl(context):
	assert False

@then('I should see the list of contacts')
def step_impl(context):
	assert False

@when('I click abort')
def step_impl(context):
	assert False

@when('I type in false data')
def step_impl(context):
	assert False

@then('I should see an error message')
def step_impl(context):
	assert False