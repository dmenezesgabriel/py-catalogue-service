import os

import requests


def clean_product(context, sku):
    try:
        response = requests.delete(f"{context.base_url}/product/{sku}")
        print(response.json())
    except Exception as error:
        print(error)


def before_all(context):
    context.base_url = os.environ["BASE_URL"]
    context.sku = None  # Initialize the SKU context variable


def before_scenario(context, scenario):
    if context.sku:
        clean_product(context, context.sku)
    context.sku = None  # Reset the SKU before each scenario


def after_scenario(context, scenario):
    if context.sku:
        clean_product(context, context.sku)
