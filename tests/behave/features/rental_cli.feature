Feature: Rental App CLI

  @car
  Scenario: Normal Register Car
    Given Car Data
    When I register Car
    Then I receive success response
