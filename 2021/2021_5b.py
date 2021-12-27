with open("2021_5_input") as file:
    coords_vents = []
    for line in file:
        coords_vents.append([[int(cc) for cc in c.strip().split(',')] for c in line.split("->")])
    x_max = 0
    y_max = 0
    for c_pair in coords_vents:
        x_max = max(c_pair[0][0], x_max)
        x_max = max(c_pair[1][0], x_max)
        y_max = max(c_pair[0][1], y_max)
        y_max = max(c_pair[1][1], y_max)
    print(x_max)
    print(y_max)

    field = [[0] * (x_max + 1) for n in range(y_max + 1)]
    for c_pair in coords_vents:
        print(c_pair)
        if c_pair[0][0] == c_pair[1][0]: # x1 == x2
            x = c_pair[0][0]
            y0 = min(c_pair[0][1], c_pair[1][1])
            y1 = max(c_pair[0][1], c_pair[1][1])
            for y in range(y0, y1 + 1):
                field[y][x] += 1
        elif c_pair[0][1] == c_pair[1][1]: # y1 == y2
            y = c_pair[0][1]
            x0 = min(c_pair[0][0], c_pair[1][0])
            x1 = max(c_pair[0][0], c_pair[1][0])
            for x in range(x0, x1 + 1):
                field[y][x] += 1
        else:
            c0 = c_pair[0]
            c1 = c_pair[1]
            if c1[0] < c0[0]:
                c0, c1 = c1, c0
            rc = round((c1[1] - c0[1]) / (c1[0] - c0[0]))
            y = c0[1]
            for x in range(c0[0], c1[0] + 1):
                field[y][x] += 1
                y += rc
    
    nr_danger_points = 0
    for row in field:
        for d in row:
            if d >= 2:
                nr_danger_points += 1

    print(nr_danger_points)