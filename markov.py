import random

# First order Markov chains. May extend to second if there is the need.

# Each row must add to 1.
markov_choices = [
    [0, 0, 0, 0, 0, 1, 0],
    #[0.3, 0.05, 0.1, 0.2, 0.25, 0.05, 0.05],    # Tonic
    [0.1, 0.05, 0.1, 0.3, 0.35, 0.05, 0.05],  # Supertonic
    [0.3, 0.05, 0.1, 0.1, 0.35, 0.05, 0.05],  # Mediant
    [0.3, 0.05, 0.05, 0.2, 0.3, 0.05, 0.05],  # Sub-dominant
    [0.4, 0.05, 0.15, 0.2, 0.1, 0.05, 0.05],  # Dominant
    [0.05, 0, 0.1, 0.25, 0.2, 0.25, 0.15],  # Sub-mediant
    [0, 0, 0.2, 0.05, 0.25, 0.2, 0.3],  # Subtonic
    [0.4, 0.05, 0.05, 0.05, 0.1, 0.25, 0.1],  # Leading
]

def check():
    for row in markov_choices:
        if sum(row) != 1:
            print "Badly configured Markov values. Index:", markov_choices.index(row), "Total:", sum(row)
            return False

    return True

def markov_choice(current):
    row = markov_choices[int(current)]
    total = sum(row)
    r = random.uniform(0, total)
    upto = 0
    for val in row:
        if upto + val > r:
            return str(row.index(val))
        upto += val
    return str(row.index(0))

def get(current):
    if check() == False:
        return
    return markov_choice(current)

# QUICK TEST 
# print get(0)