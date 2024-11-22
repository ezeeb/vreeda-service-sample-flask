import os
import importlib.util

def register_blueprints(app, base_path='api.routes'):
    # Get the base directory for importing routes
    base_directory = os.path.join(os.path.dirname(__file__), '..', 'routes')

    # Walk through the base_directory to find all route files
    for root, _, files in os.walk(base_directory):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                # Construct module path for dynamic import
                module_path = os.path.join(root, file)
                module_name = module_path.replace(base_directory, '').replace(os.path.sep, '.').lstrip('.').replace('.py', '')

                # Generate full module name for import (e.g., "api.routes.auth.login")
                full_module_name = f"{base_path}{module_name}"

                # Dynamically import the module
                spec = importlib.util.spec_from_file_location(full_module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Register the Blueprint if it exists in the module
                if hasattr(module, 'blueprint'):
                    app.register_blueprint(getattr(module, 'blueprint'))
