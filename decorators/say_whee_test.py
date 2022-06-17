import functools

def my_decorator(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        print("Something is happening before the function is called.")
        func(*args, **kwargs)
        print("Something is happening after the function is called.")
    return wrapper_decorator

@my_decorator
def say_whee(name):
    print("Whee, "+ name+"!")
    
@my_decorator
def nameless_whee():
    print("Whee!")
