# azure-functions
Starter code for Azure functions in Python

## 0. Getting started
The subfolders of this repository contain example Azure functions which can be used as starter templates.

All of the functions require the following before they can be deployed:
* Azure subcription ([get a free account here](azure.microsoft.com/en-us/free))
* Resource group and Function App in Azure
* Visual Studio Code with [Azure Functions](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions) and [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) extensions enabled

### 0.1 Create Azure Function app
To create Azure Functions, you will first need a Function App in your Azure resource group. 

![Create app](https://github.com/James-Leslie/azure-functions/blob/main/images/1.1_create-function-app.png?raw=true)

In the application settings, choose a globally unique name and select the Python runtime stack.

![App settings](https://github.com/James-Leslie/azure-functions/blob/main/images/1.2_app-hosting-settings.png?raw=true)

It's a good idea to enable application monitoring, as this will allow us to review the application run logs in the Azure portal.

![App monitoring](https://github.com/James-Leslie/azure-functions/blob/main/images/1.3_app-monitoring.png?raw=true)

Once the Function App has been created, your resource group should have the following contents in it:

![Resource group contents](https://github.com/James-Leslie/azure-functions/blob/main/images/1.4_resource-group-contents.png?raw=true)

### 0.2 Create local Azure Function project in Azure
Once you have intalled the [Azure Functions extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions) for VS Code, you should see an additional icon appear in your left panel. When you click it, you will be prompted to sign in to your Azure account, after which you will be able to see your subscription and the Function App you created in the previous step.

![VS code extension](https://github.com/James-Leslie/azure-functions/blob/main/images/1.5_functions-vs-code-extension.png?raw=true)

