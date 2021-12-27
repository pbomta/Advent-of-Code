import itertools

class display:
    def __init__(self, c):
        #  -0-
        # 1   2
        #  -3-
        # 4   5
        #  -6-
        self.decoder = [""] * 10
        self.decoder[0] = c[0] + c[1] + c[2] + c[4] + c[5] + c[6]
        self.decoder[1] = c[2] + c[5]
        self.decoder[2] = c[0] + c[2] + c[3] + c[4] + c[6]
        self.decoder[3] = c[0] + c[2] + c[3] + c[5] + c[6]
        self.decoder[4] = c[1] + c[2] + c[3] + c[5]
        self.decoder[5] = c[0] + c[1] + c[3] + c[5] + c[6]
        self.decoder[6] = c[0] + c[1] + c[3] + c[4] + c[5] + c[6] 
        self.decoder[7] = c[0] + c[2] + c[5]
        self.decoder[8] = c[0] + c[1] + c[2] + c[3] + c[4] + c[5] + c[6]
        self.decoder[9] = c[0] + c[1] + c[2] + c[3] + c[5] + c[6]

    def decode(self, digit):
        for d in range(10):
            if len(digit) == len(self.decoder[d]) and sorted(digit) == sorted(self.decoder[d]):
                return d
        return None

assert(display("abcdefg").decode("cf") == 1)
assert(display("abcdefg").decode("fc") == 1)
assert(display("abcdefg").decode("ab") == None)
assert(display("abcdefg").decode("abcdefg") == 8)
assert(display("abcdefg").decode("agbcdf") == 9)

def train(data):
    connections = "abcdefg"
    for conn in itertools.permutations(connections):
        d = display(conn)
        decoded = [d.decode(x) for x in data]
        # print("C: " + str(conn) + " results in: " + str(decoded))
        if None not in decoded:
            return d
    return None

with open("2021_8_input") as file:
    nr_discernable_numbers = 0
    s = 0
    for line in file:
        training_data, display_data = line.split('|', 1)
        training_data = training_data.strip().split(' ')
        display_data = display_data.strip().split(' ')

        for n in display_data:
            if len(n) < 5 or len(n) == 7:
                nr_discernable_numbers += 1

        d = train(training_data)
        n = d.decode(display_data[0]) * 1000
        n += d.decode(display_data[1]) * 100
        n += d.decode(display_data[2]) * 10
        n += d.decode(display_data[3]) * 1
        print("Output value: " + str(n))
        s += n

    print("Number of 1, 4, 7 or 8 digits on diplay: " + str(nr_discernable_numbers))
    print(s)