import pkgutil
import importlib
import app.routes


class RouteManager:
    def __init__(self):
        self.routes = []

    def load_routes(self):
        """
        Dynamically scans and imports all modules in the app.routes package whose
        name starts with 'route_' and collects the route objects
        defined (expected to end with _route_obj).
        """
        # iterate over all modules in the app.routes package
        for finder, module_name, ispkg in pkgutil.iter_modules(
            app.routes.__path__, app.routes.__name__ + "."
        ):
            # check if module name indicates a route file
            if module_name.startswith("app.routes.route_"):
                module = importlib.import_module(module_name)
                # find attributes ending with _route_obj (e.g., question_route_obj)
                for attr in dir(module):
                    if attr.endswith("_route_obj"):
                        route_obj = getattr(module, attr)
                        self.routes.append(route_obj)

    def register_all(self):
        """Call the register() method on all collected route objects."""
        for route in self.routes:
            route.register()
