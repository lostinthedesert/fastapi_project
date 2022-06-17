# This is a decorator function. We have a parent function that takes another function as it's parameter and then runs a
# function upon execution. 'my_decorator' returns the 'wrapper' function which prints two lines of text and calls a function
# in the middle (that function being the parameter of 'my_decorator', in this case 'say_whee()')

# Using the shell, if we call 'say_whee' (no '()'), the program will return a reference to the 'wrapper' function. But if
# we call 'say_whee()' the entire code will be executed and we will get"
# "Something is happening before the function is called.
#  Whee!
#  Something is happening after the function is called."
# That extra '()' on the shell input 'say_whee' invokes the imbedded function ('func()', which invokes 'say_whee()')

def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

# In the first explanation of this code, we used the variable 'say_whee' to invoke the 'my_decorator' function. The correct
# way to express this is with the '@' (pie syntax) in front of our parent function ('my_decorator'). It serves the exact same
# purpose as the line 'say_whee = my_decorator(say_whee_)' but more succinctly. It appears as if python looks for a function
# immediately after the '@my_decorator', that's how it knows how to interpret 'say_whee()'. So to invoke the decorator we
# call 'say_whee' in the shell propmt or enter 'say_whee' in the program code below the decorator

@my_decorator
def say_whee():
    print("Whee!")
    
# say_whee = my_decorator(say_whee)

