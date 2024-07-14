Feature: Product Management
    As a user
    I want to manage products in the catalogue
    So that I can create, retrieve, update, and delete products

Scenario: Create a product
    Given a new product with SKU "12345"
    When the product is created
    Then the product with SKU "12345" should be retrievable

Scenario: Retrieve a product
    Given a product with SKU "12345" exists
    When the product is retrieved
    Then the product details should be correct

Scenario: Update a product
    Given a product with SKU "12345" exists
    When the product name is updated to "Updated Product Name"
    Then the product with SKU "12345" should have the updated name

Scenario: Delete a product
    Given a product with SKU "12345" exists
    When the product is deleted
    Then the product with SKU "12345" should not be retrievable
