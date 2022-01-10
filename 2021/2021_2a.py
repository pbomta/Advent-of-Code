with open("2021_2_input") as file:
  lines = list(filter(lambda line: line.rstrip() != "", file.readlines()))
  commands = list(line.split() for line in lines)

  x = 0
  d = 0
  aim = 0
  d2 = 0
  for c in commands:
    if c[0] == "forward":
      x += int(c[1])
      d2 += aim * int(c[1])
    if c[0] == "down":
      d += int(c[1])
      aim += int(c[1])
    if c[0] == "up":
      d -= int(c[1])
      aim -= int(c[1])

  print("Final position 1: x = " + str(x) + ", d = " + str(d))
  print("Final position 2: x = " + str(x) + ", d2 = " + str(d2))
  print("Answer 1 = " + str(x * d))
  print("Answer 2 = " + str(x * d2))