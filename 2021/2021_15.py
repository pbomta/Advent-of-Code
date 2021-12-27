from math import inf
from collections import defaultdict

with open("2021_15_input") as file:
    risk_levels_base = [line.strip() for line in file]

multiplier = 5
risk_levels = []
for m in range(multiplier):
    for base_row in risk_levels_base:
        row = ""
        for n in range(multiplier):
            for a in base_row:
                b = int(a) + m + n
                if b > 9:
                    b -= 9
                row += str(b)
        risk_levels.append(row)

end_point = (len(risk_levels) - 1, len(risk_levels[0]) - 1)

def get_neighbors(p):
    r, c = p
    result = []
    if c > 0:
        result.append((r, c - 1))
    if c < end_point[1]:
        result.append((r, c + 1))
    if r > 0:
        result.append((r - 1, c))
    if r < end_point[1]:
        result.append((r + 1, c))
    return result

frontier = [((0,0), 0)]
minrisk = defaultdict(lambda: inf, {(0,0): 0})
visited = set()
min_risk_endpoint = inf
while frontier:
    current, risk = frontier.pop()
    
    if current == end_point:
        min_risk_endpoint = minrisk[current]
        break

    visited.add(current)
    
    next = get_neighbors(current)
    for p in next:
        if p in visited:
            continue # We're never going back
        new_risk = risk + int(risk_levels[p[0]][p[1]])
        if new_risk < minrisk[p]:
            minrisk[p] = new_risk
            frontier.append((p, new_risk))
    frontier.sort(key=lambda a: a[1], reverse=True)

print("Least risk to endpoint: " + str(min_risk_endpoint))