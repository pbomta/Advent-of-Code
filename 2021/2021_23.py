import copy
import math

class burrow:
    # Map is hardcoded
    burrowsPos = (2, 4, 6, 8)
    anthropodStr = ("A", "B", "C", "D")

    def __init__(self, hallway, burrows):
        self.hallway = hallway
        self.burrows = burrows
        self.energy_usage = 0

    def __str__(self):
        result = ""
        for h in self.hallway:
            if type(h) == int:
                result += self.anthropodStr[h]
            else:
                result += h
        result += "\n "
        for b in range(len(self.burrows)):
            if len(self.burrows[b]) == 2:
                result += " " + self.anthropodStr[self.burrows[b][1]]
            else:
                result += "  "
        result += "  \n "
        for b in range(len(self.burrows)):
            if len(self.burrows[b]) > 0:
                result += " " + self.anthropodStr[self.burrows[b][0]]
            else:
                result += "  "
        result += "  \n"
        return result

    def __eq__(self, other):
        return self.hallway == other.hallway and self.burrows == other.burrows and self.energy_usage == other.energy_usage

    def __ne__(self, other):
        return not self.__eq__(other)

    # def __hash__(self):
    #     return 

    def __copy__(self):
        B = burrow(list(self.hallway), copy.deepcopy(self.burrows))
        B.energy_usage = self.energy_usage
        return B

    def isDone(self):
        for a in range(4):
            if self.burrows[a] != [a, a]:
                return False
        return True

    def score(self):
        result = -self.energy_usage
        for b in range(len(self.burrows)):
            B = self.burrows[b]
            if len(B) > 0:
                if B[0] == b: result += 2000
            if len(B) > 1:
                if B[1] == b: result += 2000
        return result

    def moveToBurrow(self, pos): # pos in hallway
        if self.hallway[pos] == '.':
            return None # Not an anthropod
        a = self.hallway[pos] # Anthropod

        if self.burrows[a] == []:
            steps = 2
        elif self.burrows[a] == [a]:
            steps = 1
        else:
            return None # No room or other anthropods are still in there
        
        # Check path (path inside burrow is clear)
        inc = 1 if self.burrowsPos[a] > pos else -1
        p = pos
        while p != self.burrowsPos[a]:
            p += inc
            steps += 1
            if self.hallway[p] != '.':
                return None # Blocked
        
        # Done! We can make that move
        result = copy.copy(self)
        result.hallway[pos] = '.'
        result.burrows[a].append(a)
        assert(len(result.burrows[a]) <= 2)
        result.energy_usage += steps * pow(10, a)
        return result

    def moveToHallway(self, b): # b = burrow index
        if self.burrows[b] == []:
            return None # Empty burrow
        if self.burrows[b] == [b]:
            return None # or only filled with the correct anthropods
        if self.burrows[b] == [b, b]:
            return None
        a = self.burrows[b][-1]
        

        # Now find all possibilities where it can go
        result = []

        p = self.burrowsPos[b]
        # Move into hallway
        steps = (3 - len(self.burrows[b]))
        while p > 0:
            p -= 1
            steps += 1
            if self.hallway[p] != '.':
                break # Blocked
            if p in self.burrowsPos:
                continue # Move beyond burrow exits
            new_state = copy.copy(self)
            new_state.hallway[p] = a
            new_state.burrows[b].pop() # pops last item
            new_state.energy_usage += steps * pow(10, a)
            result.append(new_state)

        p = self.burrowsPos[b]
        # Move into hallway
        steps = (3 - len(self.burrows[b]))
        while p < len(self.hallway) - 1:
            p += 1
            steps += 1
            if self.hallway[p] != '.':
                break # Blocked
            if p in self.burrowsPos:
                continue # Move beyond burrow exits
            new_state = copy.copy(self)
            new_state.hallway[p] = a
            new_state.burrows[b].pop() # pops last item
            new_state.energy_usage += steps * pow(10, a)
            result.append(new_state)
        return result

    def possibilities(self):
        result = []
        # All possibilities where an amphipod moves out of a burrow
        for b in range(len(self.burrowsPos)):
            new_states = self.moveToHallway(b)
            if new_states:
                result += new_states
        
        # All possibilities where an amphipod moves into its own burrow
        for pos in range(len(self.hallway)):
            new_state = self.moveToBurrow(pos)
            if new_state:
                result.append(new_state)

        return result

# Testcase. Costs 12521 energy
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
Btest0 = burrow(['.','.','.','.','.','.','.','.','.','.','.'], [[0, 1], [3, 2], [2, 1], [0, 3]])
Btest0_next = Btest0.moveToHallway(2)
# for B in Btest0_next:
#     print(B)
Btest1 = Btest0_next[1]
assert(Btest1.energy_usage == 40)
assert(Btest1.moveToHallway(2) == None)
Btest1_next = Btest1.moveToHallway(1)
# for B in Btest1_next:
#     print(B)
Btest2 = Btest1_next[0].moveToBurrow(5)
assert(Btest2.energy_usage == 440)
assert(Btest2.moveToHallway(2) == None)

#############  A = 0
#...........#  B = 1
###C#A#B#D###  C = 2
  #C#A#D#B#    D = 3
  #########
B = burrow(['.','.','.','.','.','.','.','.','.','.','.'], [[2, 2], [0, 0], [3, 1], [1, 3]])

# Search for the best answer
frontier = [B]
visited = []
lowest_energy = math.inf
while frontier:
    frontier.sort(key=lambda B: B.score(), reverse=False)
    print("lowest energy: " + str(lowest_energy) + " todo: " + str(len(frontier)) + " checked: " + str(len(visited)))
    # print(frontier[-1])
    next_burrow = frontier.pop() # Best score at the back

    # Consider the best one
    is_new = True
    found_better = False
    for n in range(len(visited)):
        if visited[n].hallway == next_burrow.hallway and visited[n].burrows == next_burrow.burrows:
            is_new = False
            if visited[n].energy_usage > next_burrow.energy_usage:
                visited[n] = next_burrow
                found_better = True
            break
    if is_new:
        visited.append(next_burrow)
    elif not found_better:
        continue
    
    # Propagate into new states
    next_states = next_burrow.possibilities()
    for S in next_states:
        if S.energy_usage >= lowest_energy:
            continue # Skip this one, can't be better
        elif S.isDone():
            if S.energy_usage < lowest_energy:
                lowest_energy = S.energy_usage
                print("Lowest energy so far: " + str(lowest_energy) + " checked: " + str(len(visited)))
        else:
            frontier.append(S)

# answer > 6736. != 12766