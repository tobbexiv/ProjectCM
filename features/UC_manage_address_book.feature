Feature: manage address book
  As an user
  I want to manage my address book
  So that I can write E-Mails to my contacts or other people

  Scenario: create contact
    Given I am logged in 
	And I am on the contact list
	And I clicked create contact
    When I type in the correct contact data
    And I upload a profile picture for the contact
    And I click create
	Then I should see a confirmation message    

  Scenario: delete contact
	Given I am logged in
    And I am on the contact list
	And I clicked delete contact
    When I confirm the deletion
	Then I should see a confirmation message
	
  Scenario: update contact data
    Given I am logged in
    And I am on the contact list
	And I clicked edit for a contact
	When I change the data correctly
	Then I should see a confirmation message
	
  Scenario: view single contact
    Given I am logged in 
	And I am on the contact list
	And I clicked show for a contact
	When I click back 
	Then I should see the list of contacts
	
  Scenario: abort creating new contact
    Given I am logged in 
	And I clicked create contact
	When I click abort
	Then I should see the list of contacts
	
  Scenario: create contact with false data
    Given I am logged in
	And I clicked create contact
	When I type in false data
	Then I should see an error message