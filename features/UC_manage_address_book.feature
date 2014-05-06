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