"""
Sort the odd (6 kyu)
"""

def sort_array(source_array):
    odds = list(filter(lambda number: number % 2 != 0, source_array))
    odds = sorted(odds)
    return [number if number % 2 == 0 else odds.pop(0) for number in source_array]

