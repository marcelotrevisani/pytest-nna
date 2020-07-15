import logging
from copy import deepcopy
from functools import wraps
from timeit import default_timer as timer

from arca import all_components


log = logging.getLogger(__name__)

class ArcaComponent:
    def __init__(self):
        self._all_components = deepcopy(all_components)

    def __getattr__(self, item):
        if item not in self._all_components:
            raise AttributeError(f"Attribute {item} not found.")

        func_ex = self._all_components[item].function
        @wraps(func_ex)
        def wrapped_function(*args, **kwargs):
            log.debug(f"Calling {func_ex.__name__} with args {args}, {kwargs}")
            start = timer()
            return_value = func_ex(*args, **kwargs)
            end = timer()
            log.debug(f"Return of {func_ex.__name__}: {return_value}")
            log.debug(f"Time to execute {func_ex.__name__}: {end - start} seconds")
            return return_value
        return wrapped_function

    def __getitem__(self, item):
        if item in self._all_components:
            return self._all_components[item].function
        raise ValueError(f"Component {item} does not exist.")

    def __delitem__(self, key):
        raise AttributeError(f"It is not possible to delete elements.")

    def __setitem__(self, key, value):
        raise AttributeError(f"It is not possible to set elements.")
