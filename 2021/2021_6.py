from functools import lru_cache

# f(n, a) where f is the amount of fish on day n, given initial state a
@lru_cache(maxsize=None)
def f(n, a):
    nf = 1
    n -= a
    while n > 0:
        nf += f(n, 9)
        n -= 7
    return nf

#  0: [1]
assert f(0,1) == 1
#  1: [0]
assert f(1,1) == 1
#  2: [6, 8]
assert f(2,1) == 2
#  3: [5, 7]
#  4: [4, 6]
#  5: [3, 5]
#  6: [2, 4]
#  7: [1, 3]
#  8: [0, 2]
assert f(8,1) == 2
#  9: [6, 1, 8]
assert f(9,1) == 3
# 10: [5, 0, 7]
assert f(10,1) == 3
# 11: [4, 6, 6, 8]
assert f(11,1) == 4

assert f(4,3) == 2

with open("2021_6_input") as file:
    fish = [int(f) for f in file.readline().split(',')]

    for n in range(11):
        print("Number of fish after " + str(n) + " days: " + str(sum([f(n, a) for a in fish])))
    print("Number of fish after 80 days: " + str(sum([f(80, a) for a in fish])))
    print("Number of fish after 256 days: " + str(sum([f(256, a) for a in fish])))
    print(f.cache_info())



