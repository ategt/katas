"""
Factorial tail (4 kyu)

The problem
How many zeroes are at the end of the factorial of 10? 10! = 3628800, i.e. there are 2 zeroes. 16! (or 0x10!) in hexadecimal would be 0x130777758000, which has 3 zeroes.

Scalability
Unfortunately, machine integer numbers has not enough precision for larger values. Floating point numbers drop the tail we need. We can fall back to arbitrary-precision ones - built-ins or from a library, but calculating the full product isn't an efficient way to find just the tail of a factorial. Calculating 100'000! in compiled language takes around 10 seconds. 1'000'000! would be around 10 minutes, even using efficient Karatsuba algorithm

Your task
is to write a function, which will find the number of zeroes at the end of (number) factorial in arbitrary radix = base for larger numbers.

base is an integer from 2 to 256
number is an integer from 1 to 1'000'000
Note Second argument: number is always declared, passed and displayed as a regular decimal number. If you see a test described as 42! in base 20 it's 4210 not 4220 = 8210.
"""

def tq(s, b):
    "I was so sleepy when I wrote this, I do not remember what the tq stands for."
    ins = []
    zx = int(s)

    while(zx > 1):
        zx = zx // b
        ins.append(zx)

    return sum(ins)

def factorize(base):
    px = set()
    for i in range(2, base+1):
        if base % i == 0:
            p = 0
            while ( base % i == 0 ):
                base = base / i
                p += 1
            px.add((i, p))

    return px
    
def zeroes (base, number):
    " Inspired by http://stackoverflow.com/questions/23202489/how-does-this-code-find-the-number-of-trailing-zeros-from-any-base-number-factor "
        
    factors = factorize(base)
            
    return min(tq(number, factor) // power for factor, power in factors)
