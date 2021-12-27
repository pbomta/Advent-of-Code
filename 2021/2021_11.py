
def get_neighbors(p):
    r, c = p
    result = []
    if c > 0:
        result.append((r, c - 1))
    if c < 9:
        result.append((r, c + 1))
    if r > 0:
        result.append((r - 1, c))
        if c > 0:
            result.append((r - 1, c - 1))
        if c < 9:
            result.append((r - 1, c + 1))
    if r < 9:
        result.append((r + 1, c))
        if c > 0:
            result.append((r + 1, c - 1))
        if c < 9:
            result.append((r + 1, c + 1))
    return result

def get_flashing(energy_levels, flashing):
    result = []
    for r in range(len(energy_levels)):
        for c in range(len(energy_levels[0])):
            if energy_levels[r][c] > 9 and (r,c) not in flashing:
                result.append((r,c))
    return result

energy_levels = []
with open("2021_11_input") as file:
    for line in file:
        energy_levels.append([int(x) for x in line.strip()])
# print("Step 0: " + str(energy_levels))

total_flashes = 0
step = 0
while True:
    step += 1
    # Phase 1: increase energy levels
    for r in range(len(energy_levels)):
        for c in range(len(energy_levels[0])):
            energy_levels[r][c] += 1
    
    # Phase 2: propagate flash
    flashing = set()
    new_flashing = get_flashing(energy_levels, flashing)
    while new_flashing:
        for p in new_flashing:
            flashing.add(p)
            for n in get_neighbors(p):
                energy_levels[n[0]][n[1]] += 1
        new_flashing = get_flashing(energy_levels, flashing)

    # Phase 3: reset flashers to 0
    for p in flashing:
        energy_levels[p[0]][p[1]] = 0

    # Calculate results and stop simulating
    total_flashes += len(flashing)
    if step == 100:
        print("Total number of flashes after 100 steps: " + str(total_flashes))
    if len(flashing) == 10*10:
        print("At the end of step " + str(step) + " all octopi will flash.")
        break

