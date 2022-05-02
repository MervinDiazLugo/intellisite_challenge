@Intellisite
Feature: Test Intellisite WebApi

  @users
  Scenario: GET my user data
    Given I login in Intellisite App
    Given I connect with endpoint users/me
    When I do a Get
    Then I print out the results of the response
    Then The api response is 200
    Then The elements <Entity> show the values <Value>
      | Entity    | Value          |
      | username  | user           |
      | role      | superadmin     |

  @users
  Scenario: Get user data without API Authentication
    Given I connect with endpoint users/me
    When I do a Get
    Then I print out the results of the response
    Then The api response is 401
    Then The elements <Entity> show the values <Value>
      | Entity    | Value                |
      | detail    | Not authenticated    |

  @users
  Scenario: Create a new client user
    Given I login in Intellisite App
    Given I connect with endpoint users/
    Then I set the entity username with the value random
    Then I set the entity role with the value client
    Then I set the entity password with the value random
    When I do a Post
    Then I print out the results of the response
    Then The api response is 200

  @users
  Scenario: Get data from non-existent user
    Given I login in Intellisite App
    Given I connect with endpoint users/notfoundUser
    When I do a Get
    Then I print out the results of the response
    Then The api response is 404
    Then The elements <Entity> show the values <Value>
      | Entity    | Value         |
      | detail    | Not Found     |


  @stats
  Scenario: Get site statistics
    Given I login in Intellisite App
    Given I connect with endpoint stats/
    When I do a Get
    Then I print out the results of the response
    Then The api response is 200
    Then The elements <Entity> show the values <Value>
      | Entity      | Value         |
      | Scion       | NOT NULL      |
      | Kia         | NOT NULL      |
      | Rolls-Royce | NUMERIC       |
      | Buick       | NUMERIC       |

  @stats
  Scenario: Get site statistics without API Authentication
    Given I connect with endpoint stats/
    When I do a Get
    Then I print out the results of the response
    Then The api response is 401
    Then The elements <Entity> show the values <Value>
      | Entity    | Value                |
      | detail    | Not authenticated    |

  @detections
  Scenario: Get detections
    Given I login in Intellisite App
    Given I connect with endpoint detections?skip=0&limit=5
    When I do a Get
    Then I print out the results of the response
    Then The api response is 200
    Then I compare <Entity> have the values <Value>
      | Entity                   | Value           |
      | [0]._id                  | NOT NULL        |
      | [0].Year                 | 2003            |
      | [0].Make                 | Land Rover      |
      | [0].Model                | Range Rover     |
      | [0].Category             | SUV             |

    @detections
  Scenario: Get detections without API Authentication
    Given I connect with endpoint detections?skip=0&limit=5
    When I do a Get
    Then I print out the results of the response
    Then The api response is 401
    Then The elements <Entity> show the values <Value>
      | Entity    | Value                |
      | detail    | Not authenticated    |