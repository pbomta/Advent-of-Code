from math import inf

def simulate(vx, vy, tgt):
    x = 0
    y = 0
    max_y = y
    while x < tgt[0][1] and y > tgt[1][0]:
        x += vx
        y += vy
        if vx > 0:
            vx -= 1
        if vx < 0:
            vx += 1 # Useless?
        vy -= 1

        max_y = max(max_y, y)
        if x >= tgt[0][0] and x <= tgt[0][1] and y >= tgt[1][0] and y <= tgt[1][1]:
            return max_y
    return None

test_target = ((20, 30), (-10, -5))
assert(simulate(7, 2, test_target) == 3)
assert(simulate(6, 3, test_target) == 6)
assert(simulate(9, 0, test_target) == 0)
assert(simulate(17, -4, test_target) == None)

target = ((281, 311), (-74, -54)) # Input
# target = ((20, 30), (-10, -5)) # Test

trajectory_tops = []
for x in range(1, 1000):
    for y in range(-100, 1000):
        top = simulate(x, y, target)
        if top is not None:
            trajectory_tops.append(top)
print(max(trajectory_tops))
print(len(trajectory_tops))
