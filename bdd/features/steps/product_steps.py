import requests
from behave import given, then, when


@given('a new product with SKU "{sku}"')
def step_given_new_product(context, sku):
    context.product_data = {
        "sku": sku,
        "name": "Test Product",
        "description": "This is a test product",
        "image_url": "http://example.com/image.jpg",
        "price": {"value": 100.0, "discount_percent": 0.1},
        "inventory": {"quantity": 50, "reserved": 5},
        "category": {"name": "Test Category"},
    }


@when("the product is created")
def step_when_create_product(context):
    response = requests.post(
        f"{context.base_url}/product", json=context.product_data
    )
    context.response = response
    assert (
        response.status_code == 200
    ), f"Failed to create product: {response.json()}"


@then('the product with SKU "{sku}" should be retrievable')
def step_then_product_retrievable(context, sku):
    response = requests.get(f"{context.base_url}/product/{sku}")
    assert response.status_code == 200, f"Product not found: {response.json()}"
    context.retrieved_product = response.json()
    assert context.retrieved_product["sku"] == sku


@given('a product with SKU "{sku}" exists')
def step_given_product_exists(context, sku):
    response = requests.get(f"{context.base_url}/product/{sku}")
    if response.status_code == 404:
        step_given_new_product(context, sku)
        step_when_create_product(context)
    else:
        context.product_data = response.json()


@when("the product is retrieved")
def step_when_product_retrieved(context):
    response = requests.get(
        f"{context.base_url}/product/{context.product_data['sku']}"
    )
    context.response = response
    assert response.status_code == 200, f"Product not found: {response.json()}"


@then("the product details should be correct")
def step_then_product_details_correct(context):
    product = context.response.json()
    assert product["sku"] == context.product_data["sku"]
    assert product["name"] == context.product_data["name"]


@when('the product name is updated to "Updated Product Name"')
def step_when_update_product_name(context):
    context.product_data["name"] = "Updated Product Name"
    response = requests.put(
        f"{context.base_url}/product/{context.product_data['sku']}",
        json=context.product_data,
    )
    context.response = response
    assert (
        response.status_code == 200
    ), f"Failed to update product: {response.json()}"


@then('the product with SKU "{sku}" should have the updated name')
def step_then_product_name_updated(context, sku):
    response = requests.get(f"{context.base_url}/product/{sku}")
    assert response.status_code == 200, f"Product not found: {response.json()}"
    product = response.json()
    assert product["name"] == "Updated Product Name"


@when("the product is deleted")
def step_when_delete_product(context):
    response = requests.delete(
        f"{context.base_url}/product/{context.product_data['sku']}"
    )
    context.response = response
    assert (
        response.status_code == 200
    ), f"Failed to delete product: {response.json()}"


@then('the product with SKU "{sku}" should not be retrievable')
def step_then_product_not_retrievable(context, sku):
    response = requests.get(f"{context.base_url}/product/{sku}")
    assert response.status_code == 404, "Product should not be retrievable"
