def score_incomplete(c):
    if c == ')': return 3
    if c == ']': return 57
    if c == '}': return 1197
    if c == '>': return 25137
    return 0

def score_autocomplete(c):
    if c == ')': return 1
    if c == ']': return 2
    if c == '}': return 3
    if c == '>': return 4
    return 0

def is_chunk_open(c):
    return c == '(' or c == '[' or c == '{' or c == '<'

def chunks_match(c, c2):
    if c == '(': return c2 == ')'
    if c == '[': return c2 == ']'
    if c == '{': return c2 == '}'
    if c == '<': return c2 == '>'
    return False

def get_chunk_match(c):
    if c == '(': return ')'
    if c == '[': return ']'
    if c == '{': return '}'
    if c == '<': return '>'
    return None

corrupted_score = 0
autocomplete_scores = []

with open("2021_10_input") as file:
    for line in file:
        chunks = []
        corrupted = False
        for c in line.strip():
            if is_chunk_open(c):
                chunks.append(c)
            else: # is_chunk_close
                if not chunks:
                    break
                c2 = chunks.pop()
                if not chunks_match(c2, c): # confusing order
                    corrupted_score += score_incomplete(c)
                    corrupted = True
                    break
        if not corrupted and chunks:
            autocomplete_score = 0
            autocomplete = []
            for c in reversed(chunks):
                autocomplete_score *= 5
                autocomplete_score += score_autocomplete(get_chunk_match(c)) # FIXME: merge functions
            autocomplete_scores.append(autocomplete_score)

autocomplete_score = sorted(autocomplete_scores)[round(len(autocomplete_scores) / 2 - 1)]
print("Corrupted lines score: " + str(corrupted_score))
print("Autocomplete lines score: " + str(autocomplete_score))