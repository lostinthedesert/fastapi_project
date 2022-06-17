# This illustrates how to import a decorator and refer to it in a separate program. So we created a normal decorator in a
# separate .py file and then imported it just like any other class/object. The name of this particular decorator is 'do_twice'
# and it is saved in the decorators_module.py file.

# In this example, our 'hello()' function should be executed twice by our 'do_twice' function (decorator)
# Note: the inner function of a decorator is called a 'wrapper'. It is common to name the inner function after the decorator,
# so in this example the inner function of the decorator 'do_twice' is 'wrapper_do_twice'.

from decorators_module import do_twice
from decorators_module2 import do_twice2

@do_twice
def hello():
    print("hello world")

# As you can see above we have imported a second decorator from 'decorators_module2.py'. This decorator includes code (*args,
# **kwargs) that will allow you to pass arguments through your decorator. This will allow you to pass functions to the
# decorator with or without arguments.

@do_twice2
def hello_world(name):
    print("Hello, " +name+"!")
    
    
