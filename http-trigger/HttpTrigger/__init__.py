import logging
import os

import azure.functions as func

# access sensitive credentials from Azure Key Vault
user_name = os.getenv('UsernameFromKeyVault')
password = os.getenv('PasswordFromKeyVault')


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    return func.HttpResponse(
        f'Hello {user_name}, your password is {password}.',
        status_code=200
    )
