
# this is a template for complex decorators. The 'functools' module is a support module for decorators, it helps when referencing
# inner functions, I'm not really clear on it's use but it's not strictly necessary for the decorator to work.

# 'functools.wraps' is the syntax for invoking the functools rules on a given decorator/wrapper.
# Now if we request a reference to a wrapper like 'say_whee' python will return something like 'function say_whee at 0x09039'
# instead of naming the parent decorator function and referring to the inner function as a 'local.function_wrapper'. Again
# the code works fine without it but apparently this is ettiquette and important.

import functools

def decorator(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        # Do something before
        value = func(*args, **kwargs)
        # Do something after
        return value
    return wrapper_decorator
