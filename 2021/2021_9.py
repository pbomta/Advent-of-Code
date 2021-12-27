import functools

def find_lower(p, heightmap):
    r, c = p
    lower = []
    if r > 0 and heightmap[r - 1][c] < heightmap[r][c]:
        lower.append((r - 1, c))
    if r < len(heightmap) - 1 and heightmap[r + 1][c] < heightmap[r][c]:
        lower.append((r + 1, c))
    if c > 0 and heightmap[r][c - 1] < heightmap[r][c]:
        lower.append((r, c - 1))
    if c < len(heightmap[0]) - 1 and heightmap[r][c + 1] < heightmap[r][c]:
        lower.append((r, c + 1))
    return lower

with open("2021_9_input") as file:
    heightmap = [[int(xx) for xx in list(x.strip())] for x in file.readlines()]

    basins = {}
    for r in range(len(heightmap)):
        for c in range(len(heightmap[0])):
            if heightmap[r][c] == 9:
                continue

            frontier = [(r, c)]
            basin = []
            lowest_point = None
            lowest_height = 9
            while len(frontier) > 0:
                p = frontier.pop()
                basin.append(p)
                frontier += find_lower(p, heightmap)
                if heightmap[p[0]][p[1]] < lowest_height:
                    lowest_point = p
                    lowest_height = heightmap[p[0]][p[1]]

            if lowest_point in basins:
                basins[lowest_point] |= set(basin)
            else:
                basins[lowest_point] = set(basin)

    lowest_points = list(basins)
    lowest_points.sort(key=lambda p: len(basins[p]), reverse=True)
    
    risk_level = functools.reduce(lambda H, p: H + 1 + heightmap[p[0]][p[1]], lowest_points, 0)
    print("Risk level: " + str(risk_level))
    
    size_mul_of_largest_three = 1
    for p in lowest_points[:3]:
        size_mul_of_largest_three *= len(basins[p])
    print("Multiple of the largest three basins' sizes: " + str(size_mul_of_largest_three))