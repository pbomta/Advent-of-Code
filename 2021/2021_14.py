polymer = ""
insertion = {}

with open("2021_14_input") as file:
    polymer = file.readline().strip()
    file.readline()
    for line in file:
        insertion[line[0] + line[1]] = line[6]

print("Template: " + polymer)
for step in range(10):
    new_polymer = ""
    for k in range(len(polymer) - 1):
        pair = polymer[k] + polymer[k + 1]
        if pair in insertion:
            new_polymer += polymer[k] + insertion[pair]
    new_polymer += polymer[-1]
    polymer = new_polymer
    print("Step " + str(step) + " done.")

# Calculate score
elements = {}
for e in polymer:
    if e in elements:
        elements[e] += 1
    else:
        elements[e] = 1

most_common_element = max(elements, key = elements.get)
least_common_element = min(elements, key = elements.get)
print(elements[most_common_element] - elements[least_common_element])