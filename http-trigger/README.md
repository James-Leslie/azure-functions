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
The function is now ready to be deployed to our existing Azure Function App.

In the explorer pane, right-click on the project folder and click on the option "Deploy to Function App..."

![Deploy](https://github.com/James-Leslie/azure-functions/blob/main/images/1.10_deploy.png?raw=true)

Select your subscription and the created Function App when prompted to do so.

### 1.4. Trigger the deployed function
The final step is to test that the deployed function works when we call it. We can call the Azure function from our browser in the same way as before, but using the deployed function's URL.

Open up the Azure panel in VS Code and find your deployed function. When you right-click on it, you will see the option to "copy function URL". 

![Function URL](https://github.com/James-Leslie/azure-functions/blob/main/images/1.11_function-url.png?raw=true)

If you copy this and paste it into your browser's address bar, you will see the same response as before, but now this response is being sent to us from our live Azure serverless function!

## 2. Modify the starter template to access Azure Key Vault

### 2.1. Add key(s) to local environment
The file `local.settings.json` can be used to store our keys for local testing. We do not need to use any special Azure Key Vault Python packages.

Modify this file with some dummy keys. Below, I have called the keys "UsernameFromKeyVault" and "PasswordFromKeyVault".

```python
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "UsernameFromKeyVault": "James",
    "PasswordFromKeyVault": "Pwd"
  }
}
```

These values will be accessible in the Python code by using the `os.getenv()` function.

### 2.2. Modify `__init__.py` to retrieve keys from vault
Let's replace the starter template code with our own:

```python
import logging
import os

import azure.functions as func

# access sensitive credentials from Azure Key Vault
user_name = os.getenv('UsernameFromKeyVault')
password = os.getenv('PasswordFromKeyVault')


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    return func.HttpResponse(
        # reference credentials in function call
        f'Hello {user_name}, your password is {password}.',
        status_code=200
    )
```

If you save this file and test locally (`F5`), you will see a new message returned from the function. The key values have been retrieved from the local environment and used in the function return.

![Debug function](https://github.com/James-Leslie/azure-functions/blob/main/images/2.7_debug-function.png?raw=true)

### 2.3. Add keys to Azure Key Vault

#### 2.3.1. Enable Function App System Identity
In the Azure portal, go to your Function App. Under **Settings -> Identity** set the status to "On":

![App identity](https://github.com/James-Leslie/azure-functions/blob/main/images/2.1_app-identity.png?raw=true)

#### 2.3.2. Create a key vault and add the credentials
Create a new Key Vault in your resource group. In the **Access policy** section of creating the vault, click on the text that says "+ Add Access Policy".

![Add access policy](https://github.com/James-Leslie/azure-functions/blob/main/images/2.2_add-access-policy.png?raw=true)

Click the dropdown box to **Configure from template** and choose "Secret Management". Then click on the text that says "None selected" and search for the name of your function app in the panel on the right to provide it with access to the vault.

![Access policy settings](https://github.com/James-Leslie/azure-functions/blob/main/images/2.3_access-policy-settings.png?raw=true)

![Select principal](https://github.com/James-Leslie/azure-functions/blob/main/images/2.4_select-principal.png?raw=true)

Click on "Add" and then confirm that your list of current access policies for the key vault looks like the list below before creating the vault.

![Current policies](https://github.com/James-Leslie/azure-functions/blob/main/images/2.5_current-access-policies.png?raw=true)

Finally, add your desired secrets to the vault. While the _values_ of these secrets do not need to be the same, their names need to be exactly the same as the ones you added to your `local.settings.json` file. In this example, we named them **UsernameFromKeyVault** and **PasswordFromKeyVault**. To illustrate the point, I have also changed the secret value of the password stored in the vault.

#### 2.3.3. Add vault secrets to app configuration
Now, the final step is to add these secrets to the function app. You will want to keep the vault open in a tab of your browser while you open a new tab with the function app configuration settings.

Click on the button to create a new application setting:

![App configuration](https://github.com/James-Leslie/azure-functions/blob/main/images/2.6_app-configuration.png?raw=true)

In your other tab, open the information of the username secret and click on the enabled version to see its details. There is a field here called **Secret Identifier**, copy its value and head back to the other tab.

![Secret identifier](https://github.com/James-Leslie/azure-functions/blob/main/images/2.8_secret-identifier.png?raw=true)
