#
# a = [-20, -5, 10, 15]



def abs_sort(a):
    N = len(a)
    for i in range(N - 1):
        for j in range(N - i - 1):
            if abs(a[j]) > abs(a[j + 1]):
                a[j], a[j + 1] = a[j + 1], a[j]

    return a

# print(abs_sort(a))