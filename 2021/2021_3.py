import functools

def most_common(bits, pos):
    nr_ones = functools.reduce(lambda B, b: B + 1 if b[pos] == '1' else B, bits, 0)
    search = '1' if nr_ones >= len(bits) / 2 else '0'
    keep = [b for b in bits if b[pos] == search]
    return search, keep

def least_common(bits, pos):
    nr_ones = functools.reduce(lambda B, b: B + 1 if b[pos] == '1' else B, bits, 0)
    search = '1' if nr_ones < len(bits) / 2 else '0'
    keep = [b for b in bits if b[pos] == search]
    return search, keep

with open("2021_3_input") as file:
    bits = [b.strip() for b in file.readlines()]
    print(str(bits))

    gamma = ""
    for n in range(len(bits[0])):
        mcb, _ = most_common(bits, n)
        gamma += mcb
    print(gamma)
    # epsilon = "".join(['1' if b == '0' else '0' for b in gamma])
    epsilon = ""
    for n in range(len(bits[0])):
        lcb, _ = least_common(bits, n)
        epsilon += lcb
    print(epsilon)
    g = int(gamma, 2)
    e = int(epsilon, 2)
    print("gamma: " + str(g))
    print("epsilon: " + str(e))
    print("Power consumption: " + str(g * e))

    oxygen_rating = bits
    for n in range(len(bits[0])):
        _, oxygen_rating = most_common(oxygen_rating, n)
        if len(oxygen_rating) == 1:
            break
    print(oxygen_rating)
    o = int(oxygen_rating[0], 2)
    print("Oxygen rating: " + str(o))

    scrubber_rating = bits
    for n in range(len(bits[0])):
        _, scrubber_rating = least_common(scrubber_rating, n)
        if len(scrubber_rating) == 1:
            break
    print(scrubber_rating)
    s = int(scrubber_rating[0], 2)
    print("CO2 Scrubber rating: " + str(s))
    print("Life support rating: " + str(o * s))

