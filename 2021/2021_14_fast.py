def get_occ(pair, insertion, step):
    if pair not in insertion:
        return {}

    result = {insertion[pair] : 1}
    if step == 1:
        return result

    return result | get_occ(pair[0] + insertion[pair], insertion, step - 1) | get_occ(insertion[pair] + pair[1], insertion, step - 1)

polymer = ""
insertion = {}

with open("2021_14_input") as file:
    polymer = file.readline().strip()
    file.readline()
    for line in file:
        insertion[line[0] + line[1]] = line[6]


elements = {}
for e in polymer:
    if e in elements:
        elements[e] += 1
    else:
        elements[e] = 1

for k in range(len(polymer) - 1):
    pair = polymer[k] + polymer[k + 1]
    elements |= get_occ(pair, insertion, 10)

most_common_element = max(elements, key = elements.get)
least_common_element = min(elements, key = elements.get)
print(elements[most_common_element] - elements[least_common_element])