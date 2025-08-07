# AzureFunctions-Python
Sample Azure Functions project with Python

## Project Structure
The recommended folder structure for a Python functions project looks like the following example:
```text
<project_root>/
 | - .venv/
 | - .vscode/
 | - function_app.py
 | - additional_functions.py
 | - test/
 | | - test_my_function.py
 | - .funcignore
 | - host.json
 | - local.settings.json
 | - requirements.txt
 | - Dockerfile
```

## Blueprints
The Python v2 programming model introduces the concept of blueprints. A blueprint is a new class that's instantiated to register functions outside of the core function application. The functions registered in blueprint instances aren't indexed directly by the function runtime. To get these blueprint functions indexed, the function app needs to register the functions from blueprint instances.

Using blueprints provides the following benefits:

- Lets you break up the function app into modular components, which enables you to define functions in multiple Python files and divide them into different components per file.
- Provides extensible public function app interfaces to build and reuse your own APIs.