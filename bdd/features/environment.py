import os


def before_all(context):
    context.base_url = os.environ["BASE_URL"]
