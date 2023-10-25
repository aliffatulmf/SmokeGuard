from functools import partial

from .cache import remove_cache
from .handler import Handler, dependency_handler


def define_handler_instance(parsed_arguments):
    handler_instance = Handler()
    handler_instance.add_handler("clean", remove_cache)
    handler_instance.add_handler(
        "install_required",
        partial(
            dependency_handler,
            name=parsed_arguments.name,
            reinstall=parsed_arguments.reinstall,
        ),
    )
    return handler_instance


def process_handlers(parsed_arguments, handler_instance):
    for key, value in vars(parsed_arguments).items():
        if isinstance(value, bool):
            if key in handler_instance.handlers and value:
                handler_instance.call_handler(key)
