# Basic function
def add_one(num):
    print(num + 1)
add_one(3)

print("\n")


# First Class Object -- here we demonstrate how functions can be passed as arguments into other functions. 'say_hello' (without
# parenthesis) is passed into 'greet_bob' and produces "Hello, Bob!" What's happening? So 'say_hello' is the argument and the
# 'greet_bob' function concantonates '("Bob")' to the end of 'say_hello' which then invokes the say_hello function and passes
# "Bob" as its argument. Resulting in "Hello, Bob!" being printed. Same for the 'greet_bob(be_awesome)'.
def say_hello(name):
    print("Hello, " + name + "!")

def be_awesome(name):
    print("Yo, " + name + " together we are the awesomest!")

def greet_bob(greeter_func):
    return greeter_func("Bob")

greet_bob(say_hello)
greet_bob(be_awesome)

print("\n")

# Inner function -- This demonstrates that the order of the defining of functions isn't important, only the order in which
# they are called ('second_child()' output prints before 'first_child()'). Also the 'child' functions are local and only
# execute and defined when the 'parent()' function is called.
def parent():
    print("Printing from the parent() function")

    def first_child():
        print("Printing from the first_child() function")

    def second_child():
        print("Printing from the second_child() function")

    second_child()
    first_child()


parent()
