class board:
    def __init__(self):
        self.numbers = []

    def draw(self, n):
        for r in range(len(self.numbers)):
            for c, num in enumerate(self.numbers[r]):
                if num == n:
                    self.numbers[r][c] = 9999
                    return

    def bingo(self):
        for r in range(len(self.numbers)):
            bingo = True
            for c in range(len(self.numbers[r])):
                if self.numbers[r][c] != 9999:
                    bingo = False
                    break
            if bingo == True:
                return True
        for c in range(len(self.numbers[0])):
            bingo = True
            for r in range(len(self.numbers)):
                if self.numbers[r][c] != 9999:
                    bingo = False;
                    break
            if bingo == True:
                return True
        return False

    def score(self):
        result = 0
        for r in range(len(self.numbers)):
            for c, num in enumerate(self.numbers[r]):
                if num != 9999:
                    result += num
        return result

with open("2021_4_input") as file:
    drawn_numbers = [int(f) for f in file.readline().split(',')]
    # print(drawn_numbers)

    boards = []
    b = None
    for line in file:
        if line.strip() == "":
            if b:
                boards.append(b)
            b = board()
        else:
            b.numbers.append([int(n) for n in line.split()])
    boards.append(b)
    print("Found " + str(len(boards)) + " boards")    

    # Play Bingo
    bingos = []
    scores = []
    winning_nrs = []
    for num in drawn_numbers:
        for n in range(len(boards)):
            boards[n].draw(num)
            if n not in bingos and boards[n].bingo():
                bingos.append(n)
                scores.append(boards[n].score())
                winning_nrs.append(num)

    print("Winning board: " + str(bingos[0]))
    print("Score of that board: " + str(scores[0]))
    print("Winning number: " + str(winning_nrs[0]))
    print("Answer to puzzle part 1: " + str(winning_nrs[0] * scores[0]))

    print("Loser board: " + str(bingos[-1]))
    print("Score of that board: " + str(scores[-1]))
    print("Last number to play: " + str(winning_nrs[-1]))
    print("Answer to puzzle part 2: " + str(winning_nrs[-1] * scores[-1]))
