def add_two_number(a, b):
    """this function add two number
    :param a: first number
    :param b: second number
    :return: sum of two number
    """
    
   
    return a + b

def three_numnber(a, b, c):
    return a + b + c
    """this function add three number
    
    """

def four_number(a, b, c, d):
    return a + b + c + d


def five_number(a, b, c, d, e):
    return a + b + c + d + e

#create a function that takes a list of numbers and returns the sum of the numbers
def sum_list(list):
    sum = 0
    for i in list:
        sum += i
    return sum

#create a function for login and signup with username , password , confirm password
def login(username, password, confirm_password):
    if password == confirm_password:
        print("login successful")
    else:
        print("password not match")
def signup(username, password, confirm_password):
    if password == confirm_password:
        print("signup successful")
    else:
        print("password not match")
        