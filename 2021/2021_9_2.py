import functools

def find_next(p, heightmap):
    r, c = p
    lower = []
    if r > 0 and heightmap[r - 1][c] < 9:
        lower.append((r - 1, c))
    if r < len(heightmap) - 1 and heightmap[r + 1][c] < 9:
        lower.append((r + 1, c))
    if c > 0 and heightmap[r][c - 1] < 9:
        lower.append((r, c - 1))
    if c < len(heightmap[0]) - 1 and heightmap[r][c + 1] < 9:
        lower.append((r, c + 1))
    return lower

with open("2021_9_input") as file:
    heightmap = [[int(xx) for xx in list(x.strip())] for x in file.readlines()]

    basins = []
    searched = []
    for r in range(len(heightmap)):
        for c in range(len(heightmap[0])):
            if heightmap[r][c] == 9:
                continue

            frontier = [(r, c)]
            basin = []
            while frontier:
                p = frontier.pop()
                if p in searched:
                    continue
                searched.append(p)
                basin.append(p)
                frontier += find_next(p, heightmap)
            if basin:
                basins.append(basin)

    lowest_points = [min(B, key=lambda p: heightmap[p[0]][p[1]]) for B in basins]
    risk_level = functools.reduce(lambda H, p: H + 1 + heightmap[p[0]][p[1]], lowest_points, 0)
    print("Risk level: " + str(risk_level))

    basins.sort(key=lambda B: len(B), reverse=True)
    size_mul_of_largest_three = 1
    for B in basins[:3]:
        size_mul_of_largest_three *= len(B)
    print("Multiple of the largest three basins' sizes: " + str(size_mul_of_largest_three))