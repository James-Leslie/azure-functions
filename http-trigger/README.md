# HTTP Trigger example
This example illustrates the ability to:
* trigger a function using HTTP `GET` / `POST` methods
* access sensitive information from Azure Key Vault inside the function

> All steps below assume you have completed all steps in [getting started](https://github.com/James-Leslie/azure-functions#0-getting-started)

## 1. Create and deploy the template HTTP trigger function

### 1.1. Create function locally
The first step is to create a local function project in VS Code. To do this, click on the Azure icon in your left panel and then click on the small "Create New Project" folder icon at the top of the Azure blade.

![Create local project](https://github.com/James-Leslie/azure-functions/blob/main/images/1.6_create-local.png?raw=true)

There will be a few prompts which you will need to respond to. 
This example uses the following settings:
  * **Folder**: "http-trigger"
  * **Language**: Python
  * **Authorisation**: anonymous

Once the project has been created locally, head back to the Explorer (Ctrl+Shift+E) and you will notice there are now many files in your chosen folder. For now, let's just take a look at the `__init__.py` file:

```python
import logging

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
```

This file contains the code needed for a very simple first function. When an HTTP `GET` or `POST` request is sent to the function URL (we'll get to this later), it will respond with either of the return calls in the final `if/else` block depending on whether or not a name has been passed in the query string.

### 1.2. Debug function locally
Once the function has been created, we can try it out right away.

Open the `__init__.py` file and press the `F5` key. This will start the debugger. You should get some logs while the virtual environment is created and the function boots up. Eventually, you should see the following:

![Start debugger](https://github.com/James-Leslie/azure-functions/blob/main/images/1.7_debug-local.png?raw=true)

Open the link for the HttpTrigger function by using Ctrl+Click. A new tab should open in your browser with the following:

![Run local](https://github.com/James-Leslie/azure-functions/blob/main/images/1.8_run-local.png?raw=true)

As the message says, we can get a more personalised response by appending a name to the query string:
`http://localhost:7071/api/HttpTrigger`**`?name=James`**

Which should then return the following:

![Run local with name](https://github.com/James-Leslie/azure-functions/blob/main/images/1.9_run-local-with-name.png?raw=true)

### 1.3. Deploy function to Azure Function App
