import os

from libs.cache import remove_cache
from libs.connection.internet import is_online
from libs.logger import console
from validation.model import validate_file_extension

from .args import ArgumentRequired

STOP = False
CONTINUE = True


def validate_run_arg(kwargs):
    run_arg = kwargs.get("run", False)
    if run_arg:
        with ArgumentRequired(**kwargs) as arg:
            arg.required("run", ["model", "source"], {"source": 0})
        return CONTINUE


def validate_clean_arg(kwargs):
    clean_arg = kwargs.get("clean", False)
    if clean_arg:
        exclude = kwargs.get("exclude", [])
        remove_cache(exclude)
        return STOP


def validate_model_arg(kwargs):
    model_arg = kwargs.get("model", None)
    if model_arg:
        if not os.path.isfile(str(model_arg)):
            console.fatal("Please specify the path of the model file")
        elif not validate_file_extension(model_arg):
            console.fatal(f"Model file {model_arg} is not a valid model")
        return CONTINUE


def general_validation(kwargs):
    if kwargs.get("supported_formats", False):
        return CONTINUE


def command_validation(**kwargs):
    if not is_online():
        console.fatal("You are not connected to the internet")

    return (
        validate_run_arg(kwargs)
        or validate_clean_arg(kwargs)
        or validate_model_arg(kwargs)
        or general_validation(kwargs)
    )
