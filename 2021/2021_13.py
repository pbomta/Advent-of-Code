
def fold_y(dots, axis):
    print("Folding along the Y-axis of " + str(axis))
    result = set()
    for dot in dots:
        if dot[1] < axis:
            result.add(dot)
        else:
            result.add((dot[0], axis - (dot[1] - axis)))
    return result

def fold_x(dots, axis):
    print("Folding along the X-axis of " + str(axis))
    result = set()
    for dot in dots:
        if dot[0] < axis:
            result.add(dot)
        else:
            result.add((axis - (dot[0] - axis), dot[1]))
    return result

dots = []
instructions = []
with open("2021_13_input") as file:
    for line in file:
        if not line.strip():
            continue

        if line[0] == 'f': # Dumb parsing
            axis, nr = line.split()[2].split('=')
            instructions.append((axis, int(nr)))
        else:
            dots.append(tuple(int(c) for c in line.split(',')))

first_fold = True
for i in instructions:
    if i[0] == 'x':
        dots = fold_x(dots, i[1])
    elif i[0] == 'y':
        dots = fold_y(dots, i[1])
    if first_fold:
        print("Number of dots after one fold: " + str(len(dots)))
        first_fold = False

max_x, _ = max(dots, key=lambda c: c[0])
_, max_y = max(dots, key=lambda c: c[1])
output = ""
for y in range(max_y + 1):
    for x in range(max_x + 1):
        if (x, y) in dots:
            output += "#"
        else:
            output += " "
    output += "\n"
print(output)