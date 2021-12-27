from math import inf

# Range is a pair, inclusive, min to max
def rangeIntersects(a, b):
    return a[0] <= b[1] and b[0] <= a[1]

assert(rangeIntersects((1,2), (3, 4)) == False)
assert(rangeIntersects((0,10), (2, 8)) == True)
assert(rangeIntersects((2, 8), (0,10)) == True)
assert(rangeIntersects((0,10), (5, 15)) == True)
assert(rangeIntersects((0,10), (-5, 5)) == True)
# Etc.

def rangeContains(a, b):
    return a[0] >= b[0] and a[1] <= b[1]

assert(rangeContains((1,2), (0,10)) == True)
assert(rangeContains((0,10), (1,2)) == False)
# Etc.

def rangeLength(a):
    return a[1] - a[0] + 1

assert(rangeLength((10,10)) == 1)

# Prec. ranges intersect
def rangeIntersection(a, b):
    return (max(a[0], b[0]), min(a[1], b[1]))

assert(rangeIntersection((0, 10), (5, 15)) == (5, 10))
assert(rangeIntersection((5, 15), (0, 10)) == (5, 10))
assert(rangeIntersection((2, 4), (0, 10)) == (2, 4))

def cubeSize(a):
    return rangeLength(a[0]) * rangeLength(a[1]) * rangeLength(a[2])

def cubeIntersects(a, b):
    return rangeIntersects(a[0], b[0]) \
        and rangeIntersects(a[1], b[1]) \
        and rangeIntersects(a[2], b[2])
    
def cubeIntersection(a, b):
    if not cubeIntersects(a, b):
        return None
    return (rangeIntersection(a[0], b[0]), rangeIntersection(a[1], b[1]), rangeIntersection(a[2], b[2]))


def parseRangeText(S):
    assert(S[1] == '=')
    return (int(S[2:].split("..")[0]), int(S[2:].split("..")[1]))

def readInput(filename):
    result = []
    with open(filename) as file:
        for line in file:
            command, range_text = line.strip().split(' ')
            x_range, y_range, z_range = range_text.split(',')
            result.append((command, (parseRangeText(x_range), parseRangeText(y_range), parseRangeText(z_range))))
    return result

instructions = readInput("2021_22_input")
# print(instructions)

# initregion = ((-50, 50), (-50, 50), (-50, 50)) # Part 1
initregion = ((-inf, inf), (-inf, inf), (-inf, inf)) # Part 2

on_switches = []
off_switches = []
for command, i in instructions:
    new_cube = cubeIntersection(initregion, i)
    if new_cube == None:
        continue
    
    new_on = []
    new_off = []
    if command == "on":
        new_on.append(new_cube)
        for C in on_switches:
            intr = cubeIntersection(new_cube, C)
            if intr != None:
                new_off.append(intr)
        for C in off_switches:
            intr = cubeIntersection(new_cube, C)
            if intr != None:
                new_on.append(intr)
    else:
        for C in on_switches:
            intr = cubeIntersection(new_cube, C)
            if intr != None:
                new_off.append(intr)
        for C in off_switches:
            intr = cubeIntersection(new_cube, C)
            if intr != None:
                new_on.append(intr)
    on_switches += new_on
    off_switches += new_off

    total_size = 0
    for C in on_switches:
        total_size += cubeSize(C)
    for C in off_switches:
        total_size -= cubeSize(C)
    print(total_size)
