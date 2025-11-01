# Sorting a 2D list (method 1)
lst = [[3, 1, 5], [4, 0, 2]]
print("original list ",lst)
for row in lst:
    row.sort()
print("sorted list 1 ",lst)


# Sorting a 2D list (method 2)
lst = [[3, 1, 5], [4, 0, 2]]
sorted_list = []

for row in lst:
    for col in range(len(row)):
        row.sort()
    sorted_list.append(row)

print("sorted list 2",sorted_list)


# Transpose of a matrix
def is_matrix(lst):
    if not isinstance(lst, list) or not lst:
        return False
    row_length = len(lst[0])
    for row in lst:
        if not isinstance(row, list):
            return False
        if len(row) != row_length:
            return False
    return True


def transpose_matrix(m):
    if not is_matrix(m):
        return False

    num_rows = len(m)
    num_cols = len(m[0])

    new_matrix = []
    num_rows_new_matrix = len(m[0])
    num_cols_new_matrix = len(m)

    for i in range(0, num_rows_new_matrix):
        new_row = []
        for j in range(0, num_cols_new_matrix):
            new_row.append(m[j][i])
        new_matrix.append(new_row)

    return new_matrix


m = [[3, 1, 5], [4, 0, 2]]
print("transport of matrix",transpose_matrix(m))

# Sum of list
def sum_list(n):
    return sum_list_itr(n, len(n) - 1)

def sum_list_itr(lst, index):
    if index < 0:
        return 0
    return lst[index] + sum_list_itr(lst, index - 1)

print()

import numpy as np
print("Sorted list using numpy:")
lst = np.array([[3, 1, 5], [4, 0, 2]])
sort = np.sort(lst, axis=1)
print(sort)

# Transpose of the list
transpose = lst.T
print("\nTranspose of list using numpy:",transpose)

# Sum of list
print("\nSum of list is using numpy:")
m = np.sum(lst)
print(m)

