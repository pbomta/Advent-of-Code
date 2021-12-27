import math
import itertools

def parse(S):
    result = []
    for c in S:
        if c.isnumeric():
            result.append(int(c))
        elif c == ',':
            continue
        else:
            result.append(c)
    return result

def pp(S):
    result = ""
    last_s = None
    for s in S:
        if type(s) == int and (type(last_s) == int or last_s == ']'):
            result += ','
        elif s == '[' and (last_s == ']' or type(last_s) == int):
            result += ','
        result += str(s)
        last_s = s
    print(result)

assert(parse("[1,2]") == ['[', 1, 2, ']'])

def add(a, b):
    return ['['] + a + b + [']']

assert(add(['[', 1, 2, ']'], ['[', 3, 4, ']']) == ['[', '[', 1, 2, ']', '[', 3, 4, ']', ']'])

def explode_once(L):
    d = 0
    for n in range(len(L)):
        if L[n] == '[':
            d += 1
        elif L[n] == ']':
            d -= 1
        elif d == 5 and type(L[n + 1]) == int: 
            # print(str(L[n]) + " " + str(L[n + 1]) )
            # assert(type(L[n + 1]) == int)
            nl = n - 1
            while nl > 0:
                if type(L[nl]) == int:
                    L[nl] += L[n]
                    break
                nl -= 1
            nr = n + 2
            while nr < len(L):
                if type(L[nr]) == int:
                    L[nr] += L[n + 1]
                    break
                nr += 1
            del L[n - 1: n + 3]
            L.insert(n - 1, 0)
            return L
    return L

def split_once(L):
    for n in range(len(L)):
        if type(L[n]) == int and L[n] > 9:
            lhs = math.floor(L[n] / 2)
            rhs = math.ceil(L[n] / 2)
            del L[n]
            L.insert(n, ']')
            L.insert(n, rhs)
            L.insert(n, lhs)
            L.insert(n, '[')
            return L
    return L

def reduce_once(L):
    Lnext = explode_once(L.copy())
    if Lnext == L:
        Lnext = split_once(L.copy())
    return Lnext

assert(reduce_once(parse("[[[[[9,8],1],2],3],4]")) == parse("[[[[0,9],2],3],4]"))
assert(reduce_once(parse("[7,[6,[5,[4,[3,2]]]]]")) == parse("[7,[6,[5,[7,0]]]]"))
assert(reduce_once(parse("[[6,[5,[4,[3,2]]]],1]")) == parse("[[6,[5,[7,0]]],3]"))
assert(reduce_once(parse("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]")) == parse("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"))
assert(reduce_once(parse("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]")) == parse("[[3,[2,[8,0]]],[9,[5,[7,0]]]]"))

def reduce_all(L):
    while True:
        Lnext = reduce_once(L.copy())
        if Lnext == L:
            return L
        L = Lnext.copy()

s0 = parse("[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]")
s1 = reduce_all(add(s0, parse("[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]")))
assert(s1 == parse("[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]"))
s2 = reduce_all(add(s1, parse("[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]")))
assert(s2 == parse("[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]"))
s3 = reduce_all(add(s2, parse("[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]")))
assert(s3 == parse("[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]"))
s4 = reduce_all(add(s3, parse("[7,[5,[[3,8],[1,4]]]]")))
assert(s4 == parse("[[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]"))
s5 = reduce_all(add(s4, parse("[[2,[2,2]],[8,[8,1]]]")))
assert(s5 == parse("[[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]"))
s6 = reduce_all(add(s5, parse("[2,9]")))
assert(s6 == parse("[[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]"))
s7 = reduce_all(add(s6, parse("[1,[[[9,3],9],[[9,0],[0,7]]]]")))
s8 = reduce_all(add(s7, parse("[[[5,[7,4]],7],1]"))) 
s9 = reduce_all(add(s8, parse("[[[[4,2],2],6],[8,7]]"))) 
assert(s9 == parse("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"))

def magnitude_pair(L, n):
    assert(L[n] == '[')
    if L[n + 1] == '[':
        lhs, n = magnitude_pair(L, n + 1)
        if L[n + 1] == '[':
            rhs, n = magnitude_pair(L, n + 1)
        else:
            assert(type(L[n + 1]) == int)
            rhs = L[n + 1]
            n += 1
    elif type(L[n + 1]) == int:
        lhs = L[n + 1]
        n += 1
        if L[n + 1] == '[':
            rhs, n = magnitude_pair(L, n + 1)
        else:
            assert(type(L[n + 1]) == int)
            rhs = L[n + 1]
            n += 1
    return 3*lhs + 2*rhs, n + 1

def magnitude(L):
    return magnitude_pair(L, 0)[0]

# print(magnitude("[[1,2],[[3,4],5]]"))
assert(magnitude(parse("[[1,2],[[3,4],5]]")) == 143)

with open("2021_18_testcase") as file:
    sum = parse(file.readline().strip())
    for line in file.readlines()[0:]:
        sum = reduce_all(add(sum, parse(line.strip())))
assert(magnitude(sum) == 4140)

with open("2021_18_input") as file:
    sum = parse(file.readline().strip())
    for line in file.readlines()[0:]:
        sum = reduce_all(add(sum, parse(line.strip())))
print("Answer 1: " + str(magnitude(sum)))

sfn = []
with open("2021_18_input") as file:
    for line in file.readlines():
        sfn.append(parse(line.strip()))
best = None
for p in itertools.permutations(sfn, 2):
    mag = magnitude(reduce_all(add(p[0], p[1])))
    if not best or mag > best:
        best = mag
print("Answer 2: " + str(best))

