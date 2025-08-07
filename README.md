# AzureFunctions-Python
Sample Azure Functions project with Python

## Project Structure
The recommended folder structure for a Python functions project looks like the following example:
```text
<project_root>/
├── .venv/
├── .vscode/
├── docs/
├── test/
│   ├── test_asb_functions.md
│   └── test_http_functions.py
├── .funcignore
├── blueprint_asb_functions.py
├── blueprint_http_functions.py
├── function_app.py
├── host.json
├── local.settings.json
└── requirements.txt
```

## Blueprints
The Python v2 programming model introduces the concept of blueprints. A blueprint is a new class that's instantiated to register functions outside of the core function application. The functions registered in blueprint instances aren't indexed directly by the function runtime. To get these blueprint functions indexed, the function app needs to register the functions from blueprint instances.

Using blueprints provides the following benefits:

- Lets you break up the function app into modular components, which enables you to define functions in multiple Python files and divide them into different components per file.
- Provides extensible public function app interfaces to build and reuse your own APIs.

## Running Locally

To run locally, use the following command.
```bash
func start
```
This uses the Azure Functions Core Tools to host your functions. Use the REST client test files (*.http) to test the HTTP trigger functions.

To run locally with authentication enabled, use the following command.
```bash
func start --enableAuth
```
In the local azurite/storage emulator, you can find the function keys in the `azure-webjob-secrets` blob container. Find your key in the `host.json` file the app's hostId-named folder.
