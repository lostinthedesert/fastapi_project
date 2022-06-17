def do_twice2(func):
    def wrapper_do_twice2(*args, **kwargs):
        func(*args, **kwargs)
        func(*args, **kwargs)
    return wrapper_do_twice2

