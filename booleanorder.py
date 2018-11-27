from collections import Counter
from functools import reduce
from multiprocessing import Pool
import itertools

def bool_and_str(a, b):
    return " (%s & %s) " % (a, b)

def bool_or_str(a, b):
    return " (%s | %s) " % (a, b)

def bool_not_str(a, b):
    return " (%s ^ %s) " % (a, b)

ops_format = {'&': bool_and_str,
              '|': bool_or_str,
              '^': bool_not_str}

def bool_and(a, b):
    return a & b

def bool_or(a, b):
    return a | b

def bool_not(a, b):
    return a ^ b

ops_map = {'&': bool_and, 
           '|': bool_or, 
           '^': bool_not}

def num_array(number):
    return reduce(lambda accum, item: [*accum, item] , range(number),[])

def permutations(list_of_numbers):
    return set(itertools.permutations(list_of_numbers))

def _solve(booleans, ops, priorities, ops_to_use, old_priorities = None):
    if old_priorities is None:
        old_priorities = priorities.copy()
    
    if len(ops) < 1:
        return (booleans[0], None)
    else:
        index = priorities.index(max(priorities))

        result = ops_to_use[ops[index]](booleans[index], booleans[index + 1])
        
        _ = priorities.pop(index)
        _        = ops.pop(index)
        new_booleans = [*booleans[:index], result, *booleans[index + 2:]]
    
        result, _ = _solve(new_booleans, ops, priorities, ops_to_use, old_priorities)
        return (result, old_priorities)

def solve(s,ops):
    boolean_map = {'t': True, 'f': False}
    booleans = list(map(lambda i: boolean_map[i], s))

    numbers = num_array(len(ops))
    
    priorities = permutations(numbers)
    
    operation_parameters = map(lambda priority: (booleans, list(ops), list(priority), ops_format), priorities)

    with Pool(processes = 10) as pool:
        mapped_operations = pool.starmap(_solve, operation_parameters)

    operation_string_to_priorities_map = {}
    for operation_string, operation_priorities in mapped_operations:
        operation_string_to_priorities_map[operation_string] = list(operation_priorities)

    results_strings = map(lambda item: item[0], mapped_operations)
    results_set = set(results_strings)

    optimized_operations = map(lambda result: (booleans, list(ops), operation_string_to_priorities_map[result], ops_map), results_set)

    with Pool(processes = 10) as pool:
        results = pool.starmap(_solve, optimized_operations)

    filtered_results = filter(lambda result: result is not None, map(lambda item: item[0], results) )

    return Counter(filtered_results)[True]
