import functools

# Highest form of 'do_twice#' decorator
def do_twice(func):
    @functools.wraps(func)
    def wrapper_do_twice(*args, **kwargs):
        func(*args, **kwargs)
        return func(*args, **kwargs)
    return wrapper_do_twice

def do_twice2(func):
    def wrapper_do_twice2(*args, **kwargs):
        func(*args, **kwargs)
        func(*args, **kwargs)
    return wrapper_do_twice2

def do_twice0(func):
    def wrapper_do_twice0():
        func()
        func()
    return wrapper_do_twice0
