import sys


class Executor:
    def __init__(self, opt):
        if opt is None:
            raise ValueError("opt should not be None")
        self.opt = opt

    def __enter__(self):
        if self.opt is None:
            raise ValueError("Invalid state, opt should not be None")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.exit(0)

    def target(self, func, h):
        if not callable(func):
            raise ValueError("func should be callable")
        if h is None:
            raise ValueError("h should not be None")
        
        if h:
            func(self.opt)