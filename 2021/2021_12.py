
caves = dict()
with open("2021_12_input") as file:
    for line in file:
        a, b = line.strip().split('-')
        if a in caves:
            caves[a].append(b)
        else:
            caves[a] = [b]
        if b in caves:
            caves[b].append(a)
        else:
            caves[b] = [a]

work = [["start"]]
routes = []
while work:
    r = work.pop()
    for r1 in caves[r[-1]]:
        if r1.islower() and r1 in r:
            continue
        if r1 == "end":
            routes.append(r + [r1])
        else:
            work.append(r + [r1])
print("Number of routes through the cave system part 1: " + str(len(routes)))

work = [(["start"], False)]
routes = []
while work:
    r, visited_small_cave_twice = work.pop()
    for r1 in caves[r[-1]]:
        if r1 == "start":
            continue
        if r1 == "end":
            routes.append(r + [r1])
            continue

        if visited_small_cave_twice and r1.islower() and r1 in r:
            continue

        visiting_small_cave_twice = r1.islower() and r1 in r
        work.append((r + [r1], visited_small_cave_twice or visiting_small_cave_twice))
print("Number of routes through the cave system part 2: " + str(len(routes)))
