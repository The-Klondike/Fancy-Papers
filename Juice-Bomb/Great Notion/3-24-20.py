# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 10:52:18 2020

@author: kyler
"""
import time

print(time.asctime())

#%% define multiply_numbers
def multiply_numbers(num1, num2, print_result=False):
    """
    
    Here we describe what the function should do.
    This function takes two numbers and returns the product.
    It also has the option to print the result to the console.
​
    Args:
        num1 (number): The first number to multiply.
        num2 (number): The second number to multiply.
        print_result (boolean, optional): Choose to print the result to the console. Defaults to False.
​
    Returns:
        Returns the product of two numbers.
    """
    # multiply the numbers
    product = num1 * num2
    # if print result is true, print to console
    if print_result:
        print("The product is:", product)
    # return the product
    return product
#%% run multiply_numbers
example1 = multiply_numbers(3, 24)    
print(example1)
# run another example with print_result = True
example2 = multiply_numbers(12, 34, print_result=True)
#%% testing functions
def testing():
    """ this function contains tests """
    
    # test that multiply numbers works properly
    input1 = 3
    input2= 24
    expected = 72
    test1 = multiply_numbers(input1, input2)
    
    # test that the function gives the expected output
    print("Test multiply_number:", test1 == expected)
#%% call tests
testing()