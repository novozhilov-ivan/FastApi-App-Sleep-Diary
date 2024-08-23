from src.application.api.namespaces.main.endpoint import MainEndpoint
from src.application.api.namespaces.main.namespace import namespace_main


main_endpoint = "main"
namespace_main.add_resource(
    MainEndpoint,
    "/main",
    endpoint=main_endpoint,
)
