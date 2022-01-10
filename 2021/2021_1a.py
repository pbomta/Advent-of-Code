class ra:
  def __init__(self, n):
    self.total = n
    self.count = 1

  def add(self, n):
    self.total += n
    self.count += 1

with open("2021_1_input") as file:
  lines = file.readlines()
  lines = list(filter(lambda line: line.rstrip() != "", lines))
  depths = [int(line) for line in list(filter(None, lines))]

  prev = depths[0]
  averages = [ra(depths[0])]
  inc = 0
  inc_ra = 0;
  for d in depths[1:]:
    if d > prev:
      inc += 1
    prev = d

    for a in averages:
      if a.count < 3:
        a.add(d)
    averages.append(ra(d))

    completed = []
    for a in averages:
      if a.count == 3:
        completed.append(a)
    if len(completed) == 2:
      if completed[1].total > completed[0].total:
        inc_ra += 1
      averages.remove(completed[0])
  
  print("Number of increasing datapoints: " + str(inc))
  print("Number of increasing datapoints with a moving average of 3: " + str(inc_ra))