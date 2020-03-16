Feature: Rental App CLI

  @car
  Scenario: Normal Register Car
    Given Car Data
    When I register Car
    Then I see car saved success


  @car
  Scenario: Normal Search Car by registration number
    Given Car Data
    And Car success Saved
    When I search Car by registration number
    Then I see listed car


  @rent
  Scenario: Normal Rent Car
    Given Car Data
    And Car success Saved
    And Rent Data
    When I rent Car
    Then I see rent success


  @rent
  Scenario: Normal Reserve Car
    Given Car Data
    And Car success Saved
    And Rent Data
    When I reserve Car
    Then I see reserve success


  @rent
  Scenario: Normal See Car Status
    Given Car Data
    And Car success Saved
    And Rent Data on 2020-03-19
    When I rent Car
    And I Check Car Status On 2020-03-19
    Then I see car status
